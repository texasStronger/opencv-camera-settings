import cv2
import logging
import time


"""
 For a given camera stream, determine which CAP_PROPS are supported, store, and
 allow the valid properties to be changed.
 camera_settings can be in two list forms:
 1) [[string, value], ...]  e.g. [ ["CAP_PROP_FRAME_WIDTH",1280], ["CAP_PROP_FRAME_HEIGHT",720] ]
 2) [[int, value], ...] e.g. [ [cv2.CAP_PROP_FRAME_WIDTH, 1280], [cv2.CAP_PROP_FRAME_HEIGHT,720] ]
 
 """

class CameraSettings: #---------------------------

    def __init__(self, cam, camera_settings=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info(__name__)
        self.camera_settings = None
        self.camera = cam
        self.getDefaults()
        if camera_settings != None:
            self.settings(camera_settings)


    def getDefaults(self):
        # determine which camera settings are supported and store setting in lists as:
        # [ ["PROP_NAME*", prop_number, prop_value], [etc... ] ]
        # e.g.[ [ CAP_PROP_BRIGHTNESS, 12, 250.0] ]
        new_settings = []
        # find list of possible property settings
        props = [p for p in dir(cv2) if 'CAP_PROP' in p]
        for prop_string in props:
            try:
                #If getting property doesn't return 0, it may be valid
                prop_number = getattr(cv2, prop_string)
                prop_value = self.camera.get(prop_number)
                if prop_value == 0.0: 
                    self.logger.info("get not supported: "+ prop_string)
                    continue
                #if setting property is not False, then it should be valid 
                ret = self.camera.set(prop_number,prop_value)
                if not ret:
                    self.logger.info("set not supported: "+ str(prop_string))
                    continue
                new_settings.append([prop_string, prop_number, prop_value])
                self.logger.info("prop supported "+str(prop_string))
            except:
                self.logger.info("prop not supported "+prop_string)
                continue
        self.camera_settings = new_settings
        time.sleep(3)
        return
    
    # change cam stream settings and return
    def settings(self, camera_settings=None):

        if self.camera_settings == None: self.getDefaults(self.camera)

        if camera_settings == None: return self.camera_settings

        prop_strings = [ p[0] for p in self.camera_settings]
        prop_ids = [ p[1] for p in self.camera_settings]
        for prop in camera_settings:
            try:
                # determine if form is string,val or int,val
                if isinstance(prop[0], int):
                    index = prop_ids.index((prop[0]))
                    prop_number = prop[0]
                else: 
                    index = prop_strings.index(str(prop[0]))
                    prop_number = self.camera_settings[index][1]

                prop_value = prop[1]
                self.camera.set(prop_number, prop_value)
                self.camera_settings[index][2] = prop_value
                self.logger.info("set "+str(self.camera_settings[index]))
            except:
                self.logger.info("can't set "+str(camera_settings))
                continue # keep going
        return self.camera_settings


#Tester
if __name__ == '__main__':
    import pprint
    pp=pprint.PrettyPrinter(indent=4)
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    set1 = [["CAP_PROP_BRIGHTNESS",200.0]]
    print("First ",set1)
    c = CameraSettings(cam, set1)
    pp.pprint(c)
    ret = c.settings()
    pp.pprint(ret)  

    set1 = [['CAP_PROP_FRAME_WIDTH', 1280]]
    print("Second ",set1)
    ret = c.settings(set1)
    pp.pprint(ret)
    
    set1 = [["CAP_PROP_BRIGHTNESS", 250.0]]
    print("Third ",set1)
    ret = c.settings(set1)
    pp.pprint(ret)

    set1 = [["CAP_PROP_FRAME_HEIGHT", 720]]
    print("Fourth ",set1)
    ret =c.settings(set1)
    pp.pprint(ret)
    
    set1 = [[cv2.CAP_PROP_FRAME_HEIGHT, 480]]
    print("Fifth ",set1)
    ret =c.settings(set1)
    pp.pprint(ret)

    set1 = [[cv2.CAP_PROP_FRAME_WIDTH, 640]]
    print("Sixth",set1)
    ret =c.settings(set1)
    pp.pprint(ret)
    
    cam.release()
