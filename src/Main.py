# coding=utf-8
import os
import json, time
import threading
import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QSizePolicy
from qt_thread_updater import get_updater
from src import config as co
from src.SLVR import SLVR


class Main:
    def __init__(self, MainGUI):
        self.MainGUI = MainGUI
        self.camera = None
        self.image = None
        self.ret = False
        self.start_camera = True
        self.model = SLVR(weights='./weights/model.pt', img_size=640, threshold=0.5)

    def img_cv_2_qt(self, img_cv):
        height, width, channel = img_cv.shape
        bytes_per_line = channel * width
        img_qt = QtGui.QImage(img_cv, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
        return QtGui.QPixmap.fromImage(img_qt)
    
    def auto_camera(self):
        self.camera = cv2.VideoCapture(co.CAMERA_DEVICE) 
        self.ret, frame = self.camera.read()
        self.start_camera = True
        while self.ret and self.start_camera:
            try:
                ret, frame = self.camera.read()
                if ret:
                    self.image = frame.copy()
                    get_updater().call_latest(self.MainGUI.label_Image.setPixmap, self.img_cv_2_qt(frame))
            except Exception as e:
                print("Bug: ", e)

    def capture_image(self):
        if self.image is not None and self.ret and self.start_camera:
            image = self.image.copy()
            # Call SLVR model
            self.close_camera()
            get_updater().call_latest(self.MainGUI.label_Image.setPixmap, self.img_cv_2_qt(image))
        else:
            self.MainGUI.MessageBox_signal.emit("Không tìm thấy Camera/Video !", "error")
    
    def manual_image(self, image_file):
        image = cv2.imread(image_file)
        # Call SLVR model

        get_updater().call_latest(self.MainGUI.label_Image.setPixmap, self.img_cv_2_qt(image))


    def close_camera(self):
        try:
            self.start_camera = False
            time.sleep(0.5)
            if self.ret:
                self.camera.release()
            self.camera = None
            self.ret = False
        except Exception as e:
                print("Bug: ", e)
