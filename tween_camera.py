from threading import Thread, Lock
import time

from pangolin.server_application.camera import TargetCamera
from pangolin.core.delegate import Delegate

class Tween:
    def start(self):
        thread = Thread(target=self._main_loop)
        thread.start()

    def _main_loop(self):
        pass

class TweenVector3State(Tween):
    def __init__(self, state, trg_vector):
        pass

class TweenCamera(Tween):
    def __init__(self, camera:TargetCamera, trg_cam_pos, trg_trg_pos, speed=0.2):
        self.camera = camera
        self.trg_cam_pos = trg_cam_pos
        self.trg_trg_pos = trg_trg_pos
        self.speed = speed
        self.on_complete = Delegate()



    def _main_loop(self):
        threshold = 0.05
        interval = 0.05
        speed = self.speed
        init_vect_cam = self.trg_cam_pos - self.camera.transform.translation.value
        init_vect_trg = self.trg_trg_pos - self.camera.target_position.value
        init_cam_mag = init_vect_cam.magnitude()
        init_trg_trg = init_vect_trg.magnitude()

        self.camera.user_control = False
        while True and not self.camera.user_control:
            vect_cam = self.trg_cam_pos - self.camera.transform.translation.value
            vect_trg = self.trg_trg_pos - self.camera.target_position.value

            cam_dist = vect_cam.magnitude()
            trg_dist = vect_trg.magnitude()

            flag1 = False
            flag2 = False
            #vect_cam = None
            #vect_trg = None

            if cam_dist != 0:
                if cam_dist< init_cam_mag * threshold:
                    self.camera.transform.translation.set(self.trg_cam_pos)
                else:
                    cam_offset_mag = cam_dist * speed
                    vect_cam = vect_cam.unitize() * cam_offset_mag
                    flag1 = True

            if trg_dist != 0:
                if trg_dist< init_trg_mag * threshold:
                    self.camera.target_position.set(self.trg_trg_pos)
                else:
                    trg_offset_mag = cam_dist * speed
                    vect_trg = vect_trg.unitize() * trg_offset_mag
                    flag2 = True

            # lock here if provided in the future
            if flag1:
                self.camera.transform.translation.set(self.camera.transform.translation.value + vect_cam)
            if flag2:
                self.camera.target_position.set(self.camera.target_position.value + vect_trg)
            # end lock

            if not flag1 and not flag2:
                time.sleep(0.1)
                self.camera.user_control = True
                break

            time.sleep(interval)

        self.on_complete.execute()
