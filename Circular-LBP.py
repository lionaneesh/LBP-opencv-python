import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx,idy]
    except IndexError:
        return default


img = cv2.imread('C:\Users\sam\Downloads\lena.BMP', 0)
transformed_img = cv2.imread('C:\Users\sam\Downloads\lena.BMP', 0)

P = 10 # number of pixels
R = 5 # radius 

for x in range(0, len(img)):
    for y in range(0, len(img[0])):
        center        = img[x,y]
        pixels = []
        for point in range(1, P + 1):
            r = x + R * math.cos(2 * math.pi * point / P)
            c = y - R * math.cos(2 * math.pi * point / P)
            pixels.append(get_pixel_else_0(img, int(r), int(c))) # XXX: fix this!

        values = thresholded(center, pixels)
        res = 0
        for a in range(0, len(values)):
            res += values[a] * 255 / P

        transformed_img.itemset((x,y), res)

cv2.imshow('image', img)
cv2.imshow('thresholded image', transformed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
