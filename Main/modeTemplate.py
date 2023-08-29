# Base class for all game modes

# Screen and utilities
from infrastructure import *

from abc import ABC, abstractmethod

# Game mode A: simplest version, blue button moves dot right
class ModeTemplate:
    def __init__(self, freqprof, cursor, screen, timer):
        
        self.screen = screen
        screen.run = True
        
        # Get access to buttons on screen
        self.btnB = self.screen.btnB
        self.btnR = self.screen.btnR
        self.btnG = self.screen.btnG
        self.btnY = self.screen.btnY

        # Get access to movement functions
        self.move_left = self.screen.move_left
        self.move_right = self.screen.move_right
        self.move_up = self.screen.move_up
        self.move_down = self.screen.move_down

        # Game stopwatch
        self.timer = timer

        # Assign movement functions to buttons
        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

        # Connect to database
        self.freqprof = freqprof
        self.Cursor = cursor

        self.button_clicks = {"Up": 0, "Down": 0, "Left": 0, "Right": 0}
        self.timestamps = []

    def update_clicks(self, button):
        self.button_clicks[button] += 1
        self.timestamps.append(time())

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
    @abstractmethod
    def move_blue(self):
        pass

    # Move dot left, then record red button click
    @abstractmethod
    def move_red(self):
        pass
    
    # Move dot up, then record green button click
    @abstractmethod
    def move_green(self):
        pass

    # Move dot down, then record yellow button click
    @abstractmethod
    def move_yellow(self):
        pass

    
    def plot_data(self):
        plt.bar(self.button_clicks.keys(), self.button_clicks.values())
        plt.xlabel("Button")
        plt.ylabel("Click Count")
        plt.title("Button Click Count")
        plt.show
    
    def animate(self):
        self.current_time = time.time()
        while self.timestamps and self.current_time - self.timestamps[0] > 0.5:
            self.timestamp = self.timestamps.pop(0)
            for button, count in self.button_cloicks.items():
                print(f"{button}: {count}")
            self.plot_data()