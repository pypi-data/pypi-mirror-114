# -*- coding: utf-8 -*-

import cv2
import os

def add_mosaic(img, frame='CAFFE', pixel_width=20, conf_threshold = 0.6):
    fp = os.path.split(__file__)[0]

    # 获取图片长宽
    fh = img.shape[0]
    fw = img.shape[1]

    # 加载模型
    if frame == 'CAFFE':
        modelFile = fp+'/model/Caffe/res10_300x300_ssd_iter_140000_fp16.caffemodel'
        configFile = fp+'/model/Caffe/deploy.prototxt'
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    else:
        return img

    # 获取人脸位置
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104.0, 117.0, 123.0], False, False)
    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * fw)
            y1 = int(detections[0, 0, i, 4] * fh)
            x2 = int(detections[0, 0, i, 5] * fw)
            y2 = int(detections[0, 0, i, 6] * fh)
            w = x2 - x1
            h = y2 - y1
            x = x1
            y = y1

            # 打马赛克
            neighbor = pixel_width
            if (y + h > fh) or (x + w > fw):
                pass
            else:
                for i in range(0, h - neighbor, neighbor):
                    for j in range(0, w - neighbor, neighbor):
                        rect = [j + x, i + y, neighbor, neighbor]
                        color = img[i + y][j + x].tolist()
                        left_up = (rect[0], rect[1])
                        right_down = (rect[0] + neighbor - 1, rect[1] + neighbor - 1)
                        cv2.rectangle(img, left_up, right_down, color, -1)

    return img
