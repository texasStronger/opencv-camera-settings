#!/usr/bin/env python
import cv2
import time
                                                  
def runit(num_frames,w,h):
    # Start default camera
    video = cv2.VideoCapture(0);
    fps = video.get(cv2.CAP_PROP_FPS)
    if w !=0:
        video.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : ",fps, " width ",w," height ",h)
    num_frames = 90
    print("Capturing ",num_frames," frames")
    # Start time
    start = time.time()
    for _ in range(0, num_frames) :
        _,_ = video.read()
    end = time.time()
    # Time elapsed
    seconds = end - start
    print ("Measured Time taken : ",seconds, " seconds")
    
    # Calculate frames per second
    fps  = num_frames / seconds;
    print ("Measured frames per second : ",fps); 
    # Release video
    video.release()
    return 

if __name__ == '__main__' :
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    print("opencv version ",major_ver, minor_ver, subminor_ver)
    runit(90, 640,480)
    runit(90,1280,720)