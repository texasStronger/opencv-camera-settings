from Camera import Camera
import cv2
import time
import pprint

pp=pprint.PrettyPrinter(indent=4)

winname="TestCameraTypes"

winname = "Tester"

def recordVideo(filename, w, h):
    # read from active local camera 0
    #camera_settings = [[cv2.CAP_PROP_AUTO_EXPOSURE", 1.0],[cv2.CAP_PROP_BRIGHTNESS", 250.0], [cv2.CAP_PROP_FRAME_WIDTH", w], [cv2.CAP_PROP_FRAME_HEIGHT", h]]
    camera_settings = [ [cv2.CAP_PROP_FRAME_WIDTH, w], [cv2.CAP_PROP_FRAME_HEIGHT, h]]
        
    camera_memory = [['frame',1]]
    camera = Camera("camera",0,camera_settings,camera_memory)
    camera.start()
    pp.pprint(camera.settings())
    i=0
    previous = -3;
    FPS = 30.0
    # should print out possible values
    fourcc = -1 # print to see found fourcc values, nice to know
    fvideo = cv2.VideoWriter(filename, fourcc, FPS,(int(w),int(h)), True)
    fvideo.release()

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    print('fourcc ',fourcc, ' hex ',hex(fourcc))
    fvideo = cv2.VideoWriter(filename, fourcc, FPS,(int(w),int(h)), True)
    
    while True: 
        (num, frame,timestamp) = camera.read()   
        if num < 0:
            break
        if num == previous:
            time.sleep(0.005)
            continue
        previous = num
        cv2.imshow("Tester",frame)
        fvideo.write(frame)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q') or key == 27:
            break
        i += 1
    camera.stop()
    fvideo.release()
    print(camera.stats())




def main():
    cv2.namedWindow("Tester", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tester", 640,480)
    cv2.moveWindow("Tester", 100,100)
    filename = "small.mp4"
    recordVideo(filename,640,480)
    cv2.resizeWindow("Tester", 1280,720)
    filename = "large.mp4"
    recordVideo(filename,1280,720)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main() 
    
    