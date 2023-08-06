import sys
import time

import cv2


def init_video(det=0):
    '''

    :param det:
        支持 = ['mp4', 'mov', 'avi', 'mkv']
        摄像头ID
        rtsp://192.168.1.156:554/ch1/1
    :return:
    '''
    # cap = cv2.VideoCapture(det, cv2.CAP_DSHOW)  # capture=cv2.VideoCapture("1.mp4")
    cap = cv2.VideoCapture(det)  # capture=cv2.VideoCapture("1.mp4")
    cap.set(cv2.CAP_PROP_FPS, 20)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap
