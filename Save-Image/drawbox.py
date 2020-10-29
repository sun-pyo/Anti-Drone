import pandas as pd
import argparse
import os
import glob
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--imgdir', help='Name of the folder containing images to perform detection on. Folder must contain only images.',
                    default=None)
parser.add_argument('--csv', help='Name of the folder containing images to perform detection on. Folder must contain only images.',)
args = parser.parse_args()


IM_DIR = args.imgdir
csvname = args.csv
CWD_PATH = os.getcwd()
PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_DIR)
    

data = pd.read_csv("./" + csvname + ".csv")
for i in range(len(data)):
    image = cv2.imread(PATH_TO_IMAGES + '/'+ data['filename'][i])
    cv2.rectangle(image, (data['xmin'][i],data['ymin'][i]), (data['xmax'][i],data['ymax'][i]), (10, 255, 0), 2)
    cv2.imshow('filename ', image)
    if cv2.waitKey(0) == ord('d'):
        print('next')

    if cv2.waitKey(0) == ord('q'):
        print('end')
        break
    
    