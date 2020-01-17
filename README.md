# opencv-camera-settings
Test opencv cv2.CAP_PROP_ * settings on your camera

Run python TestOpenCVCameraSettings.py

This will turn on the camera and give you a prompt that allows experimenting with CAP_PROP* settings.  These CAP_PROP* settings available
on cameras varies and so does which values can be changed.  Have fun experimenting.   Older cameras can be picky.  This has been tested
with python 3.7 and opencv 3 and 4 on windows 10, mac pro and raspberry pi 3b+ and 4.

This was also a first experiment on abstracting the "camera memory" from the specific camera implementation.  
Memory can be a queue, deque, blocking, or just in time.

Check out Camera.py and run some Test programs.
