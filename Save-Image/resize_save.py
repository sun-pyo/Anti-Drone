######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 9/28/19
# Description: 
# This program uses a TensorFlow Lite object detection model to perform object 
# detection on an image or a folder full of images. It draws boxes and scores 
# around the objects of interest in each image.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import time
import shutil
from threading import Thread
import imagezmq

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.6)
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')


def save_():
    args = parser.parse_args()

    MODEL_NAME = args.modeldir
    GRAPH_NAME = args.graph
    LABELMAP_NAME = args.labels
    min_conf_threshold = float(args.threshold)
    use_TPU = args.edgetpu

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
    imageHub = imagezmq.ImageHub('tcp://*:5001')

    # Define path to images and grab all image filenames


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
        print(PATH_TO_CKPT)
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

    # Loop over every image and perform detection
    while True:
        start_time = time.time()
        # Load image and resize to expected shape [1xHxWx3]
        tm = time.localtime(start_time)
        date = time.strftime('%Y-%m-%d-%I-%M-%S', tm)

        (_, CamName, image) = imageHub.recv_image()
        imageHub.send_reply(b'OK')
        imH, imW, _ = image.shape 
        image_resized = cv2.resize(image, (300, 300))

        input_data = np.expand_dims(image_resized, axis=0)
        print(np.shape(input_data))

        successfolder = os.path.join(CWD_PATH,CamName)
        os.makedirs(successfolder, exist_ok=True)

        filename2 = str(date) + '-' +str(CamName)
        filename = filename2 + '.jpg'
        print('---------------------------------start--------------------------------------------------')
        print('image file name',filename2)
        print('image file name',filename)
        
        
        
        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()
        
        num = []
        
        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
        #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
        ymin = []
        xmin = []
        ymax = []
        xmax = []
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin.append(int(max(1,(boxes[i][0] * imH))))
                xmin.append(int(max(1,(boxes[i][1] * imW))))
                ymax.append(int(min(imH,(boxes[i][2] * imH))))
                xmax.append(int(min(imW,(boxes[i][3] * imW))))
                
                print("xmin,ymin,xmax,ymax",xmin[i],ymin[i],xmax[i],ymax[i])
                

                if scores[i] > 0.5:
                    num.append(scores[i])
        
        
        if len(num) == 0:
            print('fail------------------')
            
        if len(num) !=0:
            print(len(num))
            print('success')
            f = open(successfolder+'\\'+filename2+".xml", 'w')
            f.write('<annotation>\n\t<folder>'+successfolder+'</folder>\n')
            f.write('\t<filename>'+filename+'</filename>\n<path>'+filename2+'.jpg</path>\n')
            f.write('\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n')
            f.write('\t<size>\n\t\t<width>300</width>\n\t\t<height>300</height>\n')
            f.write('\t\t<depth>3</depth>\n\t</size>\n\t<segmented>0</segmented>\n')
            for i in range(len(num)):
                f.write('\t<object>\n\t\t<name>Drone</name>\n\t\t<pose>Unspecified</pose>\n')
                f.write('\t\t<truncated>0</truncated>\n\t\t<difficult>0</difficult>\n')
                f.write('\t\t<bndbox>\n\t\t\t<xmin>'+str(xmin[i])+'</xmin>\n')
                f.write('\t\t\t<ymin>'+str(ymin[i])+'</ymin>\n')
                f.write('\t\t\t<xmax>'+str(xmax[i])+'</xmax>\n')
                f.write('\t\t\t<ymax>'+str(ymax[i])+'</ymax>\n')
                f.write('\t\t</bndbox>\n\t</object>\n')
            f.write('</annotation>')
            f.close()
            print('createXML')

        cv2.imwrite(successfolder+'/'+filename, image_resized)
        end_time = time.time()
        process_time = end_time - start_time
        print("======== A frame took {:.3f} seconds=================".format(process_time))
        print('Choose Success Or Fail')



if __name__ == '__main__':
    print('start')
    t = Thread(target=save_, args=())
    t.daemon = True
    t.start()
    while True:
        frame = np.ones((250,300,3))
        cv2.putText(frame, "Exit with Esc key", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
        cv2.imshow('CAM_Window', frame)
        
        k = cv2.waitKey(0)
        if(k == 27):  # exit
            print('all end')
            exit()