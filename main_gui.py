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
from trans_fun import gen_mat
from fac_dir import color_list

item_name = 0, ['stone-path']

item_dir = {
    "石砖": 'stone-path',
    "标准混凝土": 'concrete',
    "标准混凝土(标识)": 'hazard-concrete-left',
    "钢筋混凝土": 'refined-concrete',
    "钢筋混凝土(标识)": 'refined-hazard-concrete-left',
    "填海料": 'landfill'
}




def github():
    webbrowser.open("https://github.com/wangyff-code/factorio_pic2blue", new=0)
    pass


class main_gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('图片转蓝图 V5.0')
        self.gen_matClass = gen_mat()
        self.read_apartment()
        self.init_menu()
        self.init_face()
        self.window.protocol("WM_DELETE_WINDOW", self.save_apartment)
        self.window.mainloop()

    def init_menu(self):
        menubar = tk.Menu(self.window)
        fmenu1 = tk.Menu(self.window)
        for item in ['打开']:
            fmenu1.add_command(label=item, command=lambda: self.openfiles())
        fmenu2 = tk.Menu(self.window)
        for item in ['材质设置']:
            fmenu2.add_command(label=item, command=lambda: self.set_item())
        menubar.add_cascade(label="文件", menu=fmenu1)
        menubar.add_cascade(label="设置", menu=fmenu2)
        self.window['menu'] = menubar

    def read_apartment(self):
        self.picvar = tk.IntVar()
        self.alpha = tk.IntVar()
        self.beta = tk.IntVar()

        self.alpha.set(100)
        self.beta.set(0)

        self.picvar.set(0)
        self.init_apart_list = []
        for i in range(0, 6):
            a = tk.IntVar()
            self.init_apart_list.append(a)
        try:
            f = open('ini.json', 'r')
            data = f.read()
            f.close()
            var_list = json.loads(data)
            for i in range(0, 6):
                self.init_apart_list[i].set(var_list[i])
        except:
            for i in range(0, 6):
                self.init_apart_list[i].set(10)
            pass

        self.color_array = np.array(color_list, dtype=np.uint8)
        self.dll = ctypes.cdll.LoadLibrary('my_cv.dll')

    def save_apartment(self):
        var_list = []
        for i in self.init_apart_list:
            var_list.append(i.get())
        f = open('ini.json', 'w')
        text = json.dumps(var_list)
        f.write(text)
        f.close()
        self.window.destroy()

    def openfiles(self):
        s2fname = filedialog.askopenfilename(title='打开图片文件',
                                             filetypes=[('jpg', '*.jpg'),
                                                        ('All Files', '*')])
        self.or_img = cv.imdecode(np.fromfile(s2fname, dtype=np.uint8), -1)
        self.upall_img(0)

    def conf(self, win, number1, number2, number3, et):
        try:
            k = float(et.get())
        except:
            k = 1
        gen_type = self.picvar.get()
        item_list = [item_dir[number1.get()], item_dir[number2.get()]]
        self.gen_matClass.set_gen(gen_type, item_list, k, self.p1)
        for widget in self.ctr_board.winfo_children():
            widget.destroy()
        if self.picvar.get() != 3:
            self.init_board_type1()
        else:
            self.init_board_type2()
        self.upall_img(0)
        win.destroy()
    def show_tkimg(self, img):
        x, y = img.shape[0:2]
        t = max(x, y)
        t = (self.init_apart_list[0].get() / t)
        x *= t
        y *= t
        dim = (int(y), int(x))
        resize = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        img_rgb = cv.cvtColor(resize, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img_rgb)
        tkImage = ImageTk.PhotoImage(image=img)
        return tkImage

    def up_img_1(self):
        x, y = self.or_img.shape[0:2]
        x *= self.init_apart_list[1].get() / 100.0
        y *= self.init_apart_list[1].get() / 100.0
        dim = (int(y), int(x))
        resize = cv.resize(self.or_img, dim, interpolation=cv.INTER_AREA)
        if self.init_apart_list[5].get() != 0:
            img_GaussianBlur = cv.GaussianBlur(
                resize, (self.init_apart_list[5].get() * 2 + 1,
                         self.init_apart_list[5].get() * 2 + 1), 0)
        else:
            img_GaussianBlur = resize
        mask = cv.Canny(img_GaussianBlur, int(self.init_apart_list[3].get()),
                        int(self.init_apart_list[4].get()))
        gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
        temp = int(self.init_apart_list[2].get())
        mask_ptr = mask.ctypes.data_as(ctypes.c_wchar_p)
        x, y = mask.shape
        arg_array = np.array(x * y, dtype=np.long)
        arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)
        if temp >= 255:
            ret, im_fixed = cv.threshold(gray, temp - 255, 255,
                                         cv.THRESH_BINARY)
            img_ptr = im_fixed.ctypes.data_as(ctypes.c_wchar_p)
            self.dll.img_not(img_ptr, mask_ptr, arg_ptr)
            out_img = im_fixed
        else:
            ret, im_fixed = cv.threshold(gray, temp, 255, cv.THRESH_BINARY)
            img_ptr = im_fixed.ctypes.data_as(ctypes.c_wchar_p)
            self.dll.img_not(img_ptr, mask_ptr, arg_ptr)
            out_img = im_fixed
        self.gen_matClass.set_pix(out_img)
        return out_img

    def up_img_2(self):
        x, y = self.or_img.shape[0:2]
        x *= self.init_apart_list[1].get() / 100.0
        y *= self.init_apart_list[1].get() / 100.0
        dim = (int(y), int(x))
        pix_array = np.zeros((int(x), int(y)), dtype=np.uint8)
        resize = cv.resize(self.or_img, dim, interpolation=cv.INTER_AREA)
        resize = cv.convertScaleAbs(resize,
                                    alpha=self.alpha.get() / 100,
                                    beta=self.beta.get())
        arg_array = np.array(
            [dim[0] * dim[1], len(color_list)], dtype=np.long)
        imgptr = resize.ctypes.data_as(ctypes.c_wchar_p)
        colorptr = self.color_array.ctypes.data_as(ctypes.c_wchar_p)
        arg_ptr = arg_array.ctypes.data_as(ctypes.c_wchar_p)
        pix_ptr = pix_array.ctypes.data_as(ctypes.c_wchar_p)
        self.dll.img_closePick(imgptr, colorptr, pix_ptr, arg_ptr)
        self.gen_matClass.set_pix(pix_array)
        return resize

    def upall_img(self, v):
        if self.picvar.get() != 3:
            self.out_img = self.up_img_1()
        else:
            self.out_img = self.up_img_2()
        tkImage = self.show_tkimg(self.out_img)
        self.label_img2.configure(image=tkImage)
        self.label_img2.image = tkImage
        tkImage = self.show_tkimg(self.or_img)
        self.label_img1.configure(image=tkImage)
        self.label_img1.image = tkImage


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

    def set_item(self):
        win = tk.Toplevel()
        win.title("材质设置")
        f1 = tk.Frame(win)
        #--------------------------------------
        self.picvar = tk.IntVar()
        pic = tk.Radiobutton(f1, text="单材质", variable=self.picvar, value=0)
        pic.grid(row=0, column=0)
        pic.select()

        pic1 = tk.Radiobutton(f1, text="双材质", variable=self.picvar, value=1)
        pic1.grid(row=1, column=0)

        pic2 = tk.Radiobutton(f1, text="特殊材质", variable=self.picvar, value=2)
        pic2.grid(row=2, column=0)

        pic3 = tk.Radiobutton(f1, text="多颜色多材质", variable=self.picvar, value=3)
        pic3.grid(row=3, column=0)

        l = tk.Label(f1,
                     text="   材质1：",
                     bg="pink",
                     font=("Arial", 10),
                     width=15)
        l.grid(row=0, column=1)

        l = tk.Label(f1,
                     text="   材质1：",
                     bg="pink",
                     font=("Arial", 10),
                     width=15)
        l.grid(row=1, column=1)

        l = tk.Label(f1,
                     text="   特殊材质：",
                     bg="pink",
                     font=("Arial", 10),
                     width=15)
        l.grid(row=2, column=1)
        #--------------------------------------
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(f1,
                                     width=10,
                                     height=10,
                                     textvariable=number1)
        numberChosen1['values'] = ("石砖", "标准混凝土", "标准混凝土(标识)", "钢筋混凝土",
                                   "钢筋混凝土(标识)", "填海料")
        numberChosen1.current(0)
        numberChosen1.grid(row=0, column=2)

        numberChosen1 = ttk.Combobox(f1,
                                     width=10,
                                     height=10,
                                     textvariable=number1)
        numberChosen1['values'] = ("石砖", "标准混凝土", "标准混凝土(标识)", "钢筋混凝土",
                                   "钢筋混凝土(标识)", "填海料")
        numberChosen1.grid(row=1, column=2)

        number3 = tk.StringVar()
        number3.set("太阳能-电池")
        numberChosen1 = ttk.Combobox(f1,
                                     width=10,
                                     height=10,
                                     textvariable=number3)
        numberChosen1['values'] = ("太阳能-电池")
        numberChosen1.grid(row=2, column=2)

        l = tk.Label(f1,
                     text="   材质2：",
                     bg="pink",
                     font=("Arial", 10),
                     width=15)
        l.grid(row=1, column=3)

        l = tk.Label(f1,
                     text="   电池/太阳能 =",
                     bg="pink",
                     font=("Arial", 10),
                     width=15)
        l.grid(row=2, column=3)

        et = tk.Entry(f1)
        et.grid(row=2, column=4)
        et.insert(0, '1')
        number2 = tk.StringVar()
        numberChosen2 = ttk.Combobox(f1,
                                     width=10,
                                     height=10,
                                     textvariable=number2)
        numberChosen2['values'] = ("石砖", "标准混凝土", "标准混凝土(标识)", "钢筋混凝土",
                                   "钢筋混凝土(标识)", "填海料")
        numberChosen2.current(0)
        numberChosen2.grid(row=1, column=4)

        b1 = tk.Button(
            f1,
            text='确定',
            width=12,
            height=2,
            command=lambda: self.conf(win, number1, number2, number3, et))
        b1.grid(row=3, column=3)
        f1.pack()

    def init_face(self):
        self.or_img = np.zeros((300, 300, 3), dtype=np.uint8)
        img = Image.fromarray(self.or_img)
        tkImage = ImageTk.PhotoImage(image=img)
        fm1 = tk.Frame(self.window)
        self.label_img1 = tk.Label(fm1, image=tkImage)
        self.label_img1.pack(side=tk.LEFT)
        self.label_img2 = tk.Label(fm1, image=tkImage)
        self.label_img2.pack(side=tk.LEFT)
        v0 = self.init_apart_list[0]
        s1 = tk.Scale(fm1,
                      from_=100,
                      to=1000,
                      length=100,
                      variable=v0,
                      command=self.upall_img)
        s1.pack()
        fm1.pack(side=tk.TOP)

        self.ctr_board = tk.Frame(self.window)
        self.init_board_type1()
        self.ctr_board.pack()

        fm3 = tk.Frame(self.window)
        com = tk.Button(fm3, text='开始转换', command=self.start_go)
        com.pack(side=tk.LEFT)

        self.p1 = ttk.Progressbar(fm3,
                                  length=1000,
                                  mode="determinate",
                                  orient=tk.HORIZONTAL)
        self.p1.pack(side=tk.BOTTOM)
        self.p1["maximum"] = 100
        self.p1["value"] = 0

        fm3.pack(side=tk.BOTTOM)
        com = tk.Button(self.window, text='支持一下，点击进入github', command=github)
        com.pack(side=tk.BOTTOM)
        self.upall_img(0)
        gen_type = self.picvar.get()
        item_list = [item_dir["石砖"], item_dir["石砖"]]
        self.gen_matClass.set_gen(gen_type, item_list, 1, self.p1)

    def init_board_type1(self):
        f_1 = tk.Frame(self.ctr_board)
        l = tk.Label(f_1,
                     text="缩放比例",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v1 = self.init_apart_list[1]
        s1 = tk.Scale(f_1,
                      from_=1,
                      to=100,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v1,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_1.pack()

        f_2 = tk.Frame(self.ctr_board)
        l = tk.Label(f_2,
                     text="阈值下限",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v2 = self.init_apart_list[2]
        s1 = tk.Scale(f_2,
                      from_=0,
                      to=510,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v2,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_2.pack()

        f_3 = tk.Frame(self.ctr_board)
        l = tk.Label(f_3,
                     text="边缘上限",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v3 = self.init_apart_list[3]
        s1 = tk.Scale(f_3,
                      from_=0,
                      to=1000,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v3,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_3.pack()

        f_4 = tk.Frame(self.ctr_board)
        l = tk.Label(f_4,
                     text="边缘下限",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v4 = self.init_apart_list[4]
        s1 = tk.Scale(f_4,
                      from_=0,
                      to=1000,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v4,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_4.pack()

        f_5 = tk.Frame(self.ctr_board)
        l = tk.Label(f_5,
                     text="高斯模糊",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v5 = self.init_apart_list[5]
        s1 = tk.Scale(f_5,
                      from_=0,
                      to=40,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v5,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_5.pack()

    def init_board_type2(self):
        f_1 = tk.Frame(self.ctr_board)
        l = tk.Label(f_1,
                     text="缩放比例",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v1 = self.init_apart_list[1]
        s1 = tk.Scale(f_1,
                      from_=1,
                      to=100,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=v1,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_1.pack()
        self.alpha

        f_2 = tk.Frame(self.ctr_board)
        l = tk.Label(f_2,
                     text="亮度增益",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v1 = self.init_apart_list[1]
        s1 = tk.Scale(f_2,
                      from_=0,
                      to=200,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=self.alpha,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_2.pack()

        f_2 = tk.Frame(self.ctr_board)
        l = tk.Label(f_2,
                     text="亮度基准",
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=1)
        l.pack(side=tk.LEFT)
        v1 = self.init_apart_list[1]
        s1 = tk.Scale(f_2,
                      from_=0,
                      to=200,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=self.beta,
                      command=self.upall_img)
        s1.pack(side=tk.LEFT)
        f_2.pack()


gui = main_gui()
