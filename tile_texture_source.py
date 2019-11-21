import threading
from functools import partial

from pangolin.server_application.texture_library import TextureLibrary

from abc import ABC, abstractmethod
from pgl.gis.utility import Transfer, Tools
from gis.maps.tiled_raster_maps import IRequestTexture

class ITileTextureSource():
    def get_tile_texture_name(self, tile_index):
        pass


class BufferedTileTextureSource(ITileTextureSource):
    def __init__(self, data_source:IRequestTexture, texture_library:TextureLibrary):
        self.data_source = data_source
        self._loaded_data = []
        self.texture_library = texture_library
        self.texture_library_lock = None
        self.lock = threading.Lock()


    def get_tile_texture_name(self,tile_index, on_complete_callback):
        """
        param tile_index: the tile index in form of (x,y,z)
        return: the texture name loaded in texture library
        """
        if tile_index in self._loaded_data:
            texture_name = self.tile_texture_name_by_index(tile_index)
            on_complete_callback(texture_name)
        else:
            self.data_source.request_texture(
                tile_index,
                partial(self._on_texture_loaded, tile_index, on_complete_callback)
            )

    def _on_texture_loaded(self,tile_index, on_complete_callback, img_64):
        if img_64 is None:
            return 

        texture_name = self.tile_texture_name_by_index(tile_index)
        with self.lock:
            self._loaded_data.append(tile_index)

        if self.texture_library_lock:
            with self.texture_library_lock:
                self.texture_library.set(texture_name, img_64)
        else:
            self.texture_library.set(texture_name, img_64)
        on_complete_callback(texture_name)

    def tile_texture_name_by_index(self, tile_index):
        return f'{self.data_source.__class__.__name__}-tile{list(tile_index)}'

