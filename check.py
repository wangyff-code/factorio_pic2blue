import tkinter as tk
 

color_list = [[66, 158, 206], [148, 93, 0], [0, 89, 107], [164, 129, 66],
              [148, 101, 25], [173, 129, 58], [206, 214, 206], [123, 125, 123],
              [74, 81, 82], [58, 61, 58], [33, 142, 181], [41, 49, 49],
              [25, 93, 115]]



def get_colorCode(color):
    st = '#'
    for i in range(0,3):
        n = color[i]
        s = '{0:02x}'.format(n).upper()
        st += s
    return st


top = tk.Tk()
check_var_list = []
line1 = len(color_list)//2
f_SelectBoard = tk.Frame(top,borderwidth=2,relief="groove")
one = tk.Label(f_SelectBoard,text ='helloworld')
one.pack(side = tk.TOP)
f_selet1 = tk.Frame(f_SelectBoard)
for i in range(0,line1):
    f1 = tk.Frame(f_selet1)
    CheckVar1 = tk.IntVar()
    check_var_list.append(CheckVar1)
    C1 = tk.Checkbutton(f1, variable = CheckVar1,
                    onvalue = 1, offvalue = 0)
    one = tk.Label(f1,text ='helloworld',bg=get_colorCode(color_list[i]))
    C1.pack(side=tk.LEFT)
    one.pack(side=tk.LEFT) 
    f1.pack(side=tk.TOP)
f_selet1.pack(side=tk.LEFT)

f_selet2 = tk.Frame(f_SelectBoard)
for i in range(line1,len(color_list)):
    f1 = tk.Frame(f_selet2)
    CheckVar1 = tk.IntVar()
    check_var_list.append(CheckVar1)
    C1 = tk.Checkbutton(f1, variable = CheckVar1,
                    onvalue = 1, offvalue = 0)
    one = tk.Label(f1,text ='helloworld',bg=get_colorCode(color_list[i]))
    C1.pack(side=tk.LEFT)
    one.pack(side=tk.LEFT) 
    f1.pack(side=tk.TOP)
f_selet2.pack(side=tk.LEFT)
f_SelectBoard.pack(side=tk.LEFT)
top.mainloop()