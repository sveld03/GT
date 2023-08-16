# Graphics
from tkinter import *

# Database
import sqlite3

# Timer
from time import *

# Frequency Profile
from convert import *

# Data Visualization
import matplotlib.pyplot as plt

# Arrays
import numpy as np

# table name: FreqProf
# table columns: id (int -- primary key), B1 (int), B2 (int), B3 (int), B4 (int), B5, time (REAL), mode, name, trial

# Cursor.execute('CREATE TABLE FreqProf (id INTEGER PRIMARY KEY AUTOINCREMENT, B1 INTEGER, B2 INTEGER, B3 INTEGER, B4 INTEGER, B5 INTEGER, time REAL)')


# Game display: canvas, buttons, menu, etc.
class screen(Tk):
    
    # When an instance of this class is created, it initializes a tkinter application with visuals already filled in
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

        # User name
        self.nameLbl = Label(self, text="Enter your name here: ")
        self.nameLbl.place(x=750, y=25)
        self.nameNtr = Entry(self, width=10)
        self.nameNtr.place(x=880, y=25)

        # Trial number
        self.trialLbl = Label(self, text = "Trial: ")
        self.trialLbl.place(x=1000, y=25)
        self.trialNtr = Entry(self, width=10)
        self.trialNtr.place(x=1050, y=25)
        self.trialNtr.insert(0, '1')

        # Game mode
        self.game_mode = None
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
        self.create_menu()

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

    # Game mode menu
    def create_menu(self):
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.game_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Game Modes", menu=self.game_menu)
    
    # Resets screen: game mode, button functions, dot position
    def reset(self):

        # Calculate how far dot is from starting position
        x1, y1, x2, y2 = self.canvas.coords(self.dot)
        dx = self.init_x1 - x1
        dy = self.init_y1 - y1

        # Move dot to starting position
        self.canvas.move(self.dot, dx, dy)

        # Reset game mode and buttons
        self.game_mode = None
        self.btnB.config(command=self.do_nothing)
        self.btnR.config(command=self.do_nothing)
        self.btnG.config(command=self.do_nothing)
        self.btnY.config(command=self.do_nothing)

    # If the user has completed the game, this function says congrats, resets the screen, closes the database connection, and converts the game data to a CSV
    def check_completion(self, conn, conv):
        if self.canvas.coords(self.dot)[2] >= 1225:
            self.congrats.place(x=50, y=625)
            self.reset()
            conn.close()
            conv.convert()

    # Moves dot left
    def move_left(self):
        if self.canvas.coords(self.dot)[0] > 0:
            self.canvas.move(self.dot, -20, 0)

    # Moves dot right, then checks to see if the user has completed the game
    def move_right(self, conn, conv):
        if self.canvas.coords(self.dot)[2] < 1250:
            self.canvas.move(self.dot, 20, 0)
            self.check_completion(conn, conv)

    # Moves dot up
    def move_up(self):
        if self.canvas.coords(self.dot)[1] > 0:
            self.canvas.move(self.dot, 0, -20)

    # Moves dot down
    def move_down(self):
        if self.canvas.coords(self.dot)[3] < 500:
            self.canvas.move(self.dot, 0, 20)

    # Arbitrary button to reset buttons
    def do_nothing(self):
        x = 5

# Timer starts running when a game mode begins, keeps track of how much time has elapsed
class Timer:
    def __init__(self):
        self.start_time = time()
    def time_elapsed(self):
        current_time = time()
        elapsed = current_time - self.start_time
        return elapsed

# x_data = np.arange(0, 10, 1)
# y_data = np.random.rand(len(x_data))

# line, = plt.plot(x_data, y_data, 'b', linestyle='solid', label="test")
# plt.show(block=False)

# while True:
#     # Simulate gathering new data points
#     new_data_point = np.random.rand()
    
#     # Append the new data point to the existing data
#     x_data = np.append(x_data, x_data[-1] + 1)
#     y_data = np.append(y_data, new_data_point)
    
#     # Update the data of the line
#     line.set_data(x_data, y_data)
    
#     # Update the plot
#     plt.xlim(0, x_data[-1] + 1)  # Adjust the x-axis limits
#     plt.pause(1)  # Pause for a short time to allow the plot to update

# Records blue botton clicks
def record_blue(Cursor, freqprof, timer, game_mode, name, trial, plt):
    # When user clicks blue button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(1, 0, 0, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()
    # TO DO: when blue button is clicked, add this data point to the real-time frequency profile
    plt.plot(timer.time_elapsed(), 1, 'b', linestyle='solid')

# Records red button clicks
def record_red(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks red button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 1, 0, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()

# Records green button clicks
def record_green(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks green button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 1, 0, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()

# Records yellow button clicks
def record_yellow(Cursor, freqprof, timer, game_mode, name, trial):
    # When user clicks yellow button, this function inserts a row into the SQLite database, recording the click as a 1 and all the relevant game info
    Cursor.execute('INSERT INTO FreqProf(B1, B2, B3, B4, mode, name, time, trial) VALUES(0, 0, 0, 1, ?, ?, ?, ?)', (game_mode, name, timer.time_elapsed(), trial))
    freqprof.commit()
        