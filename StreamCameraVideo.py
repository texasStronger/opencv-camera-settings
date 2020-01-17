# import the necessary packages
from threading import Thread
import cv2
import time
import datetime
import logging
from CameraSettings import CameraSettings
from CameraMemory import CameraMemory

"""
Implement a camera based video stream.  
Tested on Raspberry Pi 3B, 3B+, 4, Windows 10 Thinkpad T570, and two logitech USB cams.

"""

class StreamCameraVideo(): #--------------------------------

    def __init__(self, camera_name='0', camera_settings=None, camera_memory=None):

        self.logger = logging.getLogger(__name__)
        self.logger.info(__name__)
        self.stream = cv2.VideoCapture(int(camera_name))     # setup stream
        self.camera_memory = CameraMemory(camera_memory) # remember memory type and camera settings
        self.camera_settings = CameraSettings(self.stream,camera_settings)
        self.starttime = 0 # keep track of some metrics
        self.stoptime = 0
        self.stopped = True
        self.frame_count = 1
        self.width=640
        self.height=480
        self.read_fps = 30.0

        if self.stream.isOpened() == False:
            self.logger.error("couldn't open camera:"+ camera_name)
            self.camera_memory.write((-2,None,""))
        return  
    
    def config(self, params):
        # params is dict like: {'camera_type': 'camera', 'camera_name': '0', 'camera_memory': ['deque', ' 100', '1'], 
        # 'camera_settings': [['CAP_PROP_AUTO_EXPOSURE', '.75']], 'read_fps': 30.0, 'width': 1280, 'height': 720}
        if params == None:
            return
        self.camera_type = params['camera_type']
        self.camera_name = int(params['camera_name'])
        self.camera_memory = None
        self.camera_memory = CameraMemory(camera_memory=params['camera_memory'])
        self.camera_settings = None
        cs = params['camera_settings']
        self.camera_settings = CameraSettings(self.stream,camera_settings=params['camera_settings'])
        self.read_fps = float(params['read_fps'])
        self.width = int(params['width'])
        self.height = int(params['height'])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
        self.stream.set(cv2.CAP_PROP_FPS,self.read_fps)
        return
        
    
    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name='StreamCameraVideo', args=())
        t.daemon = True
        self.starttime = time.time()
        t.start()
        time.sleep(1)
        return self 

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        time.sleep(0.2)
        self.stream.release()
        return 

    def update(self):
        self.stopped = False
        # Loop
        while True:
            if self.stopped:
                break
            (ret, self.frame) = self.stream.read()
            if not ret:
                self.camera_memory.write((-1,self.frame, ""))
                break 
            # always store frame number and timestamp with frame as Tuple (,,)
            timestamp = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")+".%07d"%self.frame_count
            self.camera_memory.write((self.frame_count,self.frame,timestamp))
            self.frame_count += 1

        # stopped
        self.stoptime = time.time()

    def read(self):
        # return the frame most recently read from memory
        return self.camera_memory.read()
        

    def settings(self,camera_settings=None):
        res = self.camera_settings.settings(camera_settings)
        #time.sleep(0.1)
        return res

    def memory(self,camera_memory=None):
        res = self.camera_memory.memory(camera_memory)
        #time.sleep(0.1)
        return res
    
    def stats(self):
        duration = self.stoptime-self.starttime
        fps = self.frame_count/duration
        return 'stats:%s, duration:%f, frame_count:%d, FPS:%.2f' % (__name__,duration,self.frame_count,fps)
    
    
# Test -------------------------------------
def main():
    cv2.namedWindow("TestStreamCameraVideo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TestStreamCameraVideo", 1280,720)
    cv2.moveWindow("TestStreamCameraVideo", 100,100)
    # read from a camera
    camera_memory = ['frame', 1]
    #camera_settings = [["CAP_PROP_AUTO_EXPOSURE", .75],['CAP_PROP_BRIGHTNESS',250.0]]
    camera_settings = [["CAP_PROP_FRAME_WIDTH", 1280],[cv2.CAP_PROP_FRAME_HEIGHT,720]]
    camera = StreamCameraVideo(0,camera_settings, camera_memory)
    camera.start()
    i=0
    previous = -3
    while True: 
        (num, frame,timestamp) = camera.read()   
        if num == 0: 
            continue
        if previous==num:
            time.sleep(0.02)
            continue
        previous = num
        if num == -1: # finished
            break

        cv2.imshow("TestStreamCameraVideo",frame)
        print(timestamp)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        i += 1
    camera.stop()

    cv2.destroyAllWindows()
    print(camera.stats())
    print("main read ",i)
    

if __name__ == '__main__':
    main() 
    
    