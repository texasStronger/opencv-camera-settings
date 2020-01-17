import cv2
if __name__ == '__main__' :
    video = cv2.VideoCapture("c:\\devt\\python\\videos\\senorAndrew2.mp4");
# Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
    fps = video.get(cv2.CAP_PROP_FPS)
    print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : ",fps)
    video.release(); 
