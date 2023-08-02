# touchscreen.py

# graphics library
from tkinter import *

# # data visualization
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np

import random

random.seed(1965)

class Game(Tk):
    def __init__(self):
        super().__init__()

        # for the easy version
        self.title("The Hard Easy Game")

        # set geometry (widthxheight)
        self.geometry('1360x710')

        self.resizable(width=False, height=False)

        # instructions
        subtitle = Label(self, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
        subtitle.place(anchor='nw')

        self.finish = Label(self, text="Finish Line")
        self.finish.place(x=1235, y=125)

        self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')

        self.canvas = Canvas(self, bg="white", width=1250, height = 500)
        self.canvas.place(x=50, y=150)
        # self.canvas.pack(fill=BOTH, padx=50, pady=150, expand=True)

        # self.canvas.bind("<Configure>", self.on_resize)

        # initial position of dot
        dot_radius = 20
        self.init_x1 = 50 - dot_radius
        self.init_y1 = 250 - dot_radius
        self.init_x2 = 50 + dot_radius
        self.init_y2 = 250 + dot_radius

        # create dot
        self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
                         self.init_x2, self.init_y2,
                         outline='red', fill='red')
        
        self.line = self.canvas.create_line(1225, 0, 1225, 500)
        
        # self.update_dot_position("<Configure>")
        
        self.game_mode = None

        self.create_buttons()
        self.create_menu()

        self.move_B = ['g', 'y', 'r', 'b']
        self.move_C1 = ['g', 'g']
        self.move_C2 = ['r', 'y']
        self.input_seqB = []
        self.input_seqC = []

        self.blueCounter1 = 4
        self.blueDecrease1 = 1
        
        self.redCounter1 = 4
        self.redDecrease1 = 1
        
        self.yellowCounter1 = 4
        self.yellowDecrease1 = 1

        # self.bind("<Configure>", self.on_resize)

    # def on_resize(self, event):
    #         # self.canvas_width = event.width
    #         # self.canvas_height = event.height
    #         # self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
    #         self.update_dot_position

    # def update_dot_position(self, event):
    #     canvas_width = event.width
    #     canvas_height = event.height

    #     center_x = canvas_width // 2
    #     center_y = canvas_height // 2

    #     self.canvas.coords(self.dot, center_x - 10, center_y - 10, 
    #                         center_x + 10, center_y + 10)
    
    def create_buttons(self):
        self.btnB = Button(self, width='14', height='6', bg='blue', command=self.move_blue)
        self.btnR = Button(self, width='14', height='6', bg='red', command=self.move_red)
        self.btnG = Button(self, width='14', height='6', bg='green', command=self.move_green)
        self.btnY = Button(self, width='14', height='6', bg='yellow', command=self.move_yellow)

        self.btnB.place(x='75', y='30')
        self.btnR.place(x='200', y='30')
        self.btnG.place(x='325', y='30')
        self.btnY.place(x='450', y='30')

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        game_menu = Menu(menubar, tearoff=0)
        game_menu.add_command(label='A', command=self.modeA)
        game_menu.add_command(label='B', command=self.modeB)
        game_menu.add_command(label='C', command=self.modeC)
        game_menu.add_command(label='1', command=self.mode1)

        menubar.add_cascade(label="Game Modes", menu=game_menu)

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.game_mode = "A"
        self.congrats.place_forget()

    # Mode B: a specific sequence of 4 button presses moves dot right
    def modeB(self):
        self.game_mode = "B"
        self.congrats.place_forget()

    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        self.game_mode = "C"
        self.congrats.place_forget()

    def mode1(self):
        self.game_mode = "1"
        self.congrats.place_forget()

    def check_completion(self):
        if self.canvas.coords(self.dot)[2] >= 1225:
            self.game_mode = None
            self.congrats.place(x=50, y=675)

            x1, y1, x2, y2 = self.canvas.coords(self.dot)
            dx = self.init_x1 - x1
            dy = self.init_y1 - y1
            self.canvas.move(self.dot, dx, dy)

    def move_left(self):
        if self.canvas.coords(self.dot)[0] > 0:
            self.canvas.move(self.dot, -20, 0)

    def move_right(self):
        if self.canvas.coords(self.dot)[2] < 1250:
            self.canvas.move(self.dot, 20, 0)
            self.check_completion()

    def move_up(self):
        if self.canvas.coords(self.dot)[1] > 0:
            self.canvas.move(self.dot, 0, -20)

    def move_down(self):
        if self.canvas.coords(self.dot)[3] < 500:
            self.canvas.move(self.dot, 0, 20)

    # blue button
    def move_blue(self):
        
        if self.game_mode == "A":
            self.move_right()

        elif self.game_mode == "B":
            self.input_seqB.append('b')
            self.move_up()
            if self.input_seqB[-4:] == self.move_B:
                for num in range(4):
                    self.move_right()

        elif self.game_mode == "C":
            self.input_seqC.append('b')

        elif self.game_mode == "1":
            randVal = random.randrange(1, self.blueCounter1)
            if randVal == 1 and self.blueCounter1 < 10:
                self.move_right()
            self.blueDecrease1 += 1
            if self.blueDecrease1 % 4 == 0:
                self.blueCounter1 += 1

    # red button
    def move_red(self):

        if self.game_mode == "A":
            self.move_left()

        elif self.game_mode == "B":
            self.input_seqB.append('r')
            self.move_down()

        elif self.game_mode == "C":
            self.input_seqC.append('r')

        elif self.game_mode == "1":
            randVal = random.randrange(1, self.redCounter1)
            if randVal == 1 and self.redCounter1 < 10:
                self.move_right()
            self.redDecrease1 += 1
            if self.redDecrease1 % 4 == 0:
                self.redCounter1 += 1

    # green button
    def move_green(self):
        if self.game_mode == "A":
            self.move_up()

        elif self.game_mode == "B":
            self.input_seqB.append('g')
            self.move_down()

        elif self.game_mode == "C":
            self.input_seqC.append('g')
            if self.input_seqC[-2:] == self.move_C1 and self.canvas.coords(self.dot)[0] <= 575:
                self.move_right()
                self.move_right()
                self.input_seqC = []

        elif self.game_mode == "1":
            randVal = random.randrange(1, 3)
            if randVal == 1:
                self.move_right()

    # yellow button
    def move_yellow(self):

        if self.game_mode == "A":
            self.move_down()

        elif self.game_mode == "B":
            self.input_seqB.append('y')
            self.move_up()

        elif self.game_mode == "C":
            self.input_seqC.append('y')
            if self.input_seqC[-2:] == self.move_C2 and self.canvas.coords(self.dot)[0] > 575:
                self.move_right()
                self.move_right()

        elif self.game_mode == "1":
            randVal = random.randrange(1, self.yellowCounter1)
            if randVal == 1 and self.yellowCounter1 < 10:
                self.move_right()
            self.yellowDecrease1 += 1
            if self.yellowDecrease1 % 4 == 0:
                self.yellowCounter1 += 1

if __name__ == "__main__":
    game = Game()
    game.mainloop()