from Camera import Camera
import cv2
import time
import pprint
pp=pprint.PrettyPrinter(indent=4)
winname="TestCameraTypes"

camera_settings = [["CAP_PROP_AUTO_EXPOSURE",.75]]
def testFrameMemory() :
    print("testFrameMemory")
    # read from active local camera 0
    camera_memory = ['frame', 1]
    camera = Camera("camera",0,camera_settings=camera_settings,camera_memory=camera_memory)
    set = camera.settings()
    pp.pprint(set)
    pp.pprint(camera.memory())
    camera.start()
    while True: 
        (frame_number, frame,timestamp) = camera.read()   
        if frame_number < 1: continue
        cv2.imshow(winname,frame)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
    camera.stop()
    print(camera.stats())
    return

def testDequeMemory() :
    print("testDequeMemory")
    camera_memory = ["deque", 100,1]
    camera = Camera("camera",0,camera_settings=camera_settings,camera_memory=camera_memory)
    set = camera.settings(camera_settings)
    pp.pprint(set)
    pp.pprint(camera.memory())
    camera.start()
    while True: 
        (frame_number, frame) = camera.read()   
        if frame_number < 1: continue
        cv2.imshow(winname,frame)
        #time.sleep(0.01)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
    camera.stop()
    print(camera.stats())
    return

def testQueueMemory():
    print("testQueueMemory")
    camera_memory = ["queue", 100,True, .2, 1]
    camera = Camera("camera",0,camera_settings=camera_settings,camera_memory=camera_memory)
    set = camera.settings(camera_settings)
    pp.pprint(set)
    pp.pprint(camera.memory())
    camera.start()
    while True: 
        (frame_number, frame) = camera.read()   
        if frame_number < 1: continue
        cv2.imshow(winname,frame)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
    camera.stop()
    print(camera.stats())
    

def main():
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winname, 640,540)
    cv2.moveWindow(winname, 100,100)
    
    testFrameMemory()
    testDequeMemory()
    testQueueMemory()

    
  

if __name__ == '__main__':
    main() 
    
    