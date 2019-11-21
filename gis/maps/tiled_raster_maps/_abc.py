from abc import ABC, abstractmethod
from typing import Callable
from pangolin.server_application.texture_library import TextureLibrary
from ... import TileIndex

@abstractmethod
class IRequestTexture(ABC):
    def request_texture(self, tile_index:TileIndex, on_complete_callback:Callable):
        pass

