from picamera2 import Picamera2 
import cv2 as cv 
import numpy as np
from libcamera import controls
import time

picam2 = Picamera2()

#configure the picamera
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode

picam2.start() #must start the camera before taking any images
time.sleep(1)

for i in range(50):
    picam2.capture_file('image{0:09d}.jpg'.format(i))
    time.sleep(3)

