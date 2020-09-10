from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, cv2, numpy, time
from webcamvideostream import WebcamVideoStream
from Button import My_Button
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save_server", required=False,
    help="ip address of the save_server to which the client will connect", default=0)
args = parser.parse_args()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.video_width = 600    # 4분할 영상 사이즈 width
        self.video_height = 450   # 4분할 영상 사이즈 height
        self.Window_width = 2000  # Window width
        self.Window_height = 1000 # Window height
        self.stream = WebcamVideoStream().start() # 영상 스트리밍 시작
        self.setWindowTitle("A.I. Anti-Drone Security Feed")
        self.resize(self.Window_width, self.Window_height)
        self.setStyleSheet("background-color: #F5F5F5;") 
        self.initUI()

    def initUI(self):
        self.fps = 60
        self.timer = QTimer()
        self.timer.start(1000/self.fps)

        # 시간 표시 
        self.lbltime = QLabel("", self)
        self.lbltime.setFont(QFont("Segoe UI Black, 9",25))
        self.lbltime.setAlignment(Qt.AlignCenter)
        self.lbltime.resize(500,50)
        self.lbltime.move(self.video_width*2 +50, 10)

        # All Button
        self.btn_on = My_Button("All", self)
        self.btn_on.resize(100, 50)
        self.btn_on.move(5, 30 + self.video_height*2)
        self.btn_on.clicked.connect(self.start_all)

        self.imgList = []
        self.frameList = []  
        self.lb_dnumList = []
        self.btn_camList = []

        self.create_frame()
        self.create_btnCam()

        self.frameList[0].move(5,5)
        self.frameList[1].move(15+self.video_width,5)
        self.frameList[2].move(5 ,15+self.video_height)
        self.frameList[3].move(15+self.video_width,15+self.video_height)

        self.btn_camList[0].clicked.connect(lambda : self.start_cam('cam1'))
        self.btn_camList[1].clicked.connect(lambda : self.start_cam('cam2'))
        self.btn_camList[2].clicked.connect(lambda : self.start_cam('cam3'))
        self.btn_camList[3].clicked.connect(lambda : self.start_cam('cam4'))


        self.btn_saveimg = My_Button("Save", self)
        self.btn_saveimg.resize(100, 50)
        self.btn_saveimg.move(5+110*5, 30 + self.video_height*2)
        self.btn_saveimg.setVisible(False)

        self.Big_frame = QLabel(self)
        self.Big_frame.resize(self.video_width*2+15, self.video_height*2+15)
        self.Big_frame.setScaledContents(True)
        self.Big_frame.move(5,5)
        self.Big_frame.setVisible(False)

        self.radar_frame = QLabel(self)
        self.radar_frame.resize(self.video_width, self.video_height)
        self.radar_frame.setScaledContents(True)
        self.radar_frame.move(25+self.video_width*2, 15+self.video_height)

        self.start_all()
        self.show()

    
    def create_btnCam(self):
        for i in range(4):
            # 각 카메라 버튼
            self.btn_camList.append(My_Button('Cam' + str(i+1),self))
            self.btn_camList[i].resize(100, 50) 
            self.btn_camList[i].move(5+110*(i+1), 30 + self.video_height*2)
            self.btn_camList[i].show()
            # 각 카메라 드론 수 표시
            self.lb_dnumList.append(QLabel('',self))
            self.lb_dnumList[i].setFont(QFont("Segoe UI Black, 9",15))
            self.lb_dnumList[i].setAlignment(Qt.AlignLeft)
            self.lb_dnumList[i].resize(350,50)
            self.lb_dnumList[i].move(self.video_width*2 + 50, 10+50*(i+2))
            self.lb_dnumList[i].show()
    
    # 영상 Label 생성
    def create_frame(self):
        for i in range(4):
            self.imgList.append(self.stream.get_frame('cam'+str(i+1)))
            self.frameList.append(QLabel(self))
            self.frameList[i].resize(self.video_width, self.video_height)
            self.frameList[i].setScaledContents(True)
    
    # 4분할 화면 송출
    def start_all(self):
        self.stop_Bigframe()   # 큰 화면 정지

        for i in range(4):     # 4분할 화면 보이게하기
            self.frameList[i].setVisible(True)
        
        try:                   # connect된 함수가 있으면 삭제
             self.timer.timeout.disconnect() 
        except Exception: pass

                               # 4분할 영상 송출하는 함수 connect
        self.timer.timeout.connect(self.nextFrameSlot)
        self.btn_saveimg.setVisible(False)  # Save button 숨기기

        try:                   
            self.btn_saveimg.disconnect() 
        except Exception: pass
    
    # 4분할 화면 끄기
    def stop_all(self):
        for i in range(4):
            self.frameList[i].setPixmap(QPixmap.fromImage(QImage()))
            self.frameList[i].setVisible(False)

    # 4분할 영상 송출
    def nextFrameSlot(self):
        for i in range(4):
            self.imgList[i] = cv2.cvtColor(self.stream.get_frame('cam'+str(i+1)),cv2.COLOR_BGR2RGB)
            qImg = QImage(self.imgList[i].data, self.imgList[i].shape[1], self.imgList[i].shape[0], self.imgList[i].shape[1]*self.imgList[i].shape[2], QImage.Format_RGB888)
            self.frameList[i].setPixmap(QPixmap.fromImage(qImg))        

        img = cv2.cvtColor(self.stream.Radar_map(), cv2.COLOR_BGR2RGB)
        qImg = QImage(img.data, img.shape[1], img.shape[0], img.shape[1]*img.shape[2], QImage.Format_RGB888)
        self.radar_frame.setPixmap(QPixmap.fromImage(qImg))
        
        self.set_text()

        
    # 큰 화면 송출
    def start_cam(self, cam):
        self.stop_all()         # 4분할 화면 정지
        self.Big_frame.setVisible(True) # 큰 화면 보이게하기
        try:                        # connect된 함수가 있으면 삭제
            self.timer.timeout.disconnect() 
        except Exception: 
            pass                    # 해당하는 cam 영상을 큰 화면에서 송출하는 함수 connect
        self.timer.timeout.connect(lambda : self.next_Bigframe(cam))
        self.btn_saveimg.setVisible(True)
        try:
             self.btn_saveimg.disconnect() 
        except Exception: 
            pass                    # 해당하는 cam 영상을 이미지 저장 서버로 전송하는 함수 connect
        self.btn_saveimg.clicked.connect(lambda : self.Save_img(cam))
    
    # 큰 화면 중단
    def stop_Bigframe(self):
        self.Big_frame.setPixmap(QPixmap.fromImage(QImage()))
        self.Big_frame.setVisible(False)

    # 큰 화면 영상 송출
    def next_Bigframe(self, cam):
        self.img = cv2.cvtColor(self.stream.get_frame(cam), cv2.COLOR_BGR2RGB)
        qImg = QImage(self.img.data, self.img.shape[1], self.img.shape[0], self.img.shape[1]*self.img.shape[2], QImage.Format_RGB888)
        self.Big_frame.setPixmap(QPixmap.fromImage(qImg))

        img = cv2.cvtColor(self.stream.Radar_map(), cv2.COLOR_BGR2RGB)
        qImg = QImage(img.data, img.shape[1], img.shape[0], img.shape[1]*img.shape[2], QImage.Format_RGB888)
        self.radar_frame.setPixmap(QPixmap.fromImage(qImg))

        self.set_text()
    
    # 우측 상단 text (시간, 드론 수)
    def set_text(self):
        # 시간 업데이트
        t = time.localtime()
        self.lbltime.setText("{}-{}-{} {}:{}:{}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
        
        dnum = []
        cam_list = ['cam1','cam2','cam3','cam4']

        for i in range(len(cam_list)):
            dnum.append(self.stream.get_dnum(cam_list[i]))
            # 드론이 출현한 화면, 글자 강조하기 위한 색변경 
            if dnum[i] > 0:
                self.lb_dnumList[i].setStyleSheet("Color: Red")  
                self.frameList[i].setStyleSheet(" border-style: solid; border-width: 8px; border-color: #00FF00;")
                self.lb_dnumList[i].setText("Cam{}: {}   distance{} : {}m".format((i+1), dnum[i], (i+1), self.stream.get_distance(cam_list[i])))  
            else:
                self.lb_dnumList[i].setStyleSheet("Color: Black")
                self.frameList[i].setStyleSheet(" border-style: solid; border-width: 8px; border-color: #F5F5F5;") 
                self.lb_dnumList[i].setText("Cam{}: {}   distance{} : 0m".format((i+1), dnum[i], (i+1)))
        
    # 이미지 저장 서버로 이미지 전송
    def Save_img(self, cam):
        if args.save_server != 0:
            self.stream.send_frame(cam, args.save_server)

    # 종료창 클릭 이벤트
    def closeEvent(self, QCloseEvent):    
        ans = QMessageBox.question(self, "종료 확인", "종료하시겠습니까",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) 
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
