import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import time
import shutil
import imagezmq

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.9)
parser.add_argument('--savedir', help='Name of the xml folder containing images xml.',
                    default=save)

args = parser.parse_args()
min_conf_threshold = float(args.threshold)


SU_DIR = args.savedir
CWD_PATH = os.getcwd()
    
if SU_DIR:
    PATH_TO_SUCCESS = os.path.join(CWD_PATH,SU_DIR)
    successfolder = glob.glob(PATH_TO_SUCCESS)[0]


imageHub = imagezmq.ImageHub('tcp://*:5001')

while True:
    start_time = time.time()
    tm = time.localtime(start_time)
    date = time.strftime('%Y-%m-%d-%I-%M-%S', tm)

    (Drone_data, CamName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    # ex) 2020-08-20-2-40-cam1.jpg 와 같은 형식으로 저장
    filename2 = str(date) + '-' +str(CamName)
    filename = filename2 + '.jpg'
    print('---------------------------------start--------------------------------------------------')
    print('image file name',filename)
    print('image file name',filename2)

    cv2.imwrite(successfolder+'/'+filename,frame)

    scores = list(map(float, Drone_data[5])) # float형 리스트로 변환
    ymin = []
    xmin = []
    ymax = []
    xmax = []
    num = []

    # 드론일 확률이 정해진 임계점을 넘으면 xml파일에 추가하여 저장
    for i in range(len(scores)):
        if ((float(scores[i]) > min_conf_threshold) and (float(scores[i]) <= 1.0)):
            num.append(scores[i])
            ymin.append(Drone_data[1][i])
            xmin.append(Drone_data[2][i])
            ymax.append(Drone_data[3][i])
            xmax.append(Drone_data[4][i])    
        
    if len(num) !=0:
        print(len(num))
        print('success')
        f = open(successfolder+'\\'+filename2+".xml", 'w')
        #time.sleep(0.1)
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
        #time.sleep(0.1)
        f.close
        print('createXML')
    
    end_time = time.time()
    process_time = end_time - start_time
    print("======== A frame took {:.3f} seconds=================".format(process_time))

print('all end')




