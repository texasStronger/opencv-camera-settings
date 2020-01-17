from Camera import Camera
import cv2

winname = "Tester"

def localCamera():
    # read from active local camera 0
    camera_settings = [["CAP_PROP_AUTOEXPOSURE",1.0]]
    camera_memory = [['deque',100,1]]
    camera = Camera("camera",0,camera_settings,camera_memory)
    camera.start()
    i=0
    while True: 
        (num, frame, timestamp) = camera.read()   
        if num == 0:
            continue
        cv2.imshow("Tester",frame)
        print("imwrite frame ",i)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        i += 1
    camera.stop()
    return



def localFile():
    # read from a local mp4 file
    camera_memory = ['queue',10,True,4,1]
    camera_camera_settings = [["CAP_PROP_BRIGHTNESS",199.0]]
    camera = Camera("file","c:\\devt\\python\\videos\\senorAndrew2.mp4",camera_camera_settings,camera_memory)
    camera.start()
    i=0
    while True: 
        frame_number, frame = camera.read()   
        if frame_number == 0: continue
        if frame_number == -1 : break
        cv2.imshow("Tester",frame)
        print("imwrite frame ",i)
        i+=1
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
    camera.stop() 
    print(camera.stats())
    return 

def remoteURL():
    # read from a url
    camera_memory = ['queue',100,True,None,1]

    camera = Camera("web","http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4",[],camera_memory=camera_memory)
    camera.start()
    i=0
    while True: 
        (frame_number, frame) = camera.read()   
        if frame_number == 0: continue
        if frame_number == -2 : break
        cv2.imshow(winname,frame)
        print("imwrite frame ",i)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        i += 1
    camera.stop()
    print(camera.stats())
    print("Tester read:",i)
    return 

def main():
    cv2.namedWindow("Tester", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tester", 640,540)
    cv2.moveWindow("Tester", 100,100)
    localCamera()
    #localFile()
    remoteURL()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main() 
    
    