#Final Teachable Machines code, Kenneth Siu with help from Alex Krakower
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import requests
import json
import numpy as np
from rclpy.qos import ReliabilityPolicy, QoSProfile
import re
import ast
from builtin_interfaces.msg import Duration
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import cv2 as cv
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("/home/tuftsrobot/TEACHABLE MACHINES PROJECT/keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
#camera = cv2.VideoCapture(0)
camera = Picamera2()
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous}) # sets auto focus mode
camera.start() # activates camera
time.sleep(1) # wait to give camera time to start up



def Teachablemachines():
    img_name = 'image.jpg'
    camera.capture_file(img_name)
    image = cv2.imread("image.jpg")
    cv2.imshow('img',image)

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)


    # Show the image in a window
    #cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    variablez = str(class_name[2:]).strip()
    variable = ''.join(variablez)
    confidenceinterval = str(np.round(confidence_score * 100))[:-2]
    print(variable)
    print(confidenceinterval)
    Confidence1 = int(confidenceinterval)
    return Confidence1, variable

def Left():
        global S
        global T
        S = 0.0
        T = 1
        return S, T

def Right():
    global S
    global T
    S = 0.0
    T = -1
    return S, T

def Straight():
    global S
    global T
    S = 0.1
    T = 0
    return S, T

#def Fun():
 #   S = 0.01
  #  T = 0
   # return S, T

class Direction():
    def __init__(self):
        print("wff")

class TwistNode(Node):
    def __init__(self):
        super().__init__('twist_node')
        print('Creating publisher')
        self.cp = Direction()
        self.twist_node = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.twist = Twist()
        print("A")


    def timer_callback(self):
        [Confidence1, variable] = Teachablemachines()
            #self.twist = Twist()
        Confidence = int(Confidence1)
        current_time = self.get_clock().now()
        if variable == "Maze":
            if Confidence > 1:
                [S,T] = Straight()
        if Confidence > 95:
            if variable == "Bear":
                [S,T] = Left()
            elif variable =="Cube":
                [S,T] = Left()
            elif variable =="Elephant":
                [S,T] = Left()
            elif variable =="Kiwi":
                [S,T] = Left()
            elif variable =="Mario":
                [S,T] = Left()
            elif variable =="Mug":
                [S,T] = Left()
            elif variable =="Tractor":
                [S,T] = Right()
        else:
            [S,T] = Straight()
        
        if S != 0.1:
            for num in range(950):
                self.twist.linear.x = float(S)
                self.twist.angular.z = float(T)
                self.twist_node.publish(self.twist)
        else: 
            self.twist.linear.x = float(S)
            self.twist.angular.z = float(T)
            self.twist_node.publish(self.twist)
        #if S == 0.01:
         #   for num in range(200):
          #      self.twist.linear.x = float(0)
           #     self.twist.angular.z = float(1)
            #    for num in range(200):
             #       self.twist.linear.x = float(0)
              #      self.twist.angular.z = float(-1)
               #     for num in range(200):
                #        self.twist.linear.x = float(0)
                 #       self.twist.angular.z = float(1)
                  #      for num in range(200):
                   #         self.twist.linear.x = float(0)
                    #        self.twist.angular.z = float(-1)
                     #       for num in range(200):
                      #          self.twist.linear.x = float(0)
                       #         self.twist.angular.z = float(1)
     

def main(args=None):
    rclpy.init(args=args)

    twist_node = TwistNode()

    '''
    The node is "spun" so the callbacks can be called.
    '''
    print('Callbacks are called')
    while True:
        try:
            rclpy.spin_once(twist_node)
            print("Done")  # Destroy the node explicitly
        except KeyboardInterrupt:
            print('\nCaught Keyboard Interrupt')
            twist_node.destroy_node()
            print('shutting down')
            rclpy.shutdown()
            
           

if __name__ == '__main__':
    main()

