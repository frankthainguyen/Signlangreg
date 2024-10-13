# Core AI model for Sign Language Video Recognition
import os
import cv2
import numpy as np

class SLVR(object):
    def __init__(self, weights: str, img_size: int, threshold: float):
        # self.model = 
        self.img_size = img_size
        self.threshold = threshold
        self.init_weights(weights)

    def init_weights(self, weights: str):
        pass

    def preprocessing(self, img_list):
        pass

    def predict(self, inputs):

        pass