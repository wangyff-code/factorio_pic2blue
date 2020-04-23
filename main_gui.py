import copy
import csv
import ctypes
import json
import os
import threading
import tkinter as tk
import tkinter.messagebox
import webbrowser
from tkinter import filedialog, ttk

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
from trans_class import tras_blue

from gui_class import ctr_topClass,my_pross_class
from img_class import show_tkimg,img_transClass
import time
import copy

def github():
    webbrowser.open("https://github.com/wangyff-code/factorio_pic2blue", new=0)
    pass


class main_gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('图片转蓝图 V5.0')
        self.window.configure(background='#444444')
        self.window.overrideredirect(True)
        self.main_fram = tk.Frame(self.window,bg='#444444')
        self.img_trans=img_transClass()
        self.show_size = 400
        self.read_apartment()
        self.init_face()
        self.window.bind("<MouseWheel>", self.resize)
        self.main_fram.pack()
        self.window.mainloop()

    def resize(self,event):
        if event.delta > 0:
            if self.show_size <= 1000:
                self.show_size += 40
        else:
            if self.show_size > 50:
                self.show_size -= 40
        self.up_orimg()
        self.upShow_img()


    def read_apartment(self):
        f = open('ini.json', 'r')
        data = f.read()
        f.close()
        var_list = json.loads(data)
            
    def save_apartment(self):
        # f = open('ini.json', 'w')
        # text = json.dumps([0])
        # f.write(text)
        # f.close()
        self.window.destroy()


    def openfiles(self):
        s2fname = filedialog.askopenfilename(title='打开图片文件',
                                             filetypes=[('jpg', '*.jpg'),
                                                        ('All Files', '*')])
        self.or_img = cv.imdecode(np.fromfile(s2fname, dtype=np.uint8), -1)
        self.ctr_top.Check_board.press_check()
        self.up_orimg()
        self.upShow_img()


    def up_orimg(self):
        tkImage=show_tkimg(self.or_img,self.show_size,isBGR=True)
        self.label_img1.configure(image=tkImage)
        self.label_img1.image = tkImage

    def upShow_img(self, *arg):
        check_int_dir = self.ctr_top.Check_board.check_int_dir
        scale_dir1 = self.ctr_top.scal_board.scale_dir1
        scale_dir2 = self.ctr_top.scal_board.scale_dir2
        pix_array = []
        color_list = copy.deepcopy(self.ctr_top.Check_board.color_list)
        if len(color_list) == 0:
            x,y,deep = self.or_img.shape
            tkImage=show_tkimg(np.zeros((x,y,deep),dtype=np.uint8),self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage

        if len(color_list) == 1:
            color_list.append([255,255,255])
            img,pix_array=self.img_trans.up_img_1(self.or_img,check_int_dir,scale_dir1,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage
        if len(color_list) == 2:
            img,pix_array=self.img_trans.up_img_1(self.or_img,check_int_dir,scale_dir1,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage

        if len(color_list) > 2:
            img,pix_array=self.img_trans.up_img_2(self.or_img,check_int_dir,scale_dir2,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage

        self.pix_array = pix_array

    def start_go(self):
        t = threading.Thread(target=self.tras)
        t.setDaemon(True)
        t.start()

    def tras(self):
        pix_list = copy.deepcopy(self.ctr_top.Check_board.pix_list)
        pix_array = copy.deepcopy(self.pix_array)
        print(pix_list)
        print(pix_array)
        if len(pix_list) != 0:
            tras_blue(pix_list,pix_array,self.my_pross)
        else:
            pass
       


    def init_face(self):
        self.or_img = np.zeros((400, 400, 3),dtype=np.uint8)
        cv.putText(self.or_img, 'no image', (50, 200), cv.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)

        img = Image.fromarray(self.or_img)
        tkImage = ImageTk.PhotoImage(image=img)

        fm0 = tk.Frame(self.main_fram, bg='#333333',relief="groove",bd=4)
        com = tk.Button(fm0, text='打开图片', bg='#5EB663',
                     fg='#000000',command=self.openfiles)
        com.pack(side=tk.LEFT)


        com = tk.Button(fm0, text='关闭', bg='#B65663',
                     fg='#000000',command=self.save_apartment)
        com.pack(side=tk.RIGHT)

        com = tk.Button(fm0, text='窗口', bg='#BF7F00',
                     fg='#000000',command=self.small_sc)
        com.pack(side=tk.RIGHT)

        com = tk.Button(fm0, text='全屏', bg='#BF7F00',
                     fg='#000000',command=self.full_sc)
        com.pack(side=tk.RIGHT)



        fm0.pack(fill=tk.X,side=tk.TOP)


        fm0.bind("<ButtonPress-1>", self.StartMove)
        fm0.bind("<ButtonRelease-1>", self.StopMove)
        fm0.bind("<B1-Motion>", self.OnMotion)


        fm1 = tk.Frame(self.main_fram,bg='#444444')
        self.label_img1 = tk.Label(fm1, image=tkImage,bg='#444444')
        self.label_img1.pack(side=tk.LEFT)
        self.label_img2 = tk.Label(fm1, image=tkImage,bg='#444444')
        self.label_img2.pack(side=tk.LEFT)
        fm1.pack()

        self.ctr_board = tk.Frame(self.main_fram,borderwidth=2, bg='#444444',relief="groove",bd=4)
        self.ctr_top =ctr_topClass(self.ctr_board,self.upShow_img)
        self.ctr_board.pack()

        fm3 = tk.Frame(self.main_fram, bg='#444444')
        com = tk.Button(fm3, text='开始转换', bg='#5EB663',
                     fg='#000000',command=self.start_go)
        com.pack(side=tk.LEFT)

        self.my_pross = my_pross_class(fm3,self.img_trans.dll,20,1000)

        fm3.pack(side=tk.BOTTOM)
        com = tk.Button(self.main_fram, text='支持一下，点击进入github(试试鼠标滚轮缩放？)', bg='#444444',
                     fg='#FFFFFF',command=github)
        com.pack(side=tk.BOTTOM)
        self.up_orimg()
        self.upShow_img()
    
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry("+%s+%s" % (x, y))


    def full_sc(self):
        self.window.state("zoomed")


    def small_sc(self):
        self.window.state('normal')



gui = main_gui()
