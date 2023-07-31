# touchscreen.py

# graphics library
from tkinter import *

# # data visualization
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np

class Game(Tk):
    def __init__(self):
        super().__init__()

        # for the easy version
        self.title("The Hard Easy Game")

        # set geometry (widthxheight)
        self.geometry('700x400')

        # instructions
        subtitle = Label(self, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
        subtitle.place(anchor='nw')

        self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')
        # self.congrats.place(x=300, y=375)
        # self.congrats.place_forget()

        # create canvas for dot
        canvas_width = 600
        canvas_height = 250
        self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.place(x='50', y='100')

        # initial position of dot
        dot_radius = 20
        self.init_x1 = 50 - dot_radius
        self.init_y1 = 120 - dot_radius
        self.init_x2 = 50 + dot_radius
        self.init_y2 = 120 + dot_radius

        # create dot
        self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
                         self.init_x2, self.init_y2,
                         outline='red', fill='red')
        
        self.game_mode = None

        self.create_buttons()
        self.create_menu()

    def create_buttons(self):
        self.btnB = Button(self, width='7', height='3', bg='blue', command=self.move_blue)
        self.btnR = Button(self, width='7', height='3', bg='red', command=self.move_red)
        self.btnG = Button(self, width='7', height='3', bg='green', command=self.move_green)
        self.btnY = Button(self, width='7', height='3', bg='yellow', command=self.move_yellow)

        self.btnB.place(x='75', y='30')
        self.btnR.place(x='150', y='30')
        self.btnG.place(x='225', y='30')
        self.btnY.place(x='300', y='30')

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        game_menu = Menu(menubar, tearoff=0)
        game_menu.add_command(label='A', command=self.modeA)
        game_menu.add_command(label='B', command=self.modeB)
        game_menu.add_command(label='C', command=self.modeC)

        menubar.add_cascade(label="Game Modes", menu=game_menu)

    def modeA(self):
        self.game_mode = "A"
        self.congrats.place_forget()

    def modeB(self):
        self.game_mode = "B"
        self.congrats.place_forget()

    def modeC(self):
        self.game_mode = "C"
        self.congrats.place_forget()

    def check_completion(self):
        if self.canvas.coords(self.dot)[2] >= 550:
            self.game_mode = None
            self.congrats.place(x=300, y=375)
            # self.congrats.pack()

            x1, y1, x2, y2 = self.canvas.coords(self.dot)
            dx = self.init_x1 - x1
            dy = self.init_y1 - y1
            self.canvas.move(self.dot, dx, dy)

    def move_left(self):
        if self.canvas.coords(self.dot)[0] > 0:
            self.canvas.move(self.dot, -10, 0)

    def move_right(self):
        if self.canvas.coords(self.dot)[2] < 550:
            self.canvas.move(self.dot, 10, 0)
            self.check_completion()

    def move_up(self):
        if self.canvas.coords(self.dot)[1] > 0:
            self.canvas.move(self.dot, 0, -10)

    def move_down(self):
        if self.canvas.coords(self.dot)[3] > 0:
            self.canvas.move(self.dot, 0, 10)

    def move_blue(self):
        if self.game_mode == "A":
            self.move_left()
        elif self.game_mode == "B":
            self.move_left()
        elif self.game_mode == "C":
            self.move_left()

    def move_red(self):
        if self.game_mode == "A":
            self.move_right()
        elif self.game_mode == "B":
            self.move_right()
        elif self.game_mode == "C":
            self.move_right()

    def move_green(self):
        if self.game_mode == "A":
            self.move_up()
        elif self.game_mode == "B":
            self.move_up()
        elif self.game_mode == "C":
            self.move_up()

    def move_yellow(self):
        if self.game_mode == "A":
            self.move_down()
        elif self.game_mode == "B":
            self.move_down()
        elif self.game_mode == "C":
            self.move_down()

if __name__ == "__main__":
    game = Game()
    game.mainloop()