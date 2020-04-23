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
from trans_class import gen_mat

from gui_class import ctr_topClass,my_pross_class
from img_class import show_tkimg,img_transClass



def github():
    webbrowser.open("https://github.com/wangyff-code/factorio_pic2blue", new=0)
    pass


class main_gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('图片转蓝图 V5.0')
        self.window.configure(background='#444444')
        self.main_fram = tk.Frame(self.window,bg='#444444')
        self.img_trans=img_transClass()
        self.show_size = 200
        self.gen_matClass = gen_mat()
        self.read_apartment()
        self.init_menu()
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

    def init_menu(self):
        menubar = tk.Menu(self.window)
        fmenu1 = tk.Menu(self.window)
        for item in ['打开']:
            fmenu1.add_command(label=item, command=lambda: self.openfiles())
        self.window['menu'] = fmenu1

    def read_apartment(self):
        f = open('ini.json', 'r')
        data = f.read()
        f.close()
        var_list = json.loads(data)
            
    def save_apartment(self):
        f = open('ini.json', 'w')
        text = json.dumps([0])
        f.write(text)
        f.close()
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

        color_list = self.ctr_top.Check_board.color_list
        if len(color_list) == 0:
            x,y,deep = self.or_img.shape
            tkImage=show_tkimg(np.zeros((x,y,deep),dtype=np.uint8),self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage

        if len(color_list) == 1:
            color_list.append([255,255,255])
            img=self.img_trans.up_img_1(self.or_img,check_int_dir,scale_dir1,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage
        if len(color_list) == 2:
            img=self.img_trans.up_img_1(self.or_img,check_int_dir,scale_dir1,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage

        if len(color_list) > 2:
            img=self.img_trans.up_img_2(self.or_img,check_int_dir,scale_dir2,color_list)
            tkImage=show_tkimg(img,self.show_size,isBGR=False)
            self.label_img2.configure(image=tkImage)
            self.label_img2.image = tkImage


    def start_go(self):
        for widget in self.ctr_board.winfo_children():
            widget.destroy()
        t = threading.Thread(target=self.tras)
        t.setDaemon(True)
        t.start()
        tkinter.messagebox.showinfo('提示', '正在转换，结果输出output.txt')

    def tras(self):
        self.gen_matClass.strat_trans()
        if self.picvar.get() != 3:
            self.init_board_type1()
        else:
            self.init_board_type2()


    def init_face(self):
        self.or_img = np.zeros((400, 400, 3),dtype=np.uint8)
        cv.putText(self.or_img, 'no image', (50, 200), cv.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)

        img = Image.fromarray(self.or_img)
        tkImage = ImageTk.PhotoImage(image=img)
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
    

gui = main_gui()
