import ctypes
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np


class img_transClass():
    def __init__(self):
        self.dll = ctypes.cdll.LoadLibrary('my_cv.dll')

    def up_img_1(self,or_img,check_int_dir,scale_dir1,color_list):
        x, y = or_img.shape[0:2]
        x *= scale_dir1["缩放比例"].get() / 100.0
        y *= scale_dir1["缩放比例"].get() / 100.0
        dim = (int(y), int(x))
        resize = cv.resize(or_img, dim, interpolation=cv.INTER_AREA)

        mask = cv.Canny(resize, int(scale_dir1["边缘上限"].get()),
                        int(scale_dir1["边缘下限"].get()))
        
        gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
        temp = int(scale_dir1["阈值下限"].get())

        mask_ptr = mask.ctypes.data_as(ctypes.c_wchar_p)
        x, y = mask.shape
        arg_array = np.array(x * y, dtype=np.long)
        arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)

        if temp >= 255:
            ret, im_fixed = cv.threshold(gray, temp - 255, 255,
                                         cv.THRESH_BINARY)
        else:
            ret, im_fixed = cv.threshold(gray, temp, 255, cv.THRESH_BINARY)

        img = cv.cvtColor(im_fixed,cv.COLOR_GRAY2BGR)
        img_ptr = img.ctypes.data_as(ctypes.c_wchar_p)

        color_array = np.array(color_list,dtype=np.uint8)
        color_ptr = color_array.ctypes.data_as(ctypes.c_wchar_p)

        x, y,deep = img.shape
        arg_array = np.array([x * y,len(color_list)],dtype=np.long)
        arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)

        pix_array = np.zeros((x,y),dtype=np.uint8)
        pix_ptr = pix_array.ctypes.data_as(ctypes.c_wchar_p)
        
        self.dll.img_2pick(img_ptr, color_ptr, pix_ptr, arg_ptr)
        out_img = img
        return out_img,pix_array

    def up_img_2(self,or_img,check_int_dir,scale_dir2,color_list):
        x, y = or_img.shape[0:2]
        x *= scale_dir2["缩放比例"].get() / 100.0
        y *= scale_dir2["缩放比例"].get() / 100.0
        dim = (int(y), int(x))
        pix_array = np.zeros((int(x), int(y)), dtype=np.uint8)
        resize = cv.resize(or_img, dim, interpolation=cv.INTER_AREA)
        resize = cv.convertScaleAbs(resize,
                                    alpha=scale_dir2["亮度增益"].get()/50,
                                    beta =scale_dir2["亮度基准"].get()-50)
        arg_array = np.array(
            [dim[0] * dim[1], len(color_list)], dtype=np.long)  
        imgptr = resize.ctypes.data_as(ctypes.c_wchar_p)
        color_array = np.array(color_list,dtype=np.uint8)
        colorptr = color_array.ctypes.data_as(ctypes.c_wchar_p)
        arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)
        pix_ptr = pix_array.ctypes.data_as(ctypes.c_wchar_p)
        self.dll.img_closePick(imgptr, colorptr, pix_ptr, arg_ptr)
        resize = cv.cvtColor(resize,cv.COLOR_BGR2RGB) 
        return resize,pix_array


def show_tkimg(img,size,isBGR):
    x, y = img.shape[0:2]
    t = max(x, y)
    t = (size / t)
    x *= t
    y *= t
    dim = (int(y), int(x))
    resize = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    if isBGR == True:
        img_rgb = cv.cvtColor(resize, cv.COLOR_BGR2RGB)
    else:
        img_rgb = resize
    img = Image.fromarray(img_rgb)
    tkImage = ImageTk.PhotoImage(image=img)
    return tkImage