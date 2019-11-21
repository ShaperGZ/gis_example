

# python std
from typing import Callable
from threading import Thread, Lock
from functools import partial

# pangolin framwork
from pangolin.server_application.texture_library import TextureLibrary
from pangolin.core.delegate import Delegate
import pangolin.core.image_util as image_util

#pgl.gis
from pgl.gis.obtian import Amap

# this example
from . import IRequestTexture, LocalRasterTileRequest
from ... import TileIndex

class LocalAndWebRasterTileRequest(IRequestTexture):
    def __init__(self, data_base_path:str=None, ):
        """
        params data_base_path: the path to .mbtiles file
        """
        self.thread = None
        self.lock = Lock
        self.local_source = LocalRasterTileRequest()

        self._data_base_path = None
        self.cursor = None
        self._buffered_images:dict[TileIndex,str] = dict()
        self.web_request_texture = web_request_texture

        if data_base_path is not None:
            self.set_data_base(data_base_path)

    def set_data_base(self, data_base_path):
        self.local_source.set_data_base(data_base_path)

    def on_local_request_complete(self, tile_index, on_complete_callback, img_64):
        # 这个函数用来劫持on_complete_callback，如果本地获取不到就尝试网上获取
        # 本来on_complete_callback只要一个参数
        # 这里需要两个额外参数，在获取本地图片失败后再申请网络图片
        # 通过partial函数能够把这两个额外的参数预存并隐藏起来
        if img_64 is not None:
            on_complete_callback(img_64)
        elif self.web_request_texture is not None:
            self.web_request_texture.request_texture(tile_index, partial(self.on_web_request_complete, tile_index, on_complete_callback))
        else:
            on_complete_callback(None)

    def on_web_request_complete(self, tile_index, on_complete_callback, img_64):
        with self.lock:
            self._buffered_images[tile_index] = img_64
        on_complete_callback(img_64)

    def request_texture(self, tile_index:TileIndex, on_complete_callback:Callable):
        self.local_source.request_texture(tile_index, partial(self.on_local_request_complete, tile_index, on_complete_callback))
        on_complete_callback(texture)


