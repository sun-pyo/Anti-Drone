from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect
import sys, cv2, numpy, time

# 꾸며진 버튼 클래스 
class My_Button(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title, parent)

        self.color1 = QtGui.QColor(118, 144, 152)
        self.color2 = QtGui.QColor(77, 95, 102)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:21px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

