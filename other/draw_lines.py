#coding=utf-8
import numpy as np
import cv2
#在已有图片上划线

if __name__ == "__main__":
    pic = "F:/dataset/jfr_box/meiti/00000002.jpg"
    img = cv2.imread(pic)
    green = (0, 255, 0)  # 4
    cv2.rectangle(img, (502, 527), (744, 1109), (0,0,255),1)  # 12
    cv2.rectangle(img, (487, 524), (773, 1076), (255, 0, 0),1)  # 12
    cv2.imwrite("F:\\dataset\\jfr_box\\cat2.jpg", img)
