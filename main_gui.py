import tkinter as tk
import cv2 as cv 
from PIL import Image,ImageTk
from tkinter import filedialog
import numpy as np
from tkinter import ttk
import  threading
import tkinter.messagebox
import os
import numba
import json
import webbrowser

from trans_fun import gen_mat

item_name = 0,['stone-path']

item_dir = {
    "石砖":'stone-path',
    "标准混凝土":'concrete',
    "标准混凝土(标识)":'hazard-concrete-left',
    "钢筋混凝土":'refined-concrete',
    "钢筋混凝土(标识)":'refined-hazard-concrete-left',
    "填海料":'landfill'
}


@numba.jit
def add_can_img(can,img):
    x, y = can.shape[0:2]
    for i in range(0,x):
        for k in range(0,y):
            if can[i][k] == 255:
                if img[i][k] == 255:
                    img[i][k] = 0
                else:
                    img[i][k] =255
    return img


def start_go():
    t = threading.Thread(target=tras)
    t.setDaemon(True)
    t.start()
    tkinter.messagebox.showinfo('提示','正在转换，请稍后\n转换完成后会再TXT中打开结果\n也可以自己打开output.txt')

def github():
    webbrowser.open("https://github.com/wangyff-code/factorio_pic2blue", new=0)
    pass

