from pgl.gis.utility import Transfer, Tools
from pgl.gis.obtian import MapUtil, Amap
from pgl.gis.classes import Tile

class ITileDataSource:
    """ 
    这个类只提供了一个interface,就是通过tile index 提取Tile
    """
    def get_tile(self,index):
        """
        param index: tile index in form of (x,y,z)
        return: a Tile  
        """
        pass

class AmapTileDataSource(ITileDataSource):
    def get_tile(self,tile_index):
        x,y,z = tile_index
        img = Amap.tile_by_xylevel(x,y,z)
        tile = Tile(x, y, z, img.content)
        return tile

from pgl.gis.obtian.local_map import LocalMap 
class LocalAndWebTileDataSource(ITileDataSource):
    def __init__(self, data_base_path):
        LocalMap.set_database(data_base_path)
        # 数据库的界面应该提供实例，而不是通过classmethod调用！
        # 不要每次Transfer.amaptile_by_xyz时才连接数据库！！！！！！！！
        # 请从实例里获取单一个curosr！不要每次访问时生成cursor！！！！！

    def get_tile(self, tile_index):
        # copied from map_util.amaptile_by_xyz
        x, y, zoom = tile_index
        if LocalMap.get_tile(x, y, zoom) is None:
            pic = Amap.tile_by_xylevel(x, y, zoom)
            LocalMap.add_tile(x, y, zoom, pic)
        return LocalMap.get_tile(x, y, zoom)
