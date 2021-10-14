import cv2
import sys
#from mail import sendEmail
from flask import Flask, render_template, Response
from flask_basicauth import BasicAuth
import itertools
from flask import redirect, request, url_for
import time
import threading
import imagezmq
import numpy as np
from imutils import build_montages
from datetime import datetime
import imutils
from webcamvideostream import WebcamVideoStream
import argparse

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save_server", required=False,
    help="ip address of the save_server to which the client will connect",default=0)
args = parser.parse_args()


WebcamVideoStream.set_address(args.save_server)

app = Flask(__name__)
last_epoch = 0



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

        
def cam(cam_index):
    while True:
        frame = WebcamVideoStream.get_frame('cam'+str(cam_index))
        ret, jpeg = cv2.imencode('.jpg',frame)
        if jpeg is not None:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/video_feed/<int:idx>')
def video_feed(idx):
    return Response(cam(idx),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def radar():
    while True:
        radar_frame = WebcamVideoStream.Radar_map()
        ret, jpeg = cv2.imencode('.jpg',radar_frame)
        if jpeg is not None:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/Radar_map')
def Radar_map():
    return Response(radar(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/drone_num')
def drone_num():
    rpi_name_list = ['cam1','cam2','cam3','cam4','cam5']
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                    yield "data: %s: %d, %s: %d, %s: %d, %s: %d\n\n" % (rpi_name_list[0], WebcamVideoStream.get_dnum(rpi_name_list[0]),
                                                                    rpi_name_list[1], WebcamVideoStream.get_dnum(rpi_name_list[1]),
                                                                    rpi_name_list[2], WebcamVideoStream.get_dnum(rpi_name_list[2]),
                                                                    rpi_name_list[3], WebcamVideoStream.get_dnum(rpi_name_list[3]))
                    time.sleep(.1)  # an artificial delay
        return Response(events(), content_type='text/event-stream')

if __name__ == '__main__':
    WebcamVideoStream().start()
    app.run(host='0.0.0.0', debug=False, threaded=True)

