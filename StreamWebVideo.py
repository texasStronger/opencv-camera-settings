# import the necessary packages
from threading import Thread
import cv2
import time
from CameraMemory import CameraMemory
import logging

"""
Implement a URL based video stream.  
Note: for some reason, reading / writing OPENCV cv2.CAP_PROPS* gives an error using
Python 3.7 and OpenCV 4.1.  For now, don't support settings.

"""


class  StreamWebVideo: #----------------------

    def __init__(self, url, camera_settings,camera_memory):
        self.name = "StreamWebVideo:%s" % (url)
        self.logger = logging.getLogger(__name__)
        self.webcamera = cv2.VideoCapture(url)
        time.sleep(0.2)


        self.camera_memory = CameraMemory(camera_memory) 
        # do not mess with settings on web stream.  Causes many problems.
        # self.camera_settings =  CameraSettings(self.webcamera,camera_settings)

        self.starttime = 0
        self.stoptime = 0
        self.stopped = False 

        self.frame_count = 0
        if self.webcamera.isOpened() == False:
            self.logger.error(self.name+" couldn't open url :"+ url)
            self.camera_memory.write((-2,None))
       
    def settings(self,camera_settings=None):
        ret = self.camera_settings.settings(self.webcamera,camera_settings)
        time.sleep(0.1)
        return  ret

    def memory(self,camera_memory=None):
        ret = self.camera_memory.memory(camera_memory)
        time.sleep(0.1)
        return ret


    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        self.starttime = time.time()
        t.start()
        time.sleep(1)
        return self

    def update(self):
        self.stopped = False
        while True:
            if self.stopped:
                break
            (ret, frame) = self.webcamera.read()
            if not ret:
                self.camera_memory.write((-1,None))
                break 
            # always store frame number with frame as Tuple (,)
            self.frame_count += 1
            self.camera_memory.write((self.frame_count,frame))
       
        self.stoptime = time.time()
            

    def read(self):
        return self.camera_memory.read()
            
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        time.sleep(0.2)
        self.webcamera.release
        
    def stats(self):
        duration = self.stoptime-self.starttime
        fps = self.frame_count/duration
        return {"duration":round(duration,2), "frame_count":self.frame_count,"FPS":round(fps,2)}
    
    
# Test -------------------------------------
def main():
    cv2.namedWindow("TestStreamWebVideo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TestStreamWebVideo", 640,540)
    cv2.moveWindow("TestStreamWebVideo", 100,100)
    # read from a url
    camera_memory = ['queue',30,True,3,1]
    camera_settings = []
    webcamera = StreamWebVideo("http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4", camera_settings, camera_memory)
    webcamera.start()
    previous = -3
    i=0
    while True: 
        (num, frame) = webcamera.read()   
        if num == 0: 
            continue
        if previous==num:
            time.sleep(0.02)
            continue
        previous = num
        if num == -1: # finished
            break

        cv2.imshow("TestStreamWebVideo",frame)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        
        i += 1
    webcamera.stop()

    cv2.destroyAllWindows()
    print(webcamera.stats())
    print("main read ",i)

if __name__ == '__main__':
    main() 
    
    