# -*- coding: utf-8 -*-

import cv2
import os

def get_face(img, conf_threshold = 0.6):
    fp = os.path.split(__file__)[0]

    # 获取图片长宽
    fh = img.shape[0]
    fw = img.shape[1]

    # 加载模型
    modelFile = fp+'/model/Caffe/res10_300x300_ssd_iter_140000_fp16.caffemodel'
    configFile = fp+'/model/Caffe/deploy.prototxt'
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

    # 获取人脸位置
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104.0, 117.0, 123.0], False, False)
    net.setInput(blob)
    detections = net.forward()
    facial_position = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= conf_threshold:
            x1 = int(detections[0, 0, i, 3] * fw)
            y1 = int(detections[0, 0, i, 4] * fh)
            x2 = int(detections[0, 0, i, 5] * fw)
            y2 = int(detections[0, 0, i, 6] * fh)
            facial_position.append([x1, y1, x2 - x1, y2 - y1])

    return facial_position

def mosaic(img, facial_position, pixel_width=25):
    # 获取图片长宽
    fh = img.shape[0]
    fw = img.shape[1]

    # 打马赛克
    for x, y, w, h in facial_position:
        if (y + h > fh) or (x + w > fw):
            pass
        else:
            for i in range(0, h - pixel_width, pixel_width):
                for j in range(0, w - pixel_width, pixel_width):
                    rect = [j + x, i + y, pixel_width, pixel_width]
                    color = img[i + y][j + x].tolist()
                    left_up = (rect[0], rect[1])
                    right_down = (rect[0] + pixel_width - 1, rect[1] + pixel_width - 1)
                    cv2.rectangle(img, left_up, right_down, color, -1)

    return img

def add_mosaic(img, pixel_width=25, conf_threshold=0.6):
    return mosaic(img, get_face(img, conf_threshold), pixel_width)
