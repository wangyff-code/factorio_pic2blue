import tkinter as tk
from fac_dir import scale_dir1,scale_dir2,item_color_dir


class ctr_topClass():
    def __init__(self, window, update):
        self.update = update
        self.scal_type = 0
        self.window = window
        self.Check_board = Check_board_class(self.window, tk.LEFT, self.up)
        self.scal_board = scal_board_class()
        self.scal_board.init_scal_type1(self.window, tk.LEFT,self.up)
        self.Check_board._set([0,0,0,0,0,0,0,0,0,0,1,0,1])
        self.scal_board.set1([30,50,0,0])
        self.scal_board.set2([30,50,50])


    def up(self, *arg):
        if self.Check_board.count <= 2:
            if self.scal_type == 1:
                self.scal_board.destroy()
                self.scal_board.init_scal_type1(self.window, tk.LEFT,self.up)
                self.scal_type = 0
        else:
            if self.scal_type == 0:
                self.scal_board.destroy()
                self.scal_board.init_scal_type2(self.window, tk.LEFT,self.up)
                self.scal_type = 1
        self.update()

#------------------------------------------



#-----------------------------------------------
class scal_board_class():
    def __init__(self):
        self.scale_dir1 = scale_dir1
        self.scale_dir2 = scale_dir2
        for i in scale_dir1:
            self.scale_dir1[i] = tk.IntVar()
        for i in scale_dir2:
            self.scale_dir2[i] = tk.IntVar()

    def init_scal_type1(self,window,_side,upall_img):
        row_counter = 0
        self.f_SelectBoard = tk.Frame(window, borderwidth=2, relief="groove",bd=4)
        for i in self.scale_dir1:
            l = tk.Label(self.f_SelectBoard,
                     text=i,
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=4)
            l.grid(row=row_counter, column=0)
            s1 = tk.Scale(self.f_SelectBoard,
                      from_=1,
                      to=100,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=scale_dir1[i],
                      command=upall_img)
            s1.grid(row=row_counter, column=1)
            row_counter += 1
        self.f_SelectBoard.pack(side=_side)

    def init_scal_type2(self,window,_side,upall_img):
        row_counter = 0
        self.f_SelectBoard = tk.Frame(window, borderwidth=2, relief="groove",bd=4)
        for i in self.scale_dir2:
            l = tk.Label(self.f_SelectBoard,
                     text=i,
                     bg="pink",
                     font=("Arial", 10),
                     width=7,
                     height=4)
            l.grid(row=row_counter, column=0)
            s1 = tk.Scale(self.f_SelectBoard,
                      from_=1,
                      to=100,
                      length=800,
                      orient=tk.HORIZONTAL,
                      variable=scale_dir2[i],
                      command=upall_img)
            s1.grid(row=row_counter, column=1)
            row_counter += 1
        self.f_SelectBoard.pack(side=_side)

    def destroy(self):
        self.f_SelectBoard.destroy()

    def set1(self,set_list):
        k = 0
        for i in self.scale_dir1:
            self.scale_dir1[i].set(set_list[k])
            k += 1

    def get1(self):
        get_list = []
        for i in self.scale_dir1:
            get_list.append(self.scale_dir1[i].get())
        return get_list

    def set2(self,set_list):
        k = 0
        for i in self.scale_dir2:
            self.scale_dir2[i].set(set_list[k])
            k += 1

    def get2(self):
        get_list = []
        for i in self.scale_dir2:
            get_list.append(self.scale_dir2[i].get())
        return get_list



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
        self.color_list.clear()
        for i in self.check_int_dir:
            v = int(self.check_int_dir[i][0].get())
            if v == 1:
                self.color_list.append(item_color_dir[self.check_int_dir[i][1]]['color'])
                self.count += v
        self.up()

    def set_all(self):
        for i in self.check_int_dir.values():
            i[0].set(1)
        self.press_check()
 
    def clr_all(self):
        for i in self.check_int_dir.values():
            i[0].set(0)
        self.press_check()

    def __init__(self,window,_side,up):
        self.color_list = []
        self.count = 0
        self.up = up
        self.check_int_dir = {}
        for i in item_color_dir:
            self.check_int_dir[item_color_dir[i]['name']] = tk.IntVar(),i

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
                CheckVar1 = self.check_int_dir[i['name']][0]
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
                CheckVar1 = self.check_int_dir[i['name']][0]
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


    def _set(self,set_list):
        k = 0
        for i in item_color_dir.values():
            CheckVar1 = self.check_int_dir[i['name']][0]
            CheckVar1.set(set_list[k])
            k += 1

    def get(self):
        get_list = []
        for i in item_color_dir.values():
            CheckVar1 = self.check_int_dir[i['name']][0]
            get_list.append(CheckVar1.get())
        return get_list





if __name__ == "__main__":
    top = tk.Tk()
    top.mainloop()