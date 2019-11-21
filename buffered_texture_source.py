from abc import ABC
from functools import partial
from web_data_api.tiled_raster_maps import IRequestTexture

class ITileTextureSource():
    def get_tile_texture_name(self, tile_index):
        pass

    def tile_texture_name_by_index(self, tile_index):
        return f'{self.data_source.__class__.__name__}-tile{list(tile_index)}'

class BufferedTileTextureSource(ITileTextureSource):
    def __init__(self, data_source, texture_library):
        self.data_source = data_source
        self._loaded_data = {}
        self.texture_library = texture_library
        self.lock = threading.Lock()

    def set_texture(self,tile_index, tile_object):
        if tuple(tile_index) in self._loaded_data.keys():
            texture_name = self.tile_texture_name_by_index(tile_index)
            tile_object.material.set_texture(f'diffuse', texture_name)
        else:
            self.data_source.on_complete.add(partial(self._on_texture_loaded,tile_object)

    def _on_texture_loaded(self, tile_object, image_64):
        texture_name = self.tile_texture_name_by_index(tile_index)
        with self.lock:
            self.texture_library.set(texture_name, image_64)
            self._loaded_data[tuple(tile_index)] = tile

        tile_object.material.set_texture(f'diffuse', texture_name)



    def get_tile(self, tile_index):
        return self._loaded_data[tuple(tile_index)]