class main_gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('图片转蓝图 V4.1')

        self.read_apartment()
        self.init_menu()
        self.init_face()

        self.window.protocol("WM_DELETE_WINDOW", self.save_apartment)
        self.window.mainloop()

    def init_menu(self):
        menubar=tk.Menu(self.window)
        fmenu1=tk.Menu(self.window)
        for item in ['打开']:
            fmenu1.add_command(label=item,command=lambda :self.openfiles())
        fmenu2=tk.Menu(self.window)
        for item in ['材质设置']:
            fmenu2.add_command(label=item,command=lambda :self.set_item())
        menubar.add_cascade(label="文件",menu=fmenu1)
        menubar.add_cascade(label="设置",menu=fmenu2)
        self.window['menu']=menubar


    def read_apartment(self):
        self.init_apart_list = []
        for i in range(0,6):
            a = tk.IntVar()
            self.init_apart_list.append(a)
        try:
            f = open('ini.json','r')
            data = f.read()
            f.close()
            var_list = json.loads(data)
            for i in range(0,6):
                self.init_apart_list[i].set(var_list[i])
        except:
            for i in range(0,6):
                self.init_apart_list[i].set(10)    
            pass

    def save_apartment(self,window):
        var_list = []
        for i in self.init_apart_list:
            var_list.append(i.get())
        f = open('ini.json','w')
        text = json.dumps(var_list)
        f.write(text)
        f.close()
        self.window.destroy()

    def openfiles(self):
        s2fname = filedialog.askopenfilename(title='打开图片文件', filetypes=[('jpg', '*.jpg'), ('All Files', '*')])
        self.or_img=cv.imdecode(np.fromfile(s2fname,dtype=np.uint8),-1)


    def conf(self,win,picvar,number1,number2,number3,et):
        global item_name
        try:
            k = float(et.get())
        except:
            k=1
        item_list = [item_dir[number1.get()],item_dir[number2.get()],k]
        gen_type = picvar.get()
        print(gen_type)
        item_name = gen_type,item_list
        win.destroy()


    def show_tkimg(self.img):
        x, y = img.shape[0:2]
        t = max(x,y)
        t = (self.init_apart_list[0].get()/t)
        x *=t
        y *=t
        dim = (int(y),int(x))
        resize = cv.resize(img, dim, interpolation = cv.INTER_AREA)
        img_rgb = cv.cvtColor(resize, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img_rgb)
        tkImage = ImageTk.PhotoImage(image=img)
        return tkImage


    def up_img(self):
        x, y = self.or_img.shape[0:2]
        x*= self.init_apart_list[1].get()/100.0
        y*= self.init_apart_list[1].get()/100.0
        dim = (int(y), int(x))
        resize = cv.resize(self.or_img, dim, interpolation = cv.INTER_AREA)
        if self.init_apart_list[5].get() != 0:
            img_GaussianBlur=cv.GaussianBlur(resize,(v5.get()*2+1,v5.get()*2+1),0)
        else:
            img_GaussianBlur = resize
        Can = cv.Canny(img_GaussianBlur, int(self.init_apart_list[3].get()), int(self.init_apart_list[4].get()))
        gray=cv.cvtColor(resize,cv.COLOR_BGR2GRAY)
        temp = int(self.init_apart_list[2].get())
        if temp >= 255:
            ret,im_fixed=cv.threshold(gray,temp-255,255,cv.THRESH_BINARY)
            out_img = add_can_img(Can,im_fixed)
            out_img = cv.bitwise_not(out_img)
        else:
            ret,im_fixed=cv.threshold(gray,temp,255,cv.THRESH_BINARY)
            out_img = add_can_img(Can,im_fixed)
        return out_img

    def upall_img(self,*age):
        out_img = self.up_img(self.or_img)
        tkImage=self.show_tkimg(out_img)
        self.label_img2.configure(image= tkImage)
        self.label_img2.image = tkImage
        tkImage=self.show_tkimg(self.or_img)
        self.label_img1.configure(image= tkImage)
        self.label_img1.image = tkImage

    def set_item(self):
        win = tk.Toplevel()
        win.title("材质设置") 
        f1 = tk.Frame(win)
    #--------------------------------------
        picvar = tk.IntVar()
        pic = tk.Radiobutton(f1, text="单材质", variable=picvar, value=0)      
        pic.grid(row = 0,column = 0)
        pic.select()

        pic1 = tk.Radiobutton(f1, text="双材质", variable=picvar, value=1)      
        pic1.grid(row = 1,column = 0)

        pic2 = tk.Radiobutton(f1, text="特殊材质", variable=picvar, value=2)      
        pic2.grid(row = 2,column = 0)

        pic3 = tk.Radiobutton(f1, text="多颜色多材质", variable=picvar, value=3)      
        pic3.grid(row = 3,column = 0)

        l = tk.Label(f1, text="   材质1：", bg="pink", font=("Arial",10),width=15)
        l.grid(row = 0,column = 1)

        l = tk.Label(f1, text="   材质1：", bg="pink", font=("Arial",10),width=15)
        l.grid(row = 1,column = 1)

        l = tk.Label(f1, text="   特殊材质：", bg="pink", font=("Arial",10),width=15)
        l.grid(row = 2,column = 1)
    #--------------------------------------
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(f1, width=10, height=10, textvariable=number1)
        numberChosen1['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
        numberChosen1.current(0)
        numberChosen1.grid(row = 0,column = 2)

        numberChosen1 = ttk.Combobox(f1, width=10, height=10, textvariable=number1)
        numberChosen1['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
        numberChosen1.grid(row = 1,column = 2)

        number3 = tk.StringVar()
        number3.set("太阳能-电池")
        numberChosen1 = ttk.Combobox(f1, width=10, height=10, textvariable=number3)
        numberChosen1['values'] = ("太阳能-电池")   
        numberChosen1.grid(row = 2,column = 2)

        l = tk.Label(f1, text="   材质2：", bg="pink", font=("Arial",10),width=15)
        l.grid(row = 1,column = 3)

        l = tk.Label(f1, text="   电池/太阳能 =", bg="pink", font=("Arial",10),width=15)
        l.grid(row = 2,column = 3)

        et = tk.Entry(f1)
        et.grid(row = 2,column = 4)
        et.insert(0,'1')
        number2 = tk.StringVar()
        numberChosen2 = ttk.Combobox(f1, width=10, height=10, textvariable=number2)
        numberChosen2['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
        numberChosen2.current(0)
        numberChosen2.grid(row = 1,column = 4)

        b1=tk.Button(f1, text='确定', width=4, height=2,command=lambda :self.conf(win,picvar,number1,number2,number3,et))
        b1.grid(row = 3,column = 3)
        f1.pack()

    def init_face(self):
        self.or_img = np.zeros((100,100),dtype=np.uint8)
        tkImage = ImageTk.PhotoImage(image=self.or_img)

        fm1 = tk.Frame(self.window)
        self.label_img1 = tk.Label(fm1, image = tkImage)
        self.label_img1.pack(side = tk.LEFT)
        self.label_img2 = tk.Label(fm1, image = tkImage)
        self.label_img2.pack(side = tk.LEFT)
        v0=self.init_apart_list[0]
        s1 = tk.Scale(fm1,from_=100,to=1000,length=100,variable=v0,command=upall_img)
        s1.pack()
        fm1.pack(side =tk.TOP)

        fm2 = tk.Frame(self.window)

        f_1 = tk.Frame(fm2)
        l = tk.Label(f_1, text="缩放比例", bg="pink", font=("Arial",10), width=7, height=1)
        l.pack(side = tk.LEFT)
        v1=tk.IntVar()
        s1 = tk.Scale(f_1,from_=1,to=100,length=800,orient=tk.HORIZONTAL,variable=v1,command=up_img)
        s1.pack(side = tk.LEFT)
        f_1.pack()

        f_2 = tk.Frame(fm2)
        l = tk.Label(f_2, text="阈值下限", bg="pink", font=("Arial",10), width=7, height=1)
        l.pack(side = tk.LEFT)
        v2=tk.IntVar()
        s1 = tk.Scale(f_2,from_=0,to=510,length=800,orient=tk.HORIZONTAL,variable=v2,command=up_img)
        s1.pack(side = tk.LEFT)
        f_2.pack()

        f_3 = tk.Frame(fm2)
        l = tk.Label(f_3, text="边缘上限", bg="pink", font=("Arial",10), width=7, height=1)
        l.pack(side = tk.LEFT)
        v3=tk.IntVar()
        s1 = tk.Scale(f_3,from_=0,to=1000,length=800,orient=tk.HORIZONTAL,variable=v3,command=up_img)
        s1.pack(side = tk.LEFT)
        f_3.pack()

        f_4 = tk.Frame(fm2)
        l = tk.Label(f_4, text="边缘下限", bg="pink", font=("Arial",10), width=7, height=1)
        l.pack(side = tk.LEFT)
        v4=tk.IntVar()
        s1 = tk.Scale(f_4,from_=0,to=1000,length=800,orient=tk.HORIZONTAL,variable=v4,command=up_img)
        s1.pack(side = tk.LEFT)
        f_4.pack()

        f_5 = tk.Frame(fm2)
        l = tk.Label(f_5, text="高斯模糊", bg="pink", font=("Arial",10), width=7, height=1)
        l.pack(side = tk.LEFT)
        v5=tk.IntVar()
        s1 = tk.Scale(f_5,from_=0,to=40,length=800,orient=tk.HORIZONTAL,variable=v5,command=up_img)
        s1.pack(side = tk.LEFT)
        f_5.pack()
        fm2.pack()

        fm3 = tk.Frame(self.window)
        com = tk.Button(fm3,text = '开始转换',  command=start_go) 
        com.pack(side = tk.LEFT)

        p1 = ttk.Progressbar(fm3, length=1000, mode="determinate", orient=tk.HORIZONTAL)
        p1.pack(side=tk.BOTTOM)
        p1["maximum"] = 100
        p1["value"] = 0

        fm3.pack(side =tk.BOTTOM)
        com = tk.Button(self.window,text = '支持一下，点击进入github',command=github) 
        com.pack(side = tk.BOTTOM)        
gui = main_gui()