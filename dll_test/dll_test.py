import ctypes
import cv2 as cv
import numpy as np
from fac_dir import item_color_dir

pick_list = [0,0,0,0,0,0,0,0,0,0,1,1,0]

color_list      = []
pick_numberList = []

for i in range(0,len(pick_list)):
    if pick_list[i] == 1:
        color_list.append(item_color_dir[i]['color'])
        pick_numberList.append(i)


dll = ctypes.cdll.LoadLibrary('my_cv.dll')
img = cv.imread('1.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, im_fixed = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
im_fixed = cv.cvtColor(im_fixed,cv.COLOR_GRAY2BGR)
x,y = gray.shape
pix_array = np.zeros((x,y),dtype=np.uint8)
arg_array = np.array([x*y,len(color_list)],dtype=np.long)
imgptr = im_fixed.ctypes.data_as(ctypes.c_wchar_p)
color_array = np.array(color_list,dtype=np.uint8)
colorptr = color_array.ctypes.data_as(ctypes.c_wchar_p)
arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)
pix_ptr = pix_array.ctypes.data_as(ctypes.c_wchar_p)
dll.img_2pick(imgptr, colorptr, pix_ptr, arg_ptr)
cv.imshow('0',im_fixed)
cv.waitKey(0)