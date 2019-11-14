from typing import Callable
import threading
from pangolin.animation import Animator
from pangolin.core.states import State
from pangolin.core.state_vector3 import StateVector3
from pangolin.server_application.app_object import AppObject
import pangolin.geometry.mesh_util as mutil
from pangolin.geometry import Vector3

from pgl.gis.utility import Transfer, Tools
from pgl.gis.obtian import MapUtil, Amap
from pgl.gis.classes import Tile

# imports associates with this example
import city_centers
from tile_data_source import ITileDataSource, AmapTileDataSource, LocalAndWebTileDataSource
from tile_texture_source import ITileTextureSource, BufferedTileTextureSource
from tile_unit import TileUnit
from dynamic_tile_map import TileUnitObject,DynamicTileMap
   


from pangolin.server_application.scene import Scene
class Scene(Scene):
    def setup(self):
        texture_library = self.texture_library
        # first hand data source
        tile_data_source = AmapTileDataSource()  
        #tile_data_source = LocalAndWebTileDataSource('/home/holonking/gis_data/amap.mbtiles')
        tile_texture_source = BufferedTileTextureSource(tile_data_source, texture_library)
        center = city_centers.GUANGZHOU
        camera = self.cameras['main']
        
        dynamic_map = DynamicTileMap(city_centers.GUANGZHOU, tile_texture_source, camera)
        self.add(dynamic_map)
