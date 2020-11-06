#Firebase Version

import socket
import time
import numpy as np
import sys
import importlib.util
import argparse
from servodrive import ServoMotor
from datetime import datetime
from digital import Digital_Controller
#from imutils.video import VideoStream
import os
from videostream import VideoStream
import imagezmq
import cv2
import RPi.GPIO as GPIO
import termios
import contextlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from gpiozero import Buzzer



# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='800x600')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')
parser.add_argument("-s", "--server", required=True,
    help="ip address of the server to which the client will connect")

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold =0.5
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

cred = credentials.Certificate('drone-detection-js-firebase-adminsdk-4xh9r-3ba93b9ccd.json')
# Initialize the app with a service account, granting admin privileges

cred = credentials.Certificate('firestore-1add2-firebase-adminsdk-7vjg4-6c20413010.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'       

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    #print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5
s= ServoMotor()

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

dnum=0
time_appear_drone = 0
boxthickness = 3
linethickness = 2
Auto_flag = True
rectangule_color = (10, 255, 0)

No_Drone_Time = 2

num = []
ymin = []
xmin = []
ymax = []
xmax = []
Drone_data = []
pulse = []

buzzer = Buzzer(17)
buzzer.off()
laser = Digital_Controller(12)
led = Digital_Controller(23)

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args.server))
rpi_name = socket.gethostname() # 각 라즈베리파이의 hostname을 cam1 ~ cam4로 설정해둠 
picam = VideoStream(resolution=(imW,imH),framerate=30).start() # 영상 시작
#print(picam.read().shape)
time.sleep(1.0)  # allow camera sensor to warm up

frame1 = picam.read()
rows, cols, _ = frame1.shape

x_medium = int(cols / 2)
x_center = int(cols / 2)
y_medium = int(rows / 2)
y_center = int(rows / 2)
distance = 0
Last_time = datetime.now()
while True: 
  # Start timer (for calculating frame rate)
  t1 = cv2.getTickCount()
  frame1 = picam.read() # 영상의 한 장면씩 읽어옴 

  frame = frame1.copy()
  frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  frame_resized = cv2.resize(frame_rgb, (width, height))
  input_data = np.expand_dims(frame_resized, axis=0)

# Normalize pixel values if using a floating model (i.e. if model is non-quantized)
  if floating_model:
    input_data = (np.float32(input_data) - input_mean) / input_std

# Perform the actual detection by running the model with the image as input
  interpreter.set_tensor(input_details[0]['index'],input_data)
  interpreter.invoke()

  # Retrieve detection results
  boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
  classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
  scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
  
  for i in range(len(scores)):
    if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
      # 바운딩 박스의 좌표 좌측 상단, 우측 하단의 좌표
      ymin.append(int(max(1,(boxes[i][0] * imH))))   # 좌측 상단 y좌표
      xmin.append(int(max(1,(boxes[i][1] * imW))))   # 좌측 상단 x좌표
      ymax.append(int(min(imH,(boxes[i][2] * imH)))) # 우측 하단 y좌표
      xmax.append(int(min(imW,(boxes[i][3] * imW)))) # 우측 하단 x좌표
      num.append(str(scores[i]))
                
  if len(num) != 0:
    # 드론이 출현시 가장 높은 확률을 갖는 드론의 거리, 바운딩 박스 좌표
    most = num.index(max(num))
    lx = int(max(1,(boxes[most][1] * imW)))
    ly = int(max(1,(boxes[most][0] * imH)))
    lw = int(min(imW,(boxes[most][3] * imW)))
    lh = int(min(imH,(boxes[most][2] * imH)))
    x_medium = int((lx+lw)/2)
    y_medium = int((ly+lh)/2)
    Last_time = datetime.now()

   # if dnum != len(num):
   #     dnum = len(num)
   #     doc_ref_drone = db.collection(u'{}'.format(rpi_name)).document(u'sky')
   #     doc_ref_drone.set({
   #     u'Num_of_drone': len(num),
   #     u'Distance' : distance,
   #     u'date' : firestore.SERVER_TIMESTAMP, #date
   #     })

    D = lw-lx
    distance = round(((-(6/5)*D+268) / 100),2)
    if distance < 0:
       distance = 0.2

    # 자동모드일 경우 가장 확률이 높은 드론을 화면상 중앙으로 올 수 있게 모터 컨트롤 (드론 트래킹)
    if Auto_flag == True:
        if x_medium < x_center - 60:    # 좌우로 60은 중앙이라고 판단
            s.left()
        elif x_medium > x_center + 60:
            s.right()
        else :
            s.stop()
            
        if y_medium < y_center - 30:    # 상하로 30은 중앙이라고 판단 
            s.up()
        elif y_medium > y_center + 30:
            s.down()
    
  if len(num) == 0:
    distance = 0
    
   # if dnum != len(num):
   #     dnum = len(num)
   #     doc_ref_drone = db.collection(u'{}'.format(rpi_name)).document(u'sky')
   #     doc_ref_drone.set({
   #     u'Num_of_drone': len(num),
   #     u'Distance' : 0.0,
   #     u'date' : firestore.SERVER_TIMESTAMP, #date
   #     })

  # 현재 모터의 pulse 값
  
  if len(num) != 0:
      buzzer.on()
      laser.on()
      led.on()
  else:
      buzzer.off()
      laser.off()
      led.off()

  pulse.append(s.get_panpulse())
  pulse.append(s.get_tiltpulse())
  
  Drone_data.append(len(num)) # 출현 드론 수 
  Drone_data.append(ymin)     # 각각의 바운딩 박스 좌측 상단 y좌표
  Drone_data.append(xmin)     # 각각의 바운딩 박스 좌측 상단 x좌표
  Drone_data.append(ymax)     # 각각의 바운딩 박스 우측 하단 y좌표
  Drone_data.append(xmax)     # 각각의 바운딩 박스 우측 하단 x좌표
  Drone_data.append(num)      # 드론으로 예측되는 확률
  Drone_data.append(pulse)    # 모터들의 pulse값
  Drone_data.append(distance) # 드론일 확률이 가장 높은 드론과의 거리
  
   
  mes = sender.send_image(Drone_data, rpi_name, frame) 
  message = mes.decode()
  message = message.split(' ') # 공백을 기준으로 구분 
    
  Auto_flag = bool(message[0])

  if Auto_flag == False: # 수동모드
      if message[1] == 'R':
          s.right()
      elif message[1] == 'L':
          s.left()
      elif message[1] == 'U':
          s.up()
      elif message[1] == 'D':
          s.down()
      elif message[1] == 'C':
          s.reset()
  # 자동모드, 정해진 시간동안 드론이 없었을 경우 (2초) 
  elif Auto_flag == True and (datetime.now() - Last_time).seconds > No_Drone_Time:
      s.set_pulse(message[1], message[2])


  # Calculate framerate
  t2 = cv2.getTickCount()
  time1 = (t2-t1)/freq
  frame_rate_calc= 1/time1   
  
  num.clear()
  ymin.clear()
  xmin.clear()
  ymax.clear()
  xmax.clear()
  Drone_data.clear()
  pulse.clear()

  # Press 'q' to quit
  if cv2.waitKey(1) == ord('q'):
      break
