import tkinter as tk
from fac_dir import item_color_dir



def get_colorCode(color):
    st = '#'
    for i in range(0,3):
        n = color[i]
        s = '{0:02x}'.format(n).upper()
        st += s
    return st


top = tk.Tk()
check_var_list = []
row_counter = 0
f_SelectBoard = tk.Frame(top,borderwidth=2,relief="groove")
one = tk.Label(f_SelectBoard,text ='材质选择面板')
one.grid(row=row_counter,column=0)

row_counter +=1
one = tk.Label(f_SelectBoard,text ='实体材质')
one.grid(row=row_counter,column=0)


row_counter +=1

for i in item_color_dir.values():
    if i['isEntity'] == True:
        CheckVar1 = tk.IntVar()
        check_var_list.append(CheckVar1)
        C1 = tk.Checkbutton(f_SelectBoard, variable = CheckVar1,
                        onvalue = 1, offvalue = 0,bg=get_colorCode(i["color"]),width=4)
        one = tk.Label(f_SelectBoard,text =i["name"],width=15,anchor=tk.NW)
        one.grid(row=row_counter,column=1)
        C1.grid(row=row_counter,column=0)
        row_counter +=1


row_counter = 1


one = tk.Label(f_SelectBoard,text ='地板材质')
one.grid(row=row_counter,column=2)

row_counter +=1

for i in item_color_dir.values():
    if i['isEntity'] == False:
        CheckVar1 = tk.IntVar()
        check_var_list.append(CheckVar1)
        C1 = tk.Checkbutton(f_SelectBoard, variable = CheckVar1,
                        onvalue = 1, offvalue = 0,bg=get_colorCode(i["color"]),width=4)
        one = tk.Label(f_SelectBoard,text =i["name"],width=15,anchor=tk.NW)
        one.grid(row=row_counter,column=3)
        C1.grid(row=row_counter,column=2)
        row_counter +=1

f_SelectBoard.pack(side=tk.LEFT)
top.mainloop()