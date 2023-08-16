# Screen and utilities
from infrastructure import *

# import matplotlib.pyplot as plt

# Game mode A: simplest version, blue button moves dot right
class ModeA:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        # Get access to buttons on screen
        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        # Get access to movement functions
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        # Get access to remaining screen functions
        self.screen = screen

        # Game stopwatch
        self.timer = timer

        # Connect to database
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        # Object that can convert game data to CSV
        self.converter = Converter(self.screen.nameNtr.get(), 'A', self.screen.trialNtr.get()) 

        # Beginning of F-tier frequency profile -- ideally we don't need this
        self.blueFreq = plt.plot(0, 0, 'b', linestyle='solid', label="test")
        plt.show(block=False)

        # Assign movement functions to buttons
        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()


    # Button assignment functions; same for all game modes

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def assign_btnG(self):
        self.btnG.config(command=self.move_green)

    def assign_btnY(self):
        self.btnY.config(command=self.move_yellow)


    # Button movement functions: different across game modes

    # Move dot right, then record blue button click
    def move_blue(self):
        self.move_right(self.freqprof, self.converter)
        record_blue(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()), plt)

    # Move dot left, then record red button click
    def move_red(self):
        self.move_left()
        record_red(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))
    
    # Move dot up, then record green button click
    def move_green(self):
        self.move_up()
        record_green(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    # Move dot down, then record yellow button click
    def move_yellow(self):
        self.move_down()
        record_yellow(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))