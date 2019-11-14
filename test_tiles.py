from tiles import AmapTileDataSource, BufferedTileTextureSource, TileUnit, TileUnitObject
import city_centers

from pangolin.server_application.texture_library import TextureLibrary
from pgl.gis.utility import Transfer, Tools
import pytest


@pytest.fixture
def sample_tile():
    arbitray_position = [3,4]
    zoom = 15
    tile = TileUnit.create_by_arbitray_position(arbitray_position, zoom, city_centers.GUANGZHOU)
    return tile

def test_arbitray_position_to_tile_position(sample_tile):
    tile = sample_tile
    print('tile.model_position',tile.model_position)
    print('tile.model_size',tile.model_size)
    print('tile.tile_index',tile.tile_index)

def test_load_texture(sample_tile):
    tile_data_source = AmapTileDataSource()
    texture_library= TextureLibrary()
    tile_texture_source = BufferedTileTextureSource(tile_data_source, texture_library)

    tile = sample_tile
    tile.load_texture(tile_texture_source)
    print(tile.texture_name)
    assert tile.texture_name in texture_library.data.keys()
    #print(texture_library.data[tile.texture_name])

def test_tile_unit_creation():
    zoom = 17
    o1 = TileUnit.create_by_arbitray_position([2,3], zoom, city_centers.GUANGZHOU)
    model_position = o1.model_position
    tile_index = o1.tile_index

    o2 = TileUnit.create_by_tile_index(tile_index, city_centers.GUANGZHOU)
    assert o1.tile_index == o2.tile_index
    assert o1.model_position == o2.model_position

    x,y,z = tile_index
    next_x_tile_index = [x+1,y,z]
    o3 = TileUnit.create_by_tile_index(next_x_tile_index, city_centers.GUANGZHOU)
    xoffset = abs(o3.model_position[0] - o2.model_position[0])
    assert abs(xoffset - o3.model_size)<0.1

    next_y_tile_index = [x,y+1,z]
    o4 = TileUnit.create_by_tile_index(next_y_tile_index, city_centers.GUANGZHOU)
    yoffset = abs(o4.model_position[0] - o2.model_position[0])
    
    assert abs(xoffset - o4.model_size)<0.1
