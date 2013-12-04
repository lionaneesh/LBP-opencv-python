import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

def bilinear_interpolation(x, y, img):
    x1, y1 = int(r), int(c)
    x2, y2 = math.ceil(r), math.ceil(c)

    r1 = (x2 - x) / (x2 - x1) * get_pixel_else_0(img, x1, y1) + (x - x1) / (x2 - x1) * get_pixel_else_0(img, x2, y1)
    r2 = (x2 - x) / (x2 - x1) * get_pixel_else_0(img, x1, y2) + (x - x1) / (x2 - x1) * get_pixel_else_0(img, x2, y2)

    return (y2 - y) / (y2 - y1) * r1 + (y - y1) / (y2 - y1) * r2    

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

P = 5 # number of pixels
R = 20 # radius 

for x in range(0, len(img)):
    for y in range(0, len(img[0])):
        center        = img[x,y]
        pixels = []
        for point in range(1, P + 1):
            r = x + R * math.cos(2 * math.pi * point / P)
            c = y - R * math.cos(2 * math.pi * point / P)
            if r < 0 or c < 0:
                pixels.append(0)
                continue
            # XXX: We shouldn't just average if the point lies between just 2 pixels.
            if int(r) == r:
                if int(c) != c:
                    c1 = int(c)
                    c2 = math.ceil(c)
                    w1 = (c2 - c) / (c2 - c1)
                    w2 = (c - c1) / (c2 - c1)
                    
                    pixels.append((w1 * get_pixel_else_0(img, r, int(c), img) + \
                                   w2 * get_pixel_else_0(img, r, math.ceil(c), img)) / (w1 + w2))
                else:
                    pixels.append(get_pixel_else_0(img, int(r), int(c)))
            elif int(c) == c:
                r1 = int(r)
                r2 = math.ceil(r)
                w1 = (r2 - r) / (r2 - r1)
                w2 = (r - r1) / (r2 - r1)                
                pixels.append((w1 * get_pixel_else_0(img, int(r), int(c), img) + \
                               w2 * get_pixel_else_0(img, math.ceil(r), int(c), img)) / (w1 + w2))
            else:
                pixels.append(bilinear_interpolation(r, c, img))

                
        values = thresholded(center, pixels)
        res = 0
        for a in range(0, len(values)):
            res += values[a] * 255 / P

        transformed_img.itemset((x,y), res)

cv2.imshow('image', img)
cv2.imshow('thresholded image', transformed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
