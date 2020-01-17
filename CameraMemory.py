#from multiprocessing import Queue
import queue
import collections
import logging


"""
CameraMemory:
 Setup the way the camera will store its frames and transmit its, either as a single frame, 
 in a queue, or in a deque.  Set max sizes and timeouts also. Each implementation
 stores information in 'frame' but by experience, it is best not to directly store
 an opencv frame alone. It is bettery to use, for example, a tuple (frame_number, frame).
 This allows testing of frame_number instead of checking frame for validity.
 An implementaiton can simply increment frame number for each update. Also, codes
 can be sent back in frame_count, such as 0 is quit, -1 is frame error, or any application
 value. Not, skip frames is not implemented.
 
     ("frame", n) - return frame, skip_frames every nth frame
     ("queue", size, block, n) - use queue size, block (0) or block time, and skip_frames every nth frame
     ("deque", size, n) - use overwriting deque size, skip_frames every nth frame

"""

class CameraMemory:
    
    FRAME = 'frame'
    QUEUE = 'queue'
    DEQUE = 'deque'

    def __init__(self, camera_memory=None): #-----------------
        self.logger = logging.getLogger(__name__)
        if camera_memory == None:
            camera_memory = 'frame, 1'
        self.camera_memory = camera_memory
        self.memory(camera_memory)
        return 
    
    def memory(self, camera_memory=None): #-----------------
        try:
            if camera_memory == None:
                return self.camera_memory
            if camera_memory[0] == CameraMemory.FRAME:
                self.memory_type = camera_memory[0]
                self.skip_frames = int(camera_memory[1])
                self.frame = None
                self.camera_memory = self.memory_type+", "+str(self.skip_frames)
            elif camera_memory[0] == CameraMemory.QUEUE:
                self.memory_type = camera_memory[0]
                self.size = int(camera_memory[1])
                self.block = camera_memory[2]
                self.timeout = camera_memory[3]
                self.skip_frames = camera_memory[4] 
                self.framequeue = queue.Queue(maxsize=self.size)
                self.camera_memory = self.memory_type+", "+str(self.size)+", "+str(self.block)+", "+str(self.timeout)+", "+str(self.skip_frames)
            elif camera_memory[0] == CameraMemory.DEQUE:
                self.memory_type = camera_memory[0]
                self.size = camera_memory[1]
                self.skip_frames = camera_memory[2] 
                self.framedeque = collections.deque(maxlen=self.size)
                self.camera_memory = self.memory_type+", "+str(self.size)+", "+ str(self.skip_frames)
            else: #  junk
                self.memory_type = CameraMemory.FRAME
                self.skip_frames = 1
                self.frame = None
                self.camera_memory = "%s %d" % (self.memory_type,self.skip_frames)
        except:
                self.memory_type = CameraMemory.FRAME
                self.skip_frames = 1
                self.frame = None
                self.camera_memory= "%s %d" % (self.memory_type,self.skip_frames)
                self.logger.warning(self.camera_memory+ " due to parameter error, default memory type frame used.")
        self.logger.info(self.camera_memory)


        return  self.camera_memory
          

    def read(self): #-----------------
        frame = (0, None, 0)
        if self.memory_type == CameraMemory.FRAME: #------------
            frame = self.frame

        elif self.memory_type == CameraMemory.QUEUE: #------------
            self.logger.debug(" read queue, size "+str(self.framequeue.qsize()))
            try: 
                frame = self.framequeue.get(self.block,self.timeout)
            except queue.Empty as e:
                self.logger.warning(" read queue empty, "+str(e))
                return (0,None,0)

        elif self.memory_type == self.DEQUE: #------------
            try:
                frame = self.framedeque.pop()
            except:
                self.logger.warning(" deque empty.")
                return (0,None,0)

        else:  #------------
            self.logger.error(" read error.")
            return (-1,None,0)
        return frame
        
        
        
    def write(self, frame): #-----------------
        if self.memory_type == CameraMemory.FRAME: #------------
            self.frame = frame

        elif self.memory_type == CameraMemory.QUEUE: #------------
            try: 
                self.framequeue.put(frame,self.block,self.timeout)
                self.logger.debug(" write queue, size "+str(self.framequeue.qsize()))
            except queue.Full as e:
                self.logger.debug(" queue full: "+str(e))

        elif self.memory_type == CameraMemory.DEQUE: #------------
            self.framedeque.appendleft(frame)

        else: # ---------------- 
            return False

        return True
    
    
#Tester
import numpy as np
if __name__ == '__main__':
    blob = np.zeros(shape=(500,500))
    cmem = CameraMemory([CameraMemory.FRAME, 1])
    print(cmem.name)
    cmem.write(blob)
    res = cmem.read()
    if np.array_equal(blob,res):
        print("equal")
    else: print ("not equal")
    
    cmem = CameraMemory([CameraMemory.QUEUE, 100, True, None, 1])
    print(cmem.name)
    cmem.write(blob)
    res = cmem.read()
    if np.array_equal(blob,res):
        print("equal")
    else: print ("not equal")

    cmem = CameraMemory([CameraMemory.DEQUE, 200, 1])
    print(cmem.name)
    cmem.write(blob)
    res = cmem.read()
    if np.array_equal(blob,res):
        print("equal")
    else: print ("not equal")

    TYPO=100
    cmem = CameraMemory([TYPO, 200, 1])
    cmem.write(blob)
    print(cmem.memory())
    res = cmem.read()
    if np.array_equal(blob,res):
        print("equal")
    else: print ("not equal")
