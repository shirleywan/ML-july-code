import numpy as np
import cv2

if __name__ == "__main__":
    pic = "F:/dataset/jfr_box/meiti/00000002.jpg"
    img = np.zeros((1600, 1200, 2), dtype="uint8")  # 3
    green = (0, 255, 0)  # 4
    cv2.rectangle(img, (502, 527), (744, 1109), green)  # 12
    cv2.imshow("Canvas", img)  # 13
    cv2.rectangle(img, (487, 524), (773, 1076), green)  # 12
    cv2.imshow("Canvas", img)  # 13





