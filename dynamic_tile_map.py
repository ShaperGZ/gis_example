import threading
from functools import partial
from pangolin.animation import Animator
from pangolin.core.states import State
from pangolin.core.state_button import StateButton
from pangolin.core.state_vector3 import StateVector3
from pangolin.server_application.app_object import AppObject
import pangolin.geometry.mesh_util as mutil
from pangolin.geometry import Vector3

from pgl.gis.utility import Transfer

from tile_unit import TileUnit
from gis.maps.tiled_raster_maps import AmapRasterTileRequest
from tween_camera import TweenCamera
#from tile_texture_source import ITileTextureSource

class TileUnitObject(AppObject):
    def __init__(self):
        super().__init__()
        self.tile_unit = None
        self.mesh.set(mutil.Plane(1,1,1))

    def set_tile_unit(self, tile_unit, texture_source=None):
        #pos = Vector3(*tile_unit.model_position)
        #size = Vector3(tile_unit.model_size,tile_unit.model_size,0)

        assert tile_unit.model_size is not None
        assert tile_unit.model_size > 0

        pos = tile_unit.model_position
        size = [tile_unit.model_size,tile_unit.model_size,1]
        # TODO: size doesnt match tile locations
        size[0] *= 1.02
        size[1] *= 0.935

        #pos = [pos[0] - (size[0]), pos[1] - (size[1]), 0]

        self.transform.set('translation', pos)
        self.target_size = Vector3(*size)
        self.transform.set('scale', size)

        self.tile_unit = tile_unit
        if texture_source is not None:
            tile_index = tile_unit.tile_index
            texture_source.get_tile_texture_name(tile_index, self.on_texture_loaded)

    def on_texture_loaded(self, texture_name):
        self.material.set_texture(f'diffuse', texture_name)


class DynamicTileMap(AppObject):
    def __init__(self, city_center, texture_source, camera):
        super().__init__()
        self.map_center = self.add_in_node('map_center',StateVector3('map_center',Vector3(0,0,0)))
        self.map_extend = self.add_in_node('extend',State('extend',5, min=2, max=20, step=1))
        self.zoom = self.add_in_node('zoom', State('zoom',18))

        # add some buttons to play with
        self.bt_provincial = self.add_in_node('Provincial',StateButton('Provincial',self.on_bt_provincial))
        self.bt_bay = self.add_in_node('Bay Area',StateButton('Bay Area',self.on_bt_bay))
        self.bt_district = self.add_in_node('District',StateButton('District',self.on_bt_district))
        self.bt_site = self.add_in_node('Site',StateButton('Site',self.on_bt_site))

        self.city_center = city_center
        self._loaded_tiles = {}
        self.texture_source = texture_source
        self.camera = camera
        print('added camera type=',type(camera))

        self.register_update([self.map_center, self.map_extend,self.zoom, camera], self.on_change)
        # register states outside this object requires add_pred
        self.add_pred(camera)

        self.current_container = AppObject()
        self.buffer_container = AppObject()
    
    def setup(self):
        self.add(self.current_container)
        self._loaded_tiles = dict()
        self.texture_source.texture_library_lock = self.scene.thread_lock

    def _map_center_follows_camera(self):
        target = self.camera.target_position.value
        # current y the target_position this is a bug in the engine
        # remember to fix it! (a,b,c) should be coverted to (a,-c,b)
        pos = Vector3(target.x, target.y, 0)
        self.map_center.set(pos)

    def on_change(self):
        self._map_center_follows_camera()
        self._generate_map(self.map_center.value, self.zoom.value, self.current_container)

    def _generate_map(self,
                      map_center_position:Vector3, # this is the position in model space
                      zoom:int,
                      container:AppObject # container to hold wach tile AppObject
                      ):
        x,y,z = map_center_position
        city_center = self.city_center
        lng,lat = Transfer.mercator_to_lnglat(map_center_position,city_center)
        tile_index = Transfer.lnglat_to_tiles([lng,lat],zoom)
       
        loaded_tiles = self._loaded_tiles

        # 1 get surrounding tiles
        to_be_created_indice = []
        x,y,z = tile_index
        x -= self.map_extend.value
        y -= self.map_extend.value
        width = self.map_extend.value * 2 + 1
        for i in range(width):
            for j in range(width):
                index = (x+i,y+j,z)
                to_be_created_indice.append(index)

        # 2 delete tiles that are not in the to_be_created_indice
        keys = list(loaded_tiles.keys())
        for index in keys:
            if index not in to_be_created_indice:
                obj = loaded_tiles.pop(index)
                #obj.animator_for_destroy.start()
                obj.delete()

        # 3 create tiles from to_be_created_indice
        for index in to_be_created_indice:
            if index not in loaded_tiles.keys():
                obj = TileUnitObject()
                self.add(obj)
                unit = TileUnit.create_by_tile_index(index, city_center)
                obj.set_tile_unit(unit, self.texture_source)
                container.add(obj)
                loaded_tiles[index] = obj

    def on_bt_provincial(self):
        self.zoom.set(10)
    
    def on_bt_bay(self):
        h=55000
        self.tween_camera(h,0,0.5,partial(self.on_tween_camera_complete,13,15))

    def on_bt_district(self):
        h=6000
        self.tween_camera(h,0,0.5,partial(self.on_tween_camera_complete,13,5))

    def on_bt_site(self):
        h=800
        self.tween_camera(h,1,1,partial(self.on_tween_camera_complete,18,5))

    def on_tween_camera_complete(self, zoom, extend):
            self.zoom.set(zoom)
            self.map_extend.set(extend)


    def tween_camera(self, height, xratio=0, yratio=0.5,on_complete_callback=None):
        x,y,z = list(self.map_center.value)

        cx = x + (height*xratio)
        cy = y + (height*yratio)
        cz = height 

        #campos = Vector3(cx,cz,cy)
        #target = Vector3(x,z,y)
        campos = Vector3(cx,cy,cz)
        target = Vector3(x,y,z)

        tc = TweenCamera(self.camera, campos, target)
        if on_complete_callback:
            tc.on_complete.add(on_complete_callback)
        tc.start()
