import random
import time
import json
import numpy as np
from tkinter import *
from tkinter.ttk import *
import GA_Sudoku_Solver as gss

random.seed(time.time())

class SudokuGUI(Frame):

    def __init__(self, master, file):

        Frame.__init__(self, master)
        if master:
            master.title("SudokuGUI")

        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []
        self.easy, self.medium, self.hard, self.expert = [], [], [], []
        self.load_db(file)
        self.make_grid()
        self.bframe = Frame(self)
        #bframe = Frame(self)

        # select game difficult level
        self.lvVar = StringVar()
        self.lvVar.set("")
        difficult_level = ["Easy","Medium","Hard","Expert"]
        Label(self.bframe, text="Please select difficult level:", font="Times 18 underline").pack(anchor=S)
        for l in difficult_level:
            Radiobutton(self.bframe, text=l, width=20, variable=self.lvVar, value=l)\
                .pack(anchor=S)
        # generate new game
        self.ng = Button(self.bframe, text='Generate New Game', width=20, command=self.new_game)\
            .pack(anchor=S)
        # solver
        self.sg = Button(self.bframe, text='Solver', width=20, command=self.solver).pack(anchor=S)

        self.bframe.pack(side='bottom', fill='x', expand='1')
        self.pack()

    def rgb(self, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def load_db (self, file):
        with open(file) as f:
            data = json.load(f)
        self.easy = data['Easy']
        self.medium = data['Medium']
        self.hard = data['Hard']
        self.expert = data['Expert']

    def new_game(self):
        level = self.lvVar.get()
        if level == "Easy":
            self.given = self.easy[random.randint(0,len(self.easy)-1)]
        elif level == "Medium":
            self.given = self.medium[random.randint(0, len(self.medium)-1)]
        elif level == "Hard":
            self.given = self.hard[random.randint(0, len(self.hard)-1)]
        elif level == "Expert":
            self.given = self.expert[random.randint(0, len(self.expert)-1)]
        else:
            self.given = [[0 for x in range(9)] for y in range(9)]
        self.grid = np.array(list(self.given)).reshape((9,9)).astype(int)
        self.sync_board_and_canvas()

    def solver(self):
        s = gss.Sudoku()
        s.load(self.grid)
        start_time = time.time()
        generation, solution = s.solve()
        if (solution):
            if generation == -1:
                print("Invalid inputs")
                str_print = "Invalid input, please try to generate new game"
            elif generation == -2:
                print("No solution found")
                str_print = "No solution found, please try again"
            else:
                self.grid_2 = solution.values
                self.sync_board_and_canvas_2()
                time_elapsed = '{0:6.2f}'.format(time.time()-start_time)
                str_print = "Solution found at generation: " + str(generation) + \
                        "\n" + "Time elapsed: " + str(time_elapsed) + "s"
            Label(self.bframe, text=str_print, relief="solid", justify=LEFT).pack()
            self.bframe.pack()

    def make_grid(self):
        ( w,h ) = (256,256)
        c = Canvas(self, bg=self.rgb(128,128,128), width=2*w, height=h)
        c.pack(side='top', fill='both', expand='1')

        self.rects = [[None for x in range(18)] for y in range(18)]
        self.handles = [[None for x in range(18)] for y in range(18)]
        rsize = w/9
        guidesize = h/3

        for y in range(18):
            for x in range(18):
                (xr, yr) = (x*guidesize, y*guidesize)
                if x < 3:
                    self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize,
                                                      yr+guidesize, width=4, fill='yellow')
                else:
                    self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize,
                                                      yr+guidesize, width=4, fill='gray')
                (xr, yr) = (x*rsize, y*rsize)
                r = c.create_rectangle(xr, yr, xr+rsize, yr+rsize)
                t = c.create_text(xr + rsize / 2, yr + rsize / 2)
                self.handles[y][x] = (r, t)

        self.canvas = c
        self.sync_board_and_canvas()

    def sync_board_and_canvas(self):
        g = self.grid
        for y in range(9):
            for x in range(9):
                if g[y][x] != 0:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=str(g[y][x]))
                else:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text='')
    def sync_board_and_canvas_2(self):
        g = self.grid_2
        for y in range(9):
            for x in range(9):
                self.canvas.itemconfig(self.handles[y][x+9][1],
                                       text=str(g[y][x]))
######
file = "Sudoku_database.json"
tk = Tk()
gui = SudokuGUI(tk,file)
gui.mainloop()