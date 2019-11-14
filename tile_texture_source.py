import threading
from pgl.gis.utility import Transfer, Tools
from pgl.gis.classes import Tile

class ITileTextureSource():
    def get_tile_texture_name(self, tile_index):
        pass


class BufferedTileTextureSource(ITileTextureSource):
    def __init__(self, data_source, texture_library):
        self.data_source = data_source
        self._loaded_data = {}
        self.texture_library = texture_library
        self.lock = threading.Lock()

    def get_tile_texture_name(self,tile_index):
        """
        param tile_index: the tile index in form of (x,y,z)
        return: the texture name loaded in texture library
        """
        if tuple(tile_index) in self._loaded_data.keys():
            return self.tile_texture_name_by_index(tile_index)
        else:
            return self._load_tile_map_from_source(tile_index)

    def _load_tile_map_from_source(self, tile_index):
        tile = self.data_source.get_tile(tile_index)
        assert isinstance(tile, Tile)
        name = self.tile_texture_name_by_index(tile_index)
        with self.lock:
            self.texture_library.set(name, tile.image_64)
            self._loaded_data[tuple(tile_index)] = tile
        return name

    def tile_texture_name_by_index(self, tile_index):
        return f'{self.data_source.__class__.__name__}-tile{list(tile_index)}'

    def get_tile(self, tile_index):
        return self._loaded_data[tuple(tile_index)]

