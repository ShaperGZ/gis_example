from typing import Callable
import threading
from pangolin.geometry import Vector3
from pgl.gis.utility import Transfer, Tools

from tile_texture_source import ITileTextureSource

class TileUnit:
    """ 
    Represents one tile unit in the model space; 
    A tilemap is composed of one or many tile units
    """

    def __init__(self, ref_geo_coord):
        """
        A Tile Unit should contain the minimal data that represents a tile in model space
        the texture should be loaded saparatly from the geometry
        """
        # geo data:
        self.zoom:int = None
        self.geo_coord:list[float,float] = ref_geo_coord
        self.ref_geo_coord:list[float,float] = None
        self.tile_index:list[int,int] = None
        #self.tile = None
        
        # model data:
        self.model_position:tuple = None
        self.model_size:float = None
        self.texture_name:str = None
   

        # event callback for async texture loading
        self.on_texture_loaded:Callable = None

    def load_texture(self, texture_source:ITileTextureSource):
        # this method can be called by injecting a texture_source in saparate thread
        # by a third party
        self.texture_name = texture_source.get_tile_texture_name(self.tile_index)
        if self.on_texture_loaded is not None and isinstance(self.on_texture_loaded, Callable):
            self.on_texture_loaded(self.texture_name)

    def format(self):
        t = 'TileUnit:\n'
        t += '    tile_index:',self.tile_inedx, '/n'
        t += '    model_position:', self.model_positioni, '/n'
        t += '    model_size:', self.model_size, '/n'
        t += '    texture_name:',self.texture_name, '/n'
    
    @staticmethod
    def create_by_arbitray_position(arbitray_position:list, zoom, city_center):
        """
        Create a TileUnit by arbirary model position
        params arbitray_position: list, represents position in model space(same as mercator)
        params zoom: int, zoom level
        params center_center: list[float] the lnglat equivalent of 0,0 in model space, such as [112.3321,32.220]
        return : TileUnit
        """
        lng,lat = Transfer.mercator_to_lnglat(arbitray_position,city_center)
        tile_index = Transfer.lnglat_to_tiles([lng,lat],zoom)
        return TileUnit.create_by_tile_index(tile_index, city_center)
    
    @staticmethod
    def create_by_tile_index(tile_index, city_center):
        x,y,z = tile_index
        zoom = z
        geo_coord = Transfer.tiles_to_lnglat([x,y],z)
        model_position = Transfer.lnglat_to_mercator(geo_coord,city_center)
        tile_unit = TileUnit(city_center)
        tile_unit.geo_coord = geo_coord
        tile_unit.tile_index = tile_index
        tile_unit.ref_geo_coord = city_center
        tile_unit.model_position = model_position
        tile_unit.model_size = TileUnit.get_size_by_zoom(zoom)
        # suggest .tiles_to_lnglat renamed to .tile_index_to_lnglat(tile_index:list[int])
        return tile_unit

    @staticmethod
    def get_size_by_zoom(zoom):
        # I think is wrong
        return 78271516 * 2 ** (- zoom - 1)
