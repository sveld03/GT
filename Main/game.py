# Screen and utilities
from infrastructure import *
from params import *

# Game modes
from modeA import ModeA
from modeB import ModeB
from modeC import ModeC
from modeD import ModeD
from mode1 import Mode1
from mode2 import Mode2

import pandas as pd

# Data visualization
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

# Links menu to game modes, and initializes appropriate game mode when menu item clicked
class Game:
    def __init__(self, screen, params):
        
        # Initialize static screen
        self.screen = screen
        self.game_mode = None

        self.params = params

        # Link menu commands
        # self.screen.game_menu.add_command(label='A', command=self.modeA) 
        # self.screen.game_menu.add_command(label='B', command=self.modeB)
        # self.screen.game_menu.add_command(label='C', command=self.modeC)
        # self.screen.game_menu.add_command(label='1', command=self.mode1)
        # self.screen.game_menu.add_command(label='2', command=self.mode2)

        # database connection
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        # self.Cursor.execute('CREATE TABLE Frequencies (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mode TEXT, trial TEXT, time REAL, B1 REAL, B2 REAL, B3 REAL, B4 REAL)')
        # self.Cursor.execute('CREATE TABLE Probabilities (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mode TEXT, trial TEXT, time REAL, B1 REAL, B2 REAL, B3 REAL, B4 REAL)')
        # self.Cursor.execute('CREATE TABLE Accuracies (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mode TEXT, trial TEXT, time REAL, B1 REAL, B2 REAL, B3 REAL, B4 REAL, mean REAL, cumulative REAL)')
        # self.Cursor.execute('CREATE TABLE upParameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mode TEXT, trial TEXT, time REAL, alpha REAL, beta REAL, l12 REAL, l13 REAL, l14 REAL, l21 REAL, l23 REAL, l24 REAL, l31 REAL, l32 REAL, l34 REAL, l41 REAL, l42 REAL, l43 REAL)')
        # self.Cursor.execute('CREATE TABLE downParameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mode TEXT, trial TEXT, time REAL, epsilon REAL, p12 REAL, p13 REAL, p14 REAL, p21 REAL, p23 REAL, p24 REAL, p31 REAL, p32 REAL, p34 REAL, p41 REAL, p42 REAL, p43 REAL)')
        # self.Cursor.execute('DROP TABLE IF EXISTS Accuracies')
        # self.Cursor.execute('DROP TABLE IF EXISTS Frequencies')
        # self.Cursor.execute('DROP TABLE IF EXISTS Probabilities')
        # self.Cursor.execute('DROP TABLE IF EXISTS Parameters')

        # self.freqprof.commit()

        self.params.bind("<<startGame>>", self.start)

        atexit.register(self.freqprof.close)

    def start(self, event):
        if self.params.mode.get() == "A":
            self.modeA()
        elif self.params.mode.get() == "B":
            self.modeB()
        elif self.params.mode.get() == "C":
            self.modeC()
        elif self.params.mode.get() == "D":
            self.modeD()
        elif self.params.mode.get() == "1":
            self.mode1()
        elif self.params.mode.get() == "2":
            self.mode2()
        else:
            print("Error: no game mode selected.")
            quit()

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        self.screen.mode_label.config(text="Game Mode A")
        self.screen.mode_char = 'A'
        timer = Timer()
        self.game_mode = ModeA(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")
        # self.game_mode.start()

    # Mode B: a specific sequence of 4 button presses moves dot right
    def modeB(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode B")
        self.screen.mode_char = 'B'
        self.game_mode = ModeB(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")
        # self.game_mode.start()

    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode C")
        self.screen.mode_char = 'C'
        self.game_mode = ModeC(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")
        # self.game_mode.start()

    # Mode D: meant to produce the first two curves of the Default Probability Profile (DPP)
    def modeD(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode D")
        self.screen.mode_char = 'D'
        self.game_mode = ModeD(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    def modeE(self):
        pass

    # Mode 1: simplest probabilistic game
    def mode1(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode 1")
        self.screen.mode_char = '1'
        self.game_mode = Mode1(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")
        # self.game_mode.start()

    # Mode 2: probability swap between two buttons
    def mode2(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode 2")
        self.screen.mode_char = '2'
        self.game_mode = Mode2(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")
        # self.game_mode.start()

# Run the game
if __name__ == "__main__":

    # testRoot = Tk()
    # testRoot.title("real-time test")

    screen = Screen()
    params = Params()
    game = Game(screen, params)
    # game.screen.mainloop()
