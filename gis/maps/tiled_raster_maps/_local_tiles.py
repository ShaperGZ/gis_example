
# python std
from typing import Callable
from threading import Thread, Lock

# pangolin framwork
from pangolin.server_application.texture_library import TextureLibrary
from pangolin.core.delegate import Delegate
import pangolin.core.image_util as image_util

#pgl.gis
from pgl.gis.obtian import Amap

# this example
from . import IRequestTexture
from ... import TileIndex

class LocalRasterTileRequest(IRequestTexture):
    def __init__(self, data_base_path:str=None):
        self._data_base_path = None
        self.cursor = None

        if data_base_path is not None:
            self.set_data_base(data_base_path)

    def set_data_base(self, data_base_path):
        # it's import that only connect the database once
        # and keep only one cursor!
        self._data_base_path = data_base_path
        connection = sqlite3.connect(cls.__database)
        self.cursor = connection.cursor()

    def request_texture(self, tile_index:TileIndex, on_complete_callback:Callable):
        x,y,z = tile_index 
        query = 'SELECT tile_data FROM tiles WHERE ' \
                   + f'zoom_level == {z} ' \
                   + f'AND tile_column == {x} '\
                   + f'AND tile_row == {y};'
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        if len(result)>0 and len(result[0])>0:
            texture = result[0][0]
            on_complete_callback(texture)
        on_complete_callback(None)

