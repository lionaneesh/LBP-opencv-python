import numpy as np
import cv2
from matplotlib import pyplot as plt

def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

img = cv2.imread('C:\Users\sam\Downloads\lena.BMP', 0)
transformed_img = cv2.imread('C:\Users\sam\Downloads\lena.BMP', 0)


for x in range(1, len(img) - 1, 1):
    for y in range(1, len(img[0]) - 1, 1):
        center        = img[x,y]
        top_left      = img[x-1, y-1]
        top_up        = img[x,   y-1]
        top_right     = img[x+1, y-1]
        right         = img[x+1, y  ]
        left          = img[x-1, y  ]
        bottom_left   = img[x-1, y+1]
        bottom_right  = img[x+1, y+1]
        bottom_down   = img[x+1, y  ]

        values = thresholded(center, [top_left, top_up, top_right,
                                      right, left, bottom_left, bottom_right, bottom_down])

        weights = [1, 2, 4, 8, 128, 64, 16, 32]
        res = 0
        for a in range(0, len(values)):
            res += weights[a] * values[a]

        transformed_img.itemset((x,y), res)

cv2.imshow('image', img)
cv2.imshow('thresholded image', transformed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
