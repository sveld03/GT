# Screen and utilities
from infrastructure import *

# Game modes
from modeA import ModeA
from modeB import ModeB
from modeC import ModeC
from mode1 import Mode1
from mode2 import Mode2

from params import *

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

        self.begin = False

        self.params = params

        # Link menu commands
        self.screen.game_menu.add_command(label='A', command=self.modeA) 
        self.screen.game_menu.add_command(label='B', command=self.modeB)
        self.screen.game_menu.add_command(label='C', command=self.modeC)
        self.screen.game_menu.add_command(label='1', command=self.mode1)
        self.screen.game_menu.add_command(label='2', command=self.mode2)

        # database connection
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        self.params.bind("<<startGame>>", self.start)

        atexit.register(self.freqprof.close)

    def start(self, event):
        self.begin = True

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        if self.begin == True:
            self.screen.reset()
            self.screen.congrats.place_forget()
            timer = Timer()
            self.screen.mode_label.config(text="Game Mode A")
            self.screen.mode_char = 'A'
            self.game_mode = ModeA(self.freqprof, self.Cursor, self.screen, timer, self.params.get_window())
            self.game_mode.start()

    # Mode B: a specific sequence of 4 button presses moves dot right
    def modeB(self):
        if self.begin == True:
            self.screen.reset()
            self.screen.congrats.place_forget()
            timer = Timer()
            self.screen.mode_label.config(text="Game Mode B")
            self.screen.mode_char = 'B'
            self.game_mode = ModeB(self.freqprof, self.Cursor, self.screen, timer, self.params.get_window())
            self.game_mode.start()

    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        if self.begin == True:
            self.screen.reset()
            self.screen.congrats.place_forget()
            timer = Timer()
            self.screen.mode_label.config(text="Game Mode C")
            self.screen.mode_char = 'C'
            self.game_mode = ModeC(self.freqprof, self.Cursor, self.screen, timer, self.get_window())
            self.game_mode.start()

    # Mode 1: simplest probabilistic game
    def mode1(self):
        if self.begin == True:
            self.screen.reset()
            self.screen.congrats.place_forget()
            timer = Timer()
            self.screen.mode_label.config(text="Game Mode 1")
            self.screen.mode_char = '1'
            self.game_mode = Mode1(self.freqprof, self.Cursor, self.screen, timer, self.get_window())
            self.game_mode.start()

    # Mode C: probability swap between two buttons
    def mode2(self):
        if self.begin == True:
            self.screen.reset()
            self.screen.congrats.place_forget()
            timer = Timer()
            self.screen.mode_label.config(text="Game Mode 2")
            self.screen.mode_char = '2'
            self.game_mode = Mode2(self.freqprof, self.Cursor, self.screen, timer, self.get_window())
            self.game_mode.start()

# Run the game
if __name__ == "__main__":

    # testRoot = Tk()
    # testRoot.title("real-time test")

    screen = Screen()
    game = Game(screen)
    game.screen.mainloop()
