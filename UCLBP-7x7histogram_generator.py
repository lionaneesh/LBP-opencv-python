import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

def bilinear_interpolation(x, y, img):
    x1, y1 = int(x), int(y)
    x2, y2 = math.ceil(x), math.ceil(y)

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

def get_pixel_else_0(image, idx, idy):
    if idx < int(len(image)) - 1 and idy < len(image[0]):
        return image[idx,idy]
    else:
        return 0

def find_variations(pixel_values):
    prev = pixel_values[-1]
    t = 0
    for p in range(0, len(pixel_values)):
        cur = pixel_values[p]
        if cur != prev:
            t += 1
        prev = cur
    return t

def uniform_circular_lbp(img, P, R):
	variating_blocks = 0
	hist = {}
	for h in range(0, 256): # initialize the histogram
		hist[h] = 0 
	for x in range(0, len(img)):
		for y in range(0, len(img[0])):
			center = img[x,y]
			pixels = []
			for point in range(1, P + 1):
				r = x + R * math.cos(2 * math.pi * point / P)
				c = y - R * math.sin(2 * math.pi * point / P)
				if r < 0 or c < 0:
					pixels.append(0)
					continue            
				if int(r) == r:
					if int(c) != c:
						c1 = int(c)
						c2 = math.ceil(c)
						w1 = (c2 - c) / (c2 - c1)
						w2 = (c - c1) / (c2 - c1)
										
						pixels.append(int((w1 * get_pixel_else_0(img, int(r), int(c)) + \
									   w2 * get_pixel_else_0(img, int(r), math.ceil(c))) / (w1 + w2)))
					else:
						pixels.append(get_pixel_else_0(img, int(r), int(c)))
				elif int(c) == c:
					r1 = int(r)
					r2 = math.ceil(r)
					w1 = (r2 - r) / (r2 - r1)
					w2 = (r - r1) / (r2 - r1)                
					pixels.append((w1 * get_pixel_else_0(img, int(r), int(c)) + \
								   w2 * get_pixel_else_0(img, math.ceil(r), int(c))) / (w1 + w2))
				else:
					pixels.append(bilinear_interpolation(r, c, img))


			values = thresholded(center, pixels)
			variations = find_variations(values)
			if variations <= 2:
				res = 0
				variating_blocks += 1
				for a in range(0, len(values)):
					res += values[a] * (1 << a)
				if res > 255:
					res = 255
				hist[res] += 1

	return hist

img = cv2.imread('aneesh.jpeg', 0)
rows = len(img)
cols = len(img[0])
row_separator = rows / 7
col_spearator = cols / 7
print row_separator, col_spearator
hists = []
for a in range(1, 7 + 1):
	for b in range(1, 7 + 1):
		block = img[row_separator * (a - 1):row_separator * a, col_spearator * (b - 1):col_spearator * b]
		hists.append(uniform_circular_lbp(block, 8, 1))

print hists[0]