import tkinter as tk
from check_board import Check_board_class
from scal_board import scal_board_class


class ctr_topClass():
    def __init__(self, window, update):
        self.update = update
        self.scal_type = 0
        self.window = window
        self.Check_board = Check_board_class(self.window, tk.LEFT, self.up)
        self.scal_board = scal_board_class()
        self.scal_board.init_scal_type1(self.window, tk.LEFT, self.up)

    def up(self, *arg):
        if self.Check_board.count <= 2:
            if self.scal_type == 1:
                self.scal_board.destroy()
                self.scal_board.init_scal_type1(self.window, tk.LEFT, self.up)
                self.scal_type = 0
        else:
            if self.scal_type == 0:
                self.scal_board.destroy()
                self.scal_board.init_scal_type2(self.window, tk.LEFT, self.up)
                self.scal_type = 1
        self.update(self.scal_type, self.Check_board.check_int_dir,
                    self.scal_board.scale_dir1,
                    self.scal_board.scale_dir2)


def update(scal_type,check_int_dir,scale_dir1,scale_dir2):
    pass


if __name__ == "__main__":
    top = tk.Tk()
    test = ctr_topClass(top, update)
    top.mainloop()