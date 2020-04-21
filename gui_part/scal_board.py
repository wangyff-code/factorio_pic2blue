import tkinter as tk
from fac_dir import scale_dir1,scale_dir2


def get_colorCode(color):
    st = '#'
    for i in range(0, 3):
        n = color[i]
        s = '{0:02x}'.format(n).upper()
        st += s
    return st


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
                     height=1)
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
                     height=1)
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

