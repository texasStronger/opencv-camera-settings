from StreamCameraVideo import StreamCameraVideo
from StreamFileVideo import StreamFileVideo
from StreamWebVideo import StreamWebVideo

import logging

"""
Camera is an abstract and  represents various implementations.  Real camera in 2019
can take pictures, take videos, play a screen show, play a video, transmit wireless, 
change the camera settings and change the camera memory.
Each implementation may do things a bit differently. 
"""
    

class Camera:
   
    def __init__(self, cam_type='camera', cam_name='0', camera_settings=None, camera_memory=None):

        self.logger = logging.getLogger(__name__)
        self.logger.info(__name__) 

        # create the camera and give it settings and memory
        if cam_type == "camera": 
            self.camera = StreamCameraVideo(cam_name, camera_settings, camera_memory) 
        elif cam_type == "file": 
            self.camera = StreamFileVideo(cam_name, camera_settings, camera_memory)
        elif cam_type == "web" : 
            self.camera = StreamWebVideo(cam_name, camera_settings, camera_memory)
        else:
            self.logger.error("invalid Camera information. Default ('frame',1)")
            self.camera = StreamCameraVideo(cam_name, camera_settings, camera_memory) 
        return
    
    def config(self, params):
        self.camera.config(params)

    def start(self):
        self.camera.start()
        return

    def read(self):
        return self.camera.read()

    def stop(self):
        self.camera.stop()
    
    def restart(self):
        self.camera.restart()
        return
    
    def memory(self,camera_memory=None):
        ret = self.camera.memory(camera_memory)
        return ret

    def settings(self,camera_settings=None):
        ret = self.camera.settings(camera_settings)
        return ret

    def stats(self):
        return self.camera.stats()
