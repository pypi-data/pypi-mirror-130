from __future__ import annotations

import numpy
import copy
import math

from typing import Tuple, Optional, TYPE_CHECKING

from amulet import log, entity_support
from amulet.api.registry import BlockManager, BiomeManager
from amulet.api.block import Block
from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity
from amulet.api.chunk import Chunk, BiomesShape
from amulet.api.data_types import (
    AnyNDArray,
    BlockNDArray,
    BlockCoordinates,
    GetChunkCallback,
    TranslateBlockCallback,
    TranslateEntityCallback,
    GetBlockCallback,
    TranslateBlockCallbackReturn,
    TranslateEntityCallbackReturn,
    VersionNumberAny,
    VersionIdentifierType,
)

if TYPE_CHECKING:
    from PyMCTranslate import Version, TranslationManager


class Translator:
    def translator_key(self, version_number: VersionNumberAny) -> VersionIdentifierType:
        return self._translator_key(version_number)

    def _translator_key(
        self, version_number: VersionNumberAny
    ) -> VersionIdentifierType:
        """
        Return the version key for PyMCTranslate

        :return: The tuple version key for PyMCTranslate
        """
        raise NotImplementedError

    @staticmethod
    def is_valid(key: Tuple) -> bool:
        """
        Returns whether this translator is able to translate the chunk type with a given identifier key,
        generated by the decoder.

        :param key: The key who's decodability needs to be checked.
        :return: True if this translator is able to translate the chunk type associated with the key, False otherwise.
        """
        raise NotImplementedError

    @staticmethod
    def _translate(
        chunk: Chunk,
        get_chunk_callback: Optional[GetChunkCallback],
        translate_block: TranslateBlockCallback,
        translate_entity: TranslateEntityCallback,
        full_translate: bool,
    ):
        if full_translate:
            todo = []
            output_block_entities = []
            output_entities = []
            finished = BlockManager()
            palette_mappings = {}

            # translate each block without using the callback
            for i, input_block in enumerate(chunk.block_palette):
                input_block: Block
                (
                    output_block,
                    output_block_entity,
                    output_entity,
                    extra,
                ) = translate_block(input_block, None, (0, 0, 0))
                if extra and get_chunk_callback:
                    todo.append(i)
                elif output_block is not None:
                    palette_mappings[i] = finished.get_add_block(output_block)
                    if output_block_entity is not None:
                        for cy in chunk.blocks.sub_chunks:
                            for x, y, z in zip(
                                *numpy.where(chunk.blocks.get_sub_chunk(cy) == i)
                            ):
                                output_block_entities.append(
                                    output_block_entity.new_at_location(
                                        x + chunk.cx * 16,
                                        y + cy * 16,
                                        z + chunk.cz * 16,
                                    )
                                )
                else:
                    # TODO: this should only happen if the object is an entity, set the block to air
                    pass

                if output_entity and entity_support:
                    for cy in chunk.blocks.sub_chunks:
                        for x, y, z in zip(
                            *numpy.where(chunk.blocks.get_sub_chunk(cy) == i)
                        ):
                            x += chunk.cx * 16
                            y += cy * 16
                            z += chunk.cz * 16
                            for entity in output_entity:
                                e = copy.deepcopy(entity)
                                e.location += (x, y, z)
                                output_entities.append(e)

            # re-translate the blocks that require extra information
            block_mappings = {}
            for index in todo:
                for cy in chunk.blocks.sub_chunks:
                    for x, y, z in zip(
                        *numpy.where(chunk.blocks.get_sub_chunk(cy) == index)
                    ):
                        y += cy * 16

                        def get_block_at(
                            pos: BlockCoordinates,
                        ) -> Tuple[Block, Optional[BlockEntity]]:
                            """Get a block at a location relative to the current block"""
                            nonlocal x, y, z, chunk, cy

                            # calculate position relative to chunk base
                            dx, dy, dz = pos
                            dx += x
                            dy += y
                            dz += z

                            abs_x = dx + chunk.cx * 16
                            abs_y = dy
                            abs_z = dz + chunk.cz * 16

                            # calculate relative chunk position
                            cx = dx // 16
                            cz = dz // 16
                            if cx == 0 and cz == 0:
                                # if it is the current chunk
                                block = chunk.block_palette[chunk.blocks[dx, dy, dz]]
                                return (
                                    block,
                                    chunk.block_entities.get((abs_x, abs_y, abs_z)),
                                )

                            # if it is in a different chunk
                            local_chunk = get_chunk_callback(cx, cz)
                            block = local_chunk.block_palette[
                                local_chunk.blocks[dx % 16, dy, dz % 16]
                            ]
                            return (
                                block,
                                local_chunk.block_entities.get((abs_x, abs_y, abs_z)),
                            )

                        input_block = chunk.block_palette[chunk.blocks[x, y, z]]
                        (
                            output_block,
                            output_block_entity,
                            output_entity,
                            _,
                        ) = translate_block(
                            input_block,
                            get_block_at,
                            (x + chunk.cx * 16, y, z + chunk.cz * 16),
                        )
                        if output_block is not None:
                            block_mappings[(x, y, z)] = finished.get_add_block(
                                output_block
                            )
                            if output_block_entity is not None:
                                output_block_entities.append(
                                    output_block_entity.new_at_location(
                                        x + chunk.cx * 16, y, z + chunk.cz * 16
                                    )
                                )
                        else:
                            # TODO: set the block to air
                            pass

                        if output_entity and entity_support:
                            for entity in output_entity:
                                e = copy.deepcopy(entity)
                                e.location += (x, y, z)
                                output_entities.append(e)

            if entity_support:
                for entity in chunk.entities:
                    output_block, output_block_entity, output_entity = translate_entity(
                        entity
                    )
                    if output_block is not None:
                        block_location = (
                            int(math.floor(entity.x)),
                            int(math.floor(entity.y)),
                            int(math.floor(entity.z)),
                        )
                        block_mappings[block_location] = output_block
                        if output_block_entity:
                            output_block_entities.append(
                                output_block_entity.new_at_location(*block_location)
                            )
                    if output_entity:
                        for e in output_entity:
                            e.location = entity.location
                            output_entities.append(e)

            for cy in chunk.blocks.sub_chunks:
                old_blocks = chunk.blocks.get_sub_chunk(cy)
                new_blocks = numpy.zeros(old_blocks.shape, dtype=old_blocks.dtype)
                for old, new in palette_mappings.items():
                    new_blocks[old_blocks == old] = new
                chunk.blocks.add_sub_chunk(cy, new_blocks)
            for (x, y, z), new in block_mappings.items():
                chunk.blocks[x, y, z] = new
            chunk.block_entities = output_block_entities
            chunk.entities = output_entities
            chunk._block_palette = finished

    def to_universal(
        self,
        chunk_version: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
        get_chunk_callback: Optional[GetChunkCallback],
        full_translate: bool,
    ) -> Chunk:
        """
        Translate an interface-specific chunk into the universal format.

        :param chunk_version: The version number (int or tuple) of the input chunk
        :param translation_manager: TranslationManager used for the translation
        :param chunk: The chunk to translate.
        :param get_chunk_callback: function callback to get a chunk's data
        :param full_translate: if true do a full translate. If false just unpack the block_palette (used in callback)
        :return: Chunk object in the universal format.
        """
        version = translation_manager.get_version(*self._translator_key(chunk_version))
        self._biomes_to_universal(version, chunk)
        self._blocks_entities_to_universal(
            chunk_version,
            translation_manager,
            chunk,
            get_chunk_callback,
            full_translate,
        )
        return chunk

    def _blocks_entities_to_universal(
        self,
        chunk_version: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
        get_chunk_callback: Optional[GetChunkCallback],
        full_translate: bool,
    ):
        version = translation_manager.get_version(*self._translator_key(chunk_version))

        def translate_block(
            input_object: Block,
            get_block_callback: Optional[GetBlockCallback],
            block_location: BlockCoordinates,
        ) -> TranslateBlockCallbackReturn:
            final_block = None
            final_block_entity = None
            final_entities = []
            final_extra = False

            for depth, block in enumerate(input_object.block_tuple):
                (
                    output_object,
                    output_block_entity,
                    extra,
                ) = version.block.to_universal(
                    block,
                    get_block_callback=get_block_callback,
                    block_location=block_location,
                )

                if isinstance(output_object, Block):
                    if not output_object.namespace.startswith("universal"):
                        log.debug(
                            f"Error translating {input_object.full_blockstate} to universal. Got {output_object.full_blockstate}"
                        )
                    if final_block is None:
                        final_block = output_object
                    else:
                        final_block += output_object
                    if depth == 0:
                        final_block_entity = output_block_entity

                elif isinstance(output_object, Entity):
                    final_entities.append(output_object)
                    # TODO: offset entity coords

                final_extra |= extra

            return final_block, final_block_entity, final_entities, final_extra

        def translate_entity(input_object: Entity) -> TranslateEntityCallbackReturn:
            final_block = None
            final_block_entity = None
            final_entities = []
            # TODO
            return final_block, final_block_entity, final_entities

        self._translate(
            chunk,
            get_chunk_callback,
            translate_block,
            translate_entity,
            full_translate,
        )

    @staticmethod
    def _biomes_to_universal(translator_version: "Version", chunk: Chunk):
        chunk._biome_palette = BiomeManager(
            [
                translator_version.biome.to_universal(biome)
                for biome in chunk.biome_palette
            ]
        )

    def from_universal(
        self,
        max_world_version_number: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
        get_chunk_callback: Optional[GetChunkCallback],
        full_translate: bool,
    ) -> Chunk:
        """
        Translate a universal chunk into the interface-specific format.

        :param max_world_version_number: The version number (int or tuple) of the max world version
        :param translation_manager: TranslationManager used for the translation
        :param chunk: The chunk to translate.
        :param get_chunk_callback: function callback to get a chunk's data
        :param full_translate: if true do a full translate. If false just pack the block_palette (used in callback)
        :return: Chunk object in the interface-specific format and block_palette.
        """
        version = translation_manager.get_version(
            *self._translator_key(max_world_version_number)
        )
        self._blocks_entities_from_universal(
            max_world_version_number,
            translation_manager,
            chunk,
            get_chunk_callback,
            full_translate,
        )
        self._biomes_from_universal(version, chunk)
        return chunk

    def _blocks_entities_from_universal(
        self,
        max_world_version_number: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
        get_chunk_callback: Optional[GetChunkCallback],
        full_translate: bool,
    ):
        version = translation_manager.get_version(
            *self._translator_key(max_world_version_number)
        )

        # TODO: perhaps find a way so this code isn't duplicated in three places
        def translate_block(
            input_object: Block,
            get_block_callback: Optional[GetBlockCallback],
            block_location: BlockCoordinates,
        ) -> TranslateBlockCallbackReturn:
            final_block = None
            final_block_entity = None
            final_entities = []
            final_extra = False

            for depth, block in enumerate(input_object.block_tuple):
                (
                    output_object,
                    output_block_entity,
                    extra,
                ) = version.block.from_universal(
                    block,
                    get_block_callback=get_block_callback,
                    block_location=block_location,
                )

                if isinstance(output_object, Block):
                    if __debug__ and output_object.namespace.startswith("universal"):
                        log.debug(
                            f"Error translating {input_object.blockstate} from universal. Got {output_object.blockstate}"
                        )
                    if final_block is None:
                        final_block = output_object
                    else:
                        final_block += output_object
                    if depth == 0:
                        final_block_entity = output_block_entity

                elif isinstance(output_object, Entity):
                    final_entities.append(output_object)
                    # TODO: offset entity coords

                final_extra |= extra

            return final_block, final_block_entity, final_entities, final_extra

        def translate_entity(input_object: Entity) -> TranslateEntityCallbackReturn:
            final_block = None
            final_block_entity = None
            final_entities = []
            # TODO
            return final_block, final_block_entity, final_entities

        self._translate(
            chunk,
            get_chunk_callback,
            translate_block,
            translate_entity,
            full_translate,
        )

    @staticmethod
    def _biomes_from_universal(translator_version: "Version", chunk: Chunk):
        chunk._biome_palette = BiomeManager(
            [
                translator_version.biome.from_universal(biome)
                for biome in chunk.biome_palette
            ]
        )

    def unpack(
        self,
        chunk_version: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
        palette: AnyNDArray,
    ) -> Chunk:
        """
        Unpack the version-specific block_palette into the stringified version where needed.

        :return: The block_palette converted to block objects.
        """
        version_identifier = self._translator_key(chunk_version)
        self._unpack_blocks(translation_manager, version_identifier, chunk, palette)
        self._unpack_biomes(translation_manager, version_identifier, chunk)
        return chunk

    @staticmethod
    def _unpack_blocks(
        translation_manager: "TranslationManager",
        version_identifier: VersionIdentifierType,
        chunk: Chunk,
        block_palette: AnyNDArray,
    ):
        """
        Unpack the version-specific block_palette into the stringified version where needed.
        :return: The block_palette converted to block objects.
        """
        chunk._block_palette = BlockManager(block_palette)

    @staticmethod
    def _unpack_biomes(
        translation_manager: "TranslationManager",
        version_identifier: VersionIdentifierType,
        chunk: Chunk,
    ):
        """
        Unpack the version-specific biome_palette into the stringified version where needed.
        :return: The biome_palette converted to biome objects.
        """
        version = translation_manager.get_version(*version_identifier)

        if chunk.biomes.dimension == BiomesShape.Shape2D:
            biome_int_palette, biome_array = numpy.unique(
                chunk.biomes, return_inverse=True
            )
            chunk.biomes = biome_array.reshape(chunk.biomes.shape)
            chunk._biome_palette = BiomeManager(
                [version.biome.unpack(biome) for biome in biome_int_palette]
            )
        elif chunk.biomes.dimension == BiomesShape.Shape3D:
            biomes = {}
            palette = []
            palette_length = 0
            for sy in chunk.biomes.sections:
                biome_int_palette, biome_array = numpy.unique(
                    chunk.biomes.get_section(sy), return_inverse=True
                )
                biomes[sy] = (
                    biome_array.reshape(chunk.biomes.section_shape) + palette_length
                )
                palette_length += len(biome_int_palette)
                palette.append(biome_int_palette)

            if palette:
                chunk_palette, lut = numpy.unique(
                    numpy.concatenate(palette), return_inverse=True
                )
                lut = lut.astype(numpy.uint32)
                for sy in biomes:
                    biomes[sy] = lut[biomes[sy]]

                chunk.biomes = biomes
                chunk._biome_palette = BiomeManager(
                    numpy.vectorize(version.biome.unpack)(chunk_palette)
                )

    def pack(
        self,
        max_world_version_number: VersionNumberAny,
        translation_manager: "TranslationManager",
        chunk: Chunk,
    ) -> Tuple[Chunk, AnyNDArray]:
        """
        Translate the list of block objects into a version-specific block_palette.
        :return: The block_palette converted into version-specific blocks (ie id, data tuples for 1.12)
        """
        version_identifier = self._translator_key(max_world_version_number)
        version = translation_manager.get_version(*version_identifier)
        self._pack_biomes(translation_manager, version_identifier, chunk)
        return (
            chunk,
            self._pack_block_palette(version, numpy.array(chunk.block_palette.blocks)),
        )

    def _pack_block_palette(
        self, version: "Version", palette: BlockNDArray
    ) -> AnyNDArray:
        """
        Pack the list of block objects into a version-specific block_palette.
        :return: The block_palette converted into version-specific blocks (ie id, data tuples for 1.12)
        """
        return palette

    @staticmethod
    def _pack_biomes(
        translation_manager: "TranslationManager",
        version_identifier: VersionIdentifierType,
        chunk: Chunk,
    ):
        """
        Unpack the version-specific biome_palette into the stringified version where needed.
        :return: The biome_palette converted to biome objects.
        """
        version = translation_manager.get_version(*version_identifier)

        biome_palette = numpy.array(
            [version.biome.pack(biome) for biome in chunk.biome_palette], numpy.uint32
        )
        if chunk.biomes.dimension == BiomesShape.Shape2D:
            chunk.biomes = biome_palette[chunk.biomes]
        elif chunk.biomes.dimension == BiomesShape.Shape3D:
            chunk.biomes = {
                sy: biome_palette[chunk.biomes.get_section(sy)]
                for sy in chunk.biomes.sections
            }
        chunk._biome_palette = BiomeManager()
