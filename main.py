# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import cv2 as cv
import numpy as np
import sys
import math

# clear img size
img_size_x = 1024
img_size_y = 768
#
# drawing params]

f_range = math.pi

draw_size_x = int(img_size_x / 2)
draw_start_x = int((img_size_x - draw_size_x) / 2)
steps_x = draw_size_x * 4
draw_center_y = 0
shape_size = 11
max_shape_size = 20

slope_factor_y = 128
range_x_coeff = 256
window_name = "experiment"
trackbar_draw_x_value = "draw_size_x"
slope_factor_y_value = "slope_factor_y"
trackbar_draw_x_center_value = "draw_size_center_x"
trackbar_draw_y_center_value = "draw_size_center_y"
trackbar_p_size_value = "p_size"

img = np.zeros((img_size_y, img_size_x, 3), np.uint8)
prim_img = img

if img is None:
    sys.exit("Could not read the image.")

print(img.shape)


def draw_x_callback(*args):
    global draw_size_x
    draw_size_x = args[0]
    draw_shape()


def draw_x_center_callback(*args):
    global draw_start_x
    draw_start_x = args[0]
    draw_shape()


def slope_factor_y_callback(*args):
    global slope_factor_y
    slope_factor_y = args[0]
    draw_shape()


def draw_y_center_callback(*args):
    global draw_center_y
    draw_center_y = args[0]
    draw_shape()


def p_size_callback(*args):
    global shape_size
    shape_size = args[0] / 2
    draw_shape()


def draw_shape():
    img = np.copy(prim_img)
    step_size_xf = 2 * f_range / steps_x
    xf = -f_range
    for i in range(steps_x):
        y_c = draw_center_y + slope_factor_y * (abs(math.sin(xf)) + shape_size * math.exp(-xf ** 100) * math.cos(xf))
        y_good = min(img_size_y - 1, int(y_c))

        x_draw = draw_start_x + int((draw_size_x + xf * (draw_size_x - f_range) / f_range) / 2) - 1
        x_draw = min(img_size_x - 1, x_draw)
        y_draw = img_size_y - y_good - 1

        for j in range(img_size_y):
            if j > y_draw:
                img[j, x_draw, 0] = 255
                img[j, x_draw, 1] = 255
                img[j, x_draw, 2] = 255

        xf = xf + step_size_xf

    cv.imshow(window_name, img)


cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
cv.createTrackbar(trackbar_draw_x_value, window_name, draw_size_x, 4 * img_size_x, draw_x_callback)
cv.createTrackbar(slope_factor_y_value, window_name, slope_factor_y, 256, slope_factor_y_callback)
cv.createTrackbar(trackbar_draw_x_center_value, window_name, draw_start_x, img_size_x, draw_x_center_callback)
cv.createTrackbar(trackbar_draw_y_center_value, window_name, draw_center_y, img_size_x, draw_y_center_callback)
cv.createTrackbar(trackbar_p_size_value, window_name, shape_size, max_shape_size, p_size_callback)

# cv.imshow(window_name, img)
c = cv.waitKey(0)
