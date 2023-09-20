""" Infrastructure file -- base file to be imported by essentially all other files"""

# Graphics
from tkinter import *

# general tools used in other files
import itertools
import sys

# Database -- used in game.py, which imports this file
import sqlite3
import atexit

# Timer
from time import *

# Data Visualization
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import TimedAnimation

# To be used in modeTemplate.py
import queue

# Global constants
MAX_FRAMES = 3000 # stop the animation after 300 seconds
PREDICTION_TIME = 1 # how many seconds ahead we are predicting
SLOPERANGE = 2 # the number of frames over which we calculate the slope; right now it is at the lowest possible value

# Hyperparameters for application of parameters -- changing these values will affect how much the curves will fluctuate at a given parameter value
HYPER_BETA_APP = 2
HYPER_BETA_APP_INIT = .01
HYPER_EP_APP = 5
# HYPER_ALPH_APP = 10 -- commented because we are no longer using alpha/reinforcement, left in just in case we want to reimplement
HYPER_RESURG_IMMED_APP = 5
HYPER_RESURG_DELAY_APP = 5

# Hyperparameters for changing parameters -- changing these values will affect how quickly the parameters change value in response to frequency profile feedback
HYPER_EP_CHANGE = 5
# HYPER_ALPH_CHANGE = 30
HYPER_RESURG_CHANGE = 5
HYPER_AUTO_CHANGE = 10
HYPER_BETA_CHANGE = 20

# Hyperparameters for rule changes 
HYPER_DROP_SUBTRACT = 0.01 # not in use right now, the value we subtract from a falling curve after a rule change (now we are just removing dominance)
HYPER_DROP_LENGTH = 3 # the amount of time that the dominance effect is forcefully subdued after a rule change


# Game display: canvas, buttons, menu, etc.
class Screen(Tk):
    
    # When an instance of this class is created, it initializes a tkinter application with visuals already filled in
    def __init__(self):
        super().__init__()

        # game title
        self.title("The Hard Easy Game")

        # set geometry (widthxheight)
        self.geometry('1360x710')
        self.resizable(width=False, height=False)

        # instructions
        subtitle = Label(self, text = "Click the buttons to get the dot to the right side of the screen. Have fun! :)")
        subtitle.place(anchor='nw')

        # Game mode
        self.mode_char = '0'
        self.mode_label = Label(self, text='')
        self.mode_label.place(x=800, y=75)

        # Create canvas
        self.canvas = Canvas(self, bg="white", width=1250, height = 450)
        self.canvas.place(x=50, y=150)

        # initial position of dot
        dot_radius = 20
        self.init_x1 = 50 - dot_radius
        self.init_y1 = 225 - dot_radius
        self.init_x2 = 50 + dot_radius
        self.init_y2 = 225 + dot_radius

        # create dot, which user will move around canvas
        self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
                         self.init_x2, self.init_y2,
                         outline='red', fill='red')
        
        # Finish line and label
        self.line = self.canvas.create_line(1225, 0, 1225, 500)
        self.finish = Label(self, text="Finish Line")
        self.finish.place(x=1235, y=125)

        # Hidden congratulations label, will appear when game is completed
        self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')

        # Create buttons and menu
        self.create_buttons()
        # self.create_menu()

    # Creates 4 buttons, which start with no function and have different functions in each game mode (user can click buttons to move dot)
    def create_buttons(self):

        # 4 button colors: blue, red, green, yellow
        self.btnB = Button(self, width='14', height='6', bg='blue')
        self.btnR = Button(self, width='14', height='6', bg='red')
        self.btnG = Button(self, width='14', height='6', bg='green')
        self.btnY = Button(self, width='14', height='6', bg='yellow')

        # Place buttons next to each other above canvas
        self.btnB.place(x='75', y='30')
        self.btnR.place(x='200', y='30')
        self.btnG.place(x='325', y='30')
        self.btnY.place(x='450', y='30')

        # in case something goes wrong the researcher can tell the user to click this button
        self.stop = Button(self, width='9', height='4', bg='red', text="Stop Graph", command=self.stopGraph)
        self.stop.place(x='1200', y='25')

    # stops the predictions
    def stopGraph(self):
        self.event_generate("<<stopGraph>>")
    
    # Resets screen: game mode, button functions, dot position
    def reset(self):

        # Calculate how far dot is from starting position
        x1, y1, x2, y2 = self.canvas.coords(self.dot)
        dx = self.init_x1 - x1
        dy = self.init_y1 - y1

        # Move dot to starting position
        self.canvas.move(self.dot, dx, dy)

        # Reset game mode and buttons
        self.btnB.config(command=self.do_nothing)
        self.btnR.config(command=self.do_nothing)
        self.btnG.config(command=self.do_nothing)
        self.btnY.config(command=self.do_nothing)

    # Arbitrary button to reset buttons
    def do_nothing(self):
        pass

