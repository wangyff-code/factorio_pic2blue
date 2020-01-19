import tkinter as tk
import cv2
from PIL import Image,ImageTk
from tkinter import filedialog
import numpy as np
from tkinter import ttk
import  threading
import tkinter.messagebox
import os
import numba


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

def show_tkimg(img,zoon):
    x, y = img.shape[0:2]
    t = max(x,y)
    t = (zoon/t)
    x *=t
    y *=t
    dim = (int(y),int(x))
    resize = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    img_rgb = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_rgb)
    tkImage = ImageTk.PhotoImage(image=img)
    return tkImage



def openfiles2(label_img,window):
    global or_img
    global v0
    s2fname = filedialog.askopenfilename(title='打开图片文件', filetypes=[('jpg', '*.jpg'), ('All Files', '*')])
    or_img=cv2.imdecode(np.fromfile(s2fname,dtype=np.uint8),-1)
    tkImage=show_tkimg(or_img,v0.get())
    label_img.configure(image= tkImage)
    label_img.image = tkImage
    up_img()


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


def up_img(*age):
    global or_img
    global out_img
    global label_img2
    global v0,v1,v2,v3,v4,v5
    x, y = or_img.shape[0:2]
    x*= v1.get()/100.0
    y*= v1.get()/100.0
    dim = (int(y), int(x))
    resize = cv2.resize(or_img, dim, interpolation = cv2.INTER_AREA)
    if v5.get() != 0:
        img_GaussianBlur=cv2.GaussianBlur(resize,(v5.get()*2+1,v5.get()*2+1),0)
    else:
        img_GaussianBlur = resize
    Can = cv2.Canny(img_GaussianBlur, int(v3.get()), int(v4.get()))
    gray=cv2.cvtColor(resize,cv2.COLOR_BGR2GRAY)
    temp = int(v2.get())
    if temp >= 255:
        ret,im_fixed=cv2.threshold(gray,temp-255,255,cv2.THRESH_BINARY)
        out_img = add_can_img(Can,im_fixed)
        out_img = cv2.bitwise_not(out_img)
    else:
        ret,im_fixed=cv2.threshold(gray,temp,255,cv2.THRESH_BINARY)
        out_img = add_can_img(Can,im_fixed)
    tkImage=show_tkimg(out_img,v0.get())
    label_img2.configure(image= tkImage)
    label_img2.image = tkImage




def upall_img(*age):
    global or_img
    global out_img
    tkImage=show_tkimg(out_img,v0.get())
    label_img2.configure(image= tkImage)
    label_img2.image = tkImage
    tkImage=show_tkimg(or_img,v0.get())
    label_img1.configure(image= tkImage)
    label_img1.image = tkImage



def tras():
    global out_img
    global p1
    global item_name
    gen = gen_mat(out_img,p1,item_name)
    gen.strat_trans()
    

def conf(win,picvar,number1,number2):
    global item_name
    item_list = [item_dir[number1.get()],item_dir[number2.get()]]
    gen_type = picvar.get()
    item_name = gen_type,item_list
    win.destroy()





