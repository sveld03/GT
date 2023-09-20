# Screen and utilities
from infrastructure import *
from params import *

# Game modes
from modeC import ModeC
from modeD import ModeD
from mode1 import Mode1
from mode2 import Mode2

from modeI import ModeI
from modeII import ModeII
from modeIII import ModeIII
from modeIV import ModeIV

# Data visualization -- imported in this file to be used in other files that import this file
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Links menu to game modes, and initializes appropriate game mode when menu item clicked
class Game:
    def __init__(self, screen, params):
        
        # Initialize static screen
        self.screen = screen
        self.game_mode = None

        # Stores data from the parameter input screen
        self.params = params

        # database connection
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        """ SQL commands to create and destroy tables; leaving these here in case it is ever necessary to update the structure of the tables"""
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

        # Triggers the start function when the researcher clicks "Start Game" on the parameter input screen
        self.params.bind("<<startGame>>", self.start)

        # Close the connection when the trial is over
        atexit.register(self.freqprof.close)

    # Trigger the initialization of the game mode corresponding to the radio button that was selected on the paramaters screen
    def start(self, event):
        if self.params.mode.get() == "C":
            self.modeC()
        elif self.params.mode.get() == "D":
            self.modeD()
        elif self.params.mode.get() == "1":
            self.mode1()
        elif self.params.mode.get() == "2":
            self.mode2()
        elif self.params.mode.get() == "I":
            self.modeI()
        elif self.params.mode.get() == "II":
            self.modeII()
        elif self.params.mode.get() == "III":
            self.modeIII()
        elif self.params.mode.get() == "IV":
            self.modeIV()
        else:
            print("Error: no game mode selected.")
            quit()

    """ Mode A turned into mode I, mode B was bad and got deleted"""
    
    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        self.screen.reset() # move the dot back to starting position
        self.screen.congrats.place_forget() # hide congrats message
        timer = Timer() # create the timer; timer won't start until first button is clicked
        self.screen.mode_label.config(text="Game Mode C") # Show the user what game mode they are playing
        self.screen.mode_char = 'C' # Backend storage of game mode info
        self.game_mode = ModeC(self.freqprof, self.Cursor, self.screen, timer, self.params) # Start the game
        self.screen.event_generate("<<startPrediction>>") # Prime the prediction graph to start running once a button is clicked

    # Mode D: meant to produce the first two curves of the Default Probability Profile (DPP) -- 2nd click of blue works, after that red works
    def modeD(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode D")
        self.screen.mode_char = 'D'
        self.game_mode = ModeD(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Mode 1: simplest probabilistic game -- green has high probability, the others have decreasing probability
    def mode1(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode 1")
        self.screen.mode_char = '1'
        self.game_mode = Mode1(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Mode 2: probability swap between two buttons (first red is high, then blue is high)
    def mode2(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode 2")
        self.screen.mode_char = '2'
        self.game_mode = Mode2(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Simplest mode of all -- blue works
    def modeI(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode I")
        self.screen.mode_char = 'I'
        self.game_mode = ModeI(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Blue works, then green works
    def modeII(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode II")
        self.screen.mode_char = 'II'
        self.game_mode = ModeII(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Yellow works, then red, then green
    def modeIII(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode III")
        self.screen.mode_char = 'III'
        self.game_mode = ModeIII(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

    # Red, yellow, red, yellow -- move functions 1/2 distance
    def modeIV(self):
        self.screen.reset()
        self.screen.congrats.place_forget()
        timer = Timer()
        self.screen.mode_label.config(text="Game Mode IV")
        self.screen.mode_char = 'IV'
        self.game_mode = ModeIV(self.freqprof, self.Cursor, self.screen, timer, self.params)
        self.screen.event_generate("<<startPrediction>>")

# Run the game
if __name__ == "__main__":

    screen = Screen()
    params = Params()
    game = Game(screen, params)
    # game.screen.mainloop()