# Timer starts running when a game mode begins and the first button is clicked, keeps track of how much time has elapsed
class Timer:
    def __init__(self):
        self.start_time = time()
    def time_elapsed(self):
        current_time = time()
        elapsed = current_time - self.start_time
        return elapsed

# rounds down to the nearest tenth
def truncate_after_first_decimal(number):
    str_number = str(number)
    decimal_index = str_number.find('.')
    
    if decimal_index != -1:
        truncated_number = str_number[:decimal_index + 2]  # Include the decimal point and one digit
        return float(truncated_number)
    else:
        return number


""" Record functions store data in the FreqProf database, which is no longer really used for anything but good to have the raw data somewhere"""

# Records blue botton clicks
def record_blue(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks blue button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    
    Cursor.execute('SELECT time FROM FreqProf WHERE name=? AND mode=? and trial=? ORDER BY id DESC LIMIT 1', (name, game_mode, trial))
    last_time = Cursor.fetchone()
    cur_time = truncate_after_first_decimal(timer.time_elapsed())
    if last_time is not None and cur_time > float(last_time[0]) + .18:
        Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time - .1, trial))
    
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(1, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time, trial))
    freqprof.commit()

# Records red button clicks
def record_red(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks red button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    
    Cursor.execute('SELECT time FROM FreqProf WHERE name=? AND mode=? and trial=? ORDER BY id DESC LIMIT 1', (name, game_mode, trial))
    last_time = Cursor.fetchone()
    cur_time = truncate_after_first_decimal(timer.time_elapsed())
    if last_time is not None and cur_time > float(last_time[0]) + .18:
        Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time - .1, trial))
    
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 1, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time, trial))
    freqprof.commit()

# Records green button clicks
def record_green(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks green button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    
    Cursor.execute('SELECT time FROM FreqProf WHERE name=? AND mode=? and trial=? ORDER BY id DESC LIMIT 1', (name, game_mode, trial))
    last_time = Cursor.fetchone()
    cur_time = truncate_after_first_decimal(timer.time_elapsed())
    if last_time is not None and cur_time > float(last_time[0]) + .18:
        Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time - .1, trial))
    
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 1, 0, ?, ?, ?, ?)', (game_mode, name, cur_time, trial))
    freqprof.commit()

# Records yellow button clicks
def record_yellow(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks yellow button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    
    Cursor.execute('SELECT time FROM FreqProf WHERE name=? AND mode=? and trial=? ORDER BY id DESC LIMIT 1', (name, game_mode, trial))
    last_time = Cursor.fetchone()
    cur_time = truncate_after_first_decimal(timer.time_elapsed())
    if last_time is not None and cur_time > float(last_time[0]) + .18:
        Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time - .1, trial))
    
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 1, ?, ?, ?, ?)', (game_mode, name, cur_time, trial))
    freqprof.commit()

# Whenever a tenth of a second passes with no button clicks, this function is called
def record_none(Cursor, freqprof, timer, game_mode, name, trial):
    
    Cursor.execute('SELECT time FROM FreqProf WHERE name=? AND mode=? and trial=? ORDER BY id DESC LIMIT 1', (name, game_mode, trial))
    last_time = Cursor.fetchone()
    cur_time = truncate_after_first_decimal(timer.time_elapsed())
    if last_time is not None and cur_time > float(last_time[0]) + .18:
        Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time - .1, trial))
    
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, cur_time, trial))
    freqprof.commit()
        