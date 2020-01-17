# import the necessary packages
from threading import Thread
import cv2
import time
import logging
from CameraSettings import CameraSettings
from CameraMemory import CameraMemory

"""
Implement a File based video stream.  
Note: for some reason, reading / writing OPENCV cv2.CAP_PROPS* gives an error using
Python 3.7 and OpenCV 4.1.  For now, don't support settings.

This works with *.mp4 files.  But does not appear to work with IMG%2d.jpg image patterns 
on windows 10.

"""


class StreamFileVideo: #---------------

    def __init__(self, file_name, camera_settings, camera_memory):

        self.name = "StreamFileVideo:%s" % (file_name)
        self.logger = logging.getLogger(__name__)
        self.file_cam = cv2.VideoCapture(file_name)      # setup stream
        time.sleep(0.2)


        self.camera_settings = CameraSettings(self.file_cam,camera_settings)
        self.camera_memory = CameraMemory(camera_memory) # remember memory type and camera settings

        self.starttime = 0 # keep track of some metrics
        self.stoptime = 0
        self.stopped = True

        self.frame_count = 0
        if self.file_cam.isOpened() == False:
            self.logger.error(self.name+" couldn't open file:"+ file_name)
            self.camera_memory.write((-2,None))
        return  

    
    
    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        self.starttime = time.time()
        t.start()
        time.sleep(0.2)
        return self

    def update(self):
        # keep looping infinitely
        self.stopped = False
        # Loop
        while True:
            if self.stopped:
                break
            (ret, self.frame) = self.file_cam.read()
            if not ret:
                self.frame = None
                self.camera_memory.write((-1,None))
                break
            # always store frame number with frame as Tuple (,)
            self.frame_count += 1
            self.camera_memory.write((self.frame_count,self.frame))

        # stopped
        self.stoptime = time.time()

    def read(self):
        # return the frame most recently read
        return self.camera_memory.read()

    def stats(self):
        duration = self.stoptime-self.starttime
        fps = self.frame_count/duration
        return {"duration":round(duration,2), "frame_count":self.frame_count,"FPS":round(fps,2)}
        

    def settings(self,camera_settings=None):
        ret = self.camera_settings.settings(camera_settings)
        time.sleep(0.1)
        return ret

    def memory(self,camera_memory=None):
        ret = self.camera_memory.memory(camera_memory)
        time.sleep(0.1)
        return ret

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        time.sleep(0.2)
        self.file_cam.release() 
        
        
# Test ---------------------------------------------
def main():
    cv2.namedWindow("TestStreamFileVideo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TestStreamFileVideo", 640,540)
    cv2.moveWindow("TestStreamFileVideo", 100,100)
    # read from a file
    camera_memory = ['queue',10,True,None,1]
    camera_settings = [["CAP_PROP_BRIGHTNESS",199.0]]
    filecamera = StreamFileVideo("c:\\devt\\python\\videos\\senorAndrew2.mp4",camera_settings,camera_memory)
    filecamera.start()
    i=0
    while True: 
        (num, frame) = filecamera.read()   
        if num == 0: 
            continue
        if num == -1: # finished
            break
        if num == -2: # internal error
            break

        cv2.imshow("TestStreamFileVideo",frame)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        i += 1
    filecamera.stop()

    cv2.destroyAllWindows()
    print(filecamera.stats())
    print("main read ",i)
    

if __name__ == '__main__':
    main() 
    
            
