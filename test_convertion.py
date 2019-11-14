
from tiles import AmapTileDataSource, BufferedTileTextureSource, TileUnit, TileUnitObject
import city_centers

from pangolin.server_application.texture_library import TextureLibrary
from pgl.gis.utility import Transfer, Tools
import pytest

def test_position():
    ref_coordinates = city_centers.GUANGZHOU
    zoom = 13
    tile_index = Transfer.lnglat_to_tiles(ref_coordinates, zoom)
    tile_coord = Transfer.tiles_to_lnglat(tile_index, zoom)

    test_index = Transfer.lnglat_to_tiles(tile_coord, zoom)
    assert tile_index == test_index


