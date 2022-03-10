'''
Date: 2022-03-10 14:39:10
LastEditors: cvhadessun
LastEditTime: 2022-03-10 14:47:06
FilePath: /FLame2SMPLX/src/post_process.py
'''
import cv2

img = cv2.imread("../data/flame2smplx.png")

img =cv2.blur(img,(30,30))

cv2.imwrite('../data/blur.png',img)