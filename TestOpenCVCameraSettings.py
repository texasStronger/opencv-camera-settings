import cv2
import pprint
from Camera import Camera
import re
import time

pp=pprint.PrettyPrinter(indent=4)
winname="TestOpenCVCameraSettings"
video_output_path="./"
image_output_path="./"



def Prompt():
    print("Tests camera 0 and video writing properties. Enter:")
    print("g  - to show current camera property names, numeric name and value.")
    print("prop_id value - to change camera settings. e.g. 10 255")
    print("s - to display camera dialog (might work on windows 10.")
    print("v - to show video writer codecs")
    print("t - take picture to pictureN.jpg")
    print("r - record video for 900 frames to videoN.mp4")
    print("w - toggle camera resolution")
    print("p - to show these prompts.")
    print("- Enter ESC or q to quit.")
    return
    
def TestSettings():
    Prompt()
     
    dimensions= [[1280,720], [640,480]]
    w = dimensions[0][0]
    h = dimensions[0][1]
    cv2.namedWindow("TestOpenCVCameraSettings", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TestOpenCVCameraSettings", w,h)
    cv2.moveWindow("TestOpenCVCameraSettings", 100,100)
    
    camera_settings = [["CAP_PROP_AUTO_EXPOSURE",.75],["CAP_PROP_FRAME_WIDTH",w],["CAP_PROP_FRAME_HEIGHT",h]]
    camera_memory = ["frame",1]
    camera = Camera("camera",0,camera_settings=camera_settings,camera_memory=camera_memory)
    camera.start()
    settings = camera.settings()

    pp.pprint(settings)

    prop_numbers = [ p[1] for p in settings]
    strings = [ s[0] for s in settings]
    input_string = ''
    video_number = 1
    picture_number = 1
    video_frames = 0
    fvideo = None
    recording = False
    previous_frame_number = -3

    Prompt()

    while True: 
        (frame_number, frame, timestamp) = camera.read()   
        if previous_frame_number == frame_number:
            time.sleep(0.001)
            continue
        else: previous_frame_number = frame_number

        if frame_number <= 0: 
            break

        cv2.imshow(winname,frame)

        key = cv2.waitKey(1) & 0xFF 

        if recording:
            if video_frames < 200:
                fvideo.write(frame)
                print("writing video frame ",video_frames)
                video_frames += 1
            else:
                fvideo.release()
                video_frames=0
                video_number += 1
                recording = False
            continue
                
        if key == ord('r'):
            # start recording video
            fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
            videofile = video_output_path+"video"+str(video_number)+".mp4"
            fvideo = cv2.VideoWriter(videofile, fourcc, 30.0,(w,h), True)
            recording = True
        elif key == ord('v'):
            try:
                c = cv2.VideoWriter("none.mp4",-1,15,(1280,720))
                c.release()
            except:
                pass
            
        elif key == ord('q') or key == 27:
            # finished
            break
        
        elif key==ord('w'):
            # change camera and window resolutions
            w = (dimensions[0][0] + dimensions[1][0]) - w
            h = (dimensions[0][1] + dimensions[1][1]) - h
            cv2.resizeWindow("TestOpenCVCameraSettings", w,h)
            camera.stop()
            camera_settings = [[cv2.CAP_PROP_FRAME_WIDTH,w],[cv2.CAP_PROP_FRAME_HEIGHT,h]]
            camera = Camera("camera",0,camera_settings=camera_settings,camera_memory=camera_memory)
            camera.start()
            time.sleep(1)

        elif key==ord('g'):
            # show current camera settings
            pp.pprint(camera.settings())

        elif key==ord('p'):
            # show prompts
            Prompt()

        elif key==ord('t'):
            # take a picture
            cv2.imwrite(image_output_path+"picture"+str(picture_number)+".jpg",frame)
            picture_number += 1

        elif key==ord('s'):
            camera_settings = [["CAP_PROP_SETTINGS",-1.0]]
            camera.settings(camera_settings)

        elif key == 13:
            print(input_string)
            try: 
                current_settings = re.findall("\d+\.\d+|\d+",input_string)
                an_id = int(current_settings[0])
                current_value = float(current_settings[1])
                setting_string = strings[prop_numbers.index(an_id)]
                camera_settings = [[setting_string, current_value]]
                camera.settings(camera_settings)
            except:
                print("Could not parse and set ",input_string)
            input_string = ''
        elif key != 255:
            input_string += chr(key)

    camera.stop()
    print(camera.stats())
    return

def main():
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winname, 640,540)
    cv2.moveWindow(winname, 100,100)
    TestSettings()
    
if __name__ == '__main__':
    main() 
    
    
