from tkinter import *

import sqlite3

from time import *

# table name: FreqProf
# table columns: id (int -- primary key), B1 (int), B2 (int), B3 (int), B4 (int), B5, time (REAL), mode, name, trial

# Cursor.execute('CREATE TABLE FreqProf (id INTEGER PRIMARY KEY AUTOINCREMENT, B1 INTEGER, B2 INTEGER, B3 INTEGER, B4 INTEGER, B5 INTEGER, time REAL)')

class canvas(Tk):
    def __init__(self):
        super().__init__()
        

        # game title
        self.title("The Hard Easy Game")

        # set geometry (widthxheight)
        self.geometry('1360x710')

        self.resizable(width=False, height=False)

        # instructions
        subtitle = Label(self, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
        subtitle.place(anchor='nw')

        self.nameLbl = Label(self, text="Enter your name here: ")
        self.nameLbl.place(x=750, y=25)
        self.nameNtr = Entry(self, width=10)
        self.nameNtr.place(x=880, y=25)

        self.trialLbl = Label(self, text = "Trial: ")
        self.trialLbl.place(x=1000, y=25)
        self.trialNtr = Entry(self, width=10)
        self.trialNtr.place(x=1050, y=25)
        self.trialNtr.insert(0, '1')

        self.mode_label = Label(self, text='')
        self.mode_label.place(x=800, y=75)

        self.canvas = Canvas(self, bg="white", width=1250, height = 450)
        self.canvas.place(x=50, y=150)

        # initial position of dot
        dot_radius = 20
        self.init_x1 = 50 - dot_radius
        self.init_y1 = 225 - dot_radius
        self.init_x2 = 50 + dot_radius
        self.init_y2 = 225 + dot_radius

        # create dot
        self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
                         self.init_x2, self.init_y2,
                         outline='red', fill='red')
        
        self.line = self.canvas.create_line(1225, 0, 1225, 500)

        self.finish = Label(self, text="Finish Line")
        self.finish.place(x=1235, y=125)

        self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')

        self.create_buttons()
        self.create_menu()

    def create_buttons(self):
        self.btnB = Button(self, width='14', height='6', bg='blue')
        self.btnR = Button(self, width='14', height='6', bg='red')
        self.btnG = Button(self, width='14', height='6', bg='green')
        self.btnY = Button(self, width='14', height='6', bg='yellow')

        self.btnB.place(x='75', y='30')
        self.btnR.place(x='200', y='30')
        self.btnG.place(x='325', y='30')
        self.btnY.place(x='450', y='30')

    def create_menu(self):
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.game_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Game Modes", menu=self.game_menu)
    
    def reset(self):
        x1, y1, x2, y2 = self.canvas.coords(self.dot)
        dx = self.init_x1 - x1
        dy = self.init_y1 - y1
        self.canvas.move(self.dot, dx, dy)

    def check_completion(self, conn):
        if self.canvas.coords(self.dot)[2] >= 1225:
            self.game_mode = None
            self.congrats.place(x=50, y=625)
            self.reset()
            conn.close()

    def move_left(self):
        if self.canvas.coords(self.dot)[0] > 0:
            self.canvas.move(self.dot, -20, 0)

    def move_right(self, conn):
        if self.canvas.coords(self.dot)[2] < 1250:
            self.canvas.move(self.dot, 20, 0)
            self.check_completion(conn)

    def move_up(self):
        if self.canvas.coords(self.dot)[1] > 0:
            self.canvas.move(self.dot, 0, -20)

    def move_down(self):
        if self.canvas.coords(self.dot)[3] < 500:
            self.canvas.move(self.dot, 0, 20)

class Timer:
    def __init__(self):
        self.start_time = time()
    def time_elapsed(self):
        current_time = time()
        elapsed = current_time - self.start_time
        return elapsed

def record_blue(Cursor, freqprof, timer, game_mode, name, trial):
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(1, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()

def record_red(Cursor, freqprof, timer, game_mode, name, trial):
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 1, 0, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()

def record_green(Cursor, freqprof, timer, game_mode, name, trial):
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 1, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()

def record_yellow(Cursor, freqprof, timer, game_mode, name, trial):
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 1, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()
        