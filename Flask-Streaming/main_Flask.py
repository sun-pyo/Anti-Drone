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

#email_update_interval = 600 # sends an email only once in this time interval
#video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
#object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml") # an opencv classifier
# App Globals (do not edit)

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save_server", required=True,
    help="ip address of the save_server to which the client will connect")
args = parser.parse_args()

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'pi'
app.config['BASIC_AUTH_PASSWORD'] = 'pi'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0



@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')
        
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
    return redirect(url_for('static', filename='index.html'))


@app.route('/send_img/<string:cam>')
def send_img(cam):
    WebcamVideoStream.send_frame(cam, args.save_server)
    return '', 204

    
@app.route('/R/<string:cam>')
def R(cam):
    print(cam)
    WebcamVideoStream.move_Right(cam)
    return '', 204

@app.route('/L/<string:cam>')
def L(cam):
    WebcamVideoStream.move_Left(cam)
    return '', 204

@app.route('/U/<string:cam>')
def U(cam):
    WebcamVideoStream.move_Up(cam)
    return '', 204

@app.route('/D/<string:cam>')
def D(cam):
    WebcamVideoStream.move_Down(cam)
    return '', 204

@app.route('/C/<string:cam>')
def C(cam):
    WebcamVideoStream.move_Init(cam)
    return '', 204

@app.route('/mode_change')
def mode_change():
    print('Auto')
    WebcamVideoStream.AutoMode_Flag()
    return '', 204


if __name__ == '__main__':
    WebcamVideoStream().start()
    app.run(host='0.0.0.0', debug=False, threaded=True)