def set_item():
    global item_name
    
    win = tk.Toplevel()
    win.title("材质设置") 
    # win.geometry('200x80')

    f1 = tk.Frame(win)
  
    picvar = tk.IntVar()
    pic = tk.Radiobutton(f1, text="单材质", variable=picvar, value=0)      
    pic.grid(row = 0,column = 0)
    pic.select()

    pic1 = tk.Radiobutton(f1, text="双材质", variable=picvar, value=1)      
    pic1.grid(row = 1,column = 0)

    pic2 = tk.Radiobutton(f1, text="特殊材质", variable=picvar, value=2)      
    pic2.grid(row = 2,column = 0)


    l = tk.Label(f1, text="   材质1：", bg="pink", font=("Arial",10),width=15)
    l.grid(row = 0,column = 1)


    l = tk.Label(f1, text="   材质1：", bg="pink", font=("Arial",10),width=15)
    l.grid(row = 1,column = 1)

    l = tk.Label(f1, text="   特殊材质：", bg="pink", font=("Arial",10),width=15)
    l.grid(row = 2,column = 1)


    number1 = tk.StringVar()
    numberChosen1 = ttk.Combobox(f1, width=10, height=10, textvariable=number1)
    numberChosen1['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
    numberChosen1.current(0)
    numberChosen1.grid(row = 0,column = 2)


    numberChosen1 = ttk.Combobox(f1, width=10, height=10, textvariable=number1)
    numberChosen1['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
    numberChosen1.current(0)
    numberChosen1.grid(row = 1,column = 2)


    number3 = tk.StringVar()
    numberChosen3 = ttk.Combobox(f1, width=10, height=10, textvariable=number3)
    numberChosen3['values'] = ("灯","太阳能-电池")   
    numberChosen3.current(0)
    numberChosen3.grid(row = 2,column = 2)


    l = tk.Label(f1, text="   材质2：", bg="pink", font=("Arial",10),width=15)
    l.grid(row = 1,column = 3)

    number2 = tk.StringVar()
    numberChosen2 = ttk.Combobox(f1, width=10, height=10, textvariable=number2)
    numberChosen2['values'] = ("石砖","标准混凝土","标准混凝土(标识)","钢筋混凝土","钢筋混凝土(标识)","填海料")   
    numberChosen2.current(0)
    numberChosen2.grid(row = 1,column = 4)

    b1=tk.Button(f1, text='确定', width=4, height=2,command=lambda :conf(win,picvar,number1,number2))
    b1.grid(row = 3,column = 0)
    f1.pack()
 


def init():
    global v0
    global v1
    global v2
    global v3
    global v4
    global v5
    try:
        f = open('ini.json','r')
        data = f.read()
        f.close()
        var_list = json.loads(data)
        v0.set(var_list[0])
        v1.set(var_list[1])
        v2.set(var_list[2])
        v3.set(var_list[3])
        v4.set(var_list[4])
        v5.set(var_list[5])
    except:
        pass


def on_closing():
    global v0
    global v1
    global v2
    global v3
    global v4
    global v5
    var_list = [v0.get(),v1.get(),v2.get(),v3.get(),v4.get(),v5.get()]
    f = open('ini.json','w')
    text = json.dumps(var_list)
    f.write(text)
    f.close()
    window.destroy()


origin_img = Image.fromarray(np.zeros((100,100),dtype=np.uint8))
window = tk.Tk()
window.title('图片转蓝图 V3.0')
tkImage = ImageTk.PhotoImage(image=origin_img)


menubar=tk.Menu(window)
fmenu1=tk.Menu(window)
for item in ['打开']:
    fmenu1.add_command(label=item,command=lambda :openfiles2(label_img1,window))
fmenu2=tk.Menu(window)
for item in ['材质设置']:
     fmenu2.add_command(label=item,command=lambda :set_item())
menubar.add_cascade(label="文件",menu=fmenu1)
menubar.add_cascade(label="设置",menu=fmenu2)
window['menu']=menubar



fm1 = tk.Frame(window)


label_img1 = tk.Label(fm1, image = tkImage)
label_img1.pack(side = tk.LEFT)
label_img2 = tk.Label(fm1, image = tkImage)
label_img2.pack(side = tk.LEFT)
fm1.pack(side =tk.TOP)
v0=tk.IntVar()
v0.set(400)
s1 = tk.Scale(fm1,from_=100,to=1000,length=100,variable=v0,command=upall_img)
s1.pack()

fm2 = tk.Frame(window)

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


fm3 = tk.Frame(window)
com = tk.Button(fm3,text = '开始转换',  command=start_go) 
com.pack(side = tk.LEFT)

p1 = ttk.Progressbar(fm3, length=1000, mode="determinate", orient=tk.HORIZONTAL)
p1.pack(side=tk.BOTTOM)
p1["maximum"] = 100
p1["value"] = 0

fm3.pack(side =tk.BOTTOM)




add_can_img(np.zeros((100,100),dtype=np.uint8),np.zeros((100,100),dtype=np.uint8))
init()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()