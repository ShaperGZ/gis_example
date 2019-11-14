from pangolin.server_application.app_object import AppObject
from pangolin.core.state_button import StateButton
from pangolin.server_application.scene import Scene
from pangolin.geometry.vector3 import Vector3
import pangolin.geometry.mesh_util as mutil

class FrameFollowCamera(AppObject):
    def setup(self):
        self.set_mesh(mutil.box())
        self.camera = None
        self.flyaway = self.add_in_node('flyaway',StateButton('flyaway',self.flyaway_callback))
        self.flyclose = self.add_in_node('flyclose',StateButton('flyclose',self.flyclose_callback))

    def set_scene(self, scene):
        super().set_scene(scene)
        camera = scene.cameras['main']
        self.camera = camera
        self.add_pred(self.camera)

    def _get_target_pos_on_ground(self):
        target = self.camera.target_position.value
        # current y the target_position this is a bug in the engine
        # remember to fix it! (a,b,c) should be coverted to (a,-c,b)
        pos = Vector3(target.x, -target.z, 0)
        return pos

    def _update(self):
        if self.camera in self._stale_sources:
            pos = self._get_target_pos_on_ground()
            self.transform.set('translation',pos)

    def flyaway_callback(self):
        print('flying away')
        pos = self._get_target_pos_on_ground()
        campos = Vector3(pos.x,pos.y,pos.z + 200)
        self.scene.tween_camera(campos=list(campos),trgpos=list(pos))

    def flyclose_callback(self):
        print('flying near')
        f=10
        pos = self._get_target_pos_on_ground()
        campos = Vector3(pos.x+f, pos.y+f, pos.z+f)
        self.scene.tween_camera(campos=list(campos),trgpos=list(pos))


class Scene(Scene):
    def setup(self):
        ffc = FrameFollowCamera()
        self.add(ffc)
        
