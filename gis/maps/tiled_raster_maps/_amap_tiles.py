# python std
from typing import Callable
from threading import Thread, Lock
import time

# pangolin framwork
from pangolin.server_application.texture_library import TextureLibrary
from pangolin.core.delegate import Delegate
import pangolin.core.image_util as image_util

#pgl.gis
from pgl.gis.obtian import Amap

# this example
from . import IRequestTexture
from ... import TileIndex

class AmapRasterTileRequest(IRequestTexture):
    def __init__(self):
        # amap访问有限制，如果同时访问的线程太多会被拒绝访问
        # 错误信息为："Max retries exceeded with url: /appmaptile?styl=..."
        # 所以self.thread_count 用来记录现有线程 
        self.thread_count = 0
        self.max_threads = 20
        self.lock = Lock()
        
    def request_texture(self, tile_index:TileIndex, on_complete_callback:Callable):
        thread = Thread(target = self._request_texture_async, args=[tile_index, on_complete_callback])
        thread.start()

    def _request_texture_async(self, tile_index:TileIndex, on_complete_callback:Callable):
        # 先看看同时有多少线程在访问amap，如果多于控制的量就先等等
        while self.thread_count > self.max_threads:
            time.sleep(0.01)

        # 在开始访问amap前先记录一下多了个线程在访问
        with self.lock:
            self.thread_count += 1

        try:
            response = Amap.tile_by_xylevel(*tile_index)
        except:
            print('- connection exceeded limit at thread_count=',self.thread_count)
            response = None

        if response is not None and response != '':
            img_64 = image_util.read_response_as_b64(response)
            on_complete_callback(img_64)
        else:
            on_complete_callback(None)

        # 结束访问amap后记住记录少一线程在访问amap，
        # 否则其他等待thread_count永远无法开始访问
        with self.lock:
            self.thread_count -= 1

