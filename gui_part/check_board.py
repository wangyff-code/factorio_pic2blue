import tkinter as tk
from fac_dir import item_color_dir


def get_colorCode(color):
    st = '#'
    for i in range(0, 3):
        n = color[i]
        s = '{0:02x}'.format(n).upper()
        st += s
    return st


class Check_board_class():
    def get_colorCode(self,color):
        st = '#'
        for i in range(0, 3):
            n = color[i]
            s = '{0:02x}'.format(n).upper()
            st += s
        return st

    def press_check(self):
        self.count = 0
        for i in self.check_int_dir.values():
            self.count += int(i.get())
        self.up()

    def set_all(self):
        for i in self.check_int_dir.values():
            i.set(1)
        self.press_check()
 
    def clr_all(self):
        for i in self.check_int_dir.values():
            i.set(0)
        self.press_check()

    def __init__(self,window,_side,up):
        self.count = 0
        self.up = up
        self.check_int_dir = {}
        for i in item_color_dir.values():
            self.check_int_dir[i['name']] = tk.IntVar()

        row_counter = 0


        self.f_SelectBoard = tk.Frame(window, borderwidth=2, relief="groove",bd=4)
        one = tk.Label(self.f_SelectBoard, text='材质选择面板')
        one.grid(row=row_counter, column=0)

        row_counter += 1
        one = tk.Label(self.f_SelectBoard, text='实体材质')
        one.grid(row=row_counter, column=0)

        row_counter += 1


        for i in item_color_dir.values():
            if i['isEntity'] == True:
                CheckVar1 = self.check_int_dir[i['name']]
                C1 = tk.Checkbutton(self.f_SelectBoard,
                                    variable=CheckVar1,
                                    onvalue=1,
                                    offvalue=0,
                                    bg=self.get_colorCode(i["color"]),
                                    width=4,
                                    bd=4,
                                    relief=tk.RAISED,
                                    command=self.press_check)
                one = tk.Label(self.f_SelectBoard, text=i["name"], width=15, anchor=tk.NW)
                one.grid(row=row_counter, column=1)
                C1.grid(row=row_counter, column=0)
                row_counter += 1
        b = tk.Button(self.f_SelectBoard, text ="全选", command = self.set_all)
        b.grid(row=row_counter, column=4)

        b = tk.Button(self.f_SelectBoard, text ="清除", command = self.clr_all)
        b.grid(row=row_counter, column=5)

        row_counter = 1

        one = tk.Label(self.f_SelectBoard, text='地板材质')
        one.grid(row=row_counter, column=2)

        row_counter += 1
        for i in item_color_dir.values():
            if i['isEntity'] == False:
                CheckVar1 = self.check_int_dir[i['name']]
                C1 = tk.Checkbutton(self.f_SelectBoard,
                                    variable=CheckVar1,
                                    onvalue=1,
                                    offvalue=0,
                                    bg=self.get_colorCode(i["color"]),
                                    width=4,
                                    bd=4,
                                    relief=tk.RAISED,
                                    command=self.press_check)
                one = tk.Label(self.f_SelectBoard, text=i["name"], width=15, anchor=tk.NW)
                one.grid(row=row_counter, column=3)
                C1.grid(row=row_counter, column=2)
                row_counter += 1
        self.f_SelectBoard.pack(side=_side)

    def destroy(self):
        self.f_SelectBoard.destroy()
