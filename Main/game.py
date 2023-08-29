# Screen and utilities
from infrastructure import *

# Game modes
from modeA import ModeA
from modeB import ModeB
from modeC import ModeC
from mode1 import Mode1
from mode2 import Mode2

import pandas as pd

# Data visualization
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

# Links menu to game modes, and initializes appropriate game mode when menu item clicked
class Game:
    def __init__(self, screen):
        
        # Initialize static screen
        self.screen = screen
        self.mode_label = 'None'
        self.screen.game_mode = None

        self.processing_thread = None
        self.processing_interval = 0.1  # seconds

        # Link menu commands
        self.screen.game_menu.add_command(label='A', command=self.modeA) 
        self.screen.game_menu.add_command(label='B', command=self.modeB)
        self.screen.game_menu.add_command(label='C', command=self.modeC)
        self.screen.game_menu.add_command(label='1', command=self.mode1)
        self.screen.game_menu.add_command(label='2', command=self.mode2)

        # database connection
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        atexit.register(self.freqprof.close)

    def process_data(self):
        while True:
            start_time = time()

            self.screen.event_generate("<<DataProcessed>>", when="tail")

            elapsed_time = time() - start_time

            if elapsed_time < self.processing_interval:
                sleep(self.processing_interval - elapsed_time)

    def update_data_table(self):
        if self.processing_thread is None:
            self.processing_thread = threading.Thread(target=self.process_data)
            self.processing_thread.start()

        self.screen.after(int(self.processing_interval * 1000), self.update_data_table)

    def handle_data(self, event):
        click = False
        if self.screen.button_states['btnB'] == 1 and self.screen.run == True:
            record_blue(self.Cursor, self.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
            click = True
        if self.screen.button_states['btnR'] == 1 and self.screen.run == True:
            record_red(self.Cursor, self.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
            click = True
        if self.screen.button_states['btnG'] == 1 and self.screen.run == True:
            record_green(self.Cursor, self.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
            click = True
        if self.screen.button_states['btnY'] == 1 and self.screen.run == True:
            record_yellow(self.Cursor, self.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
            click = True
        if click == False and self.screen.run == True:
            record_none(self.Cursor, self.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())

        for button in self.screen.button_states:
            self.screen.button_states[button] = 0

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode A")
        timer = Timer()
        self.mode_label = 'A'
        self.screen.game_mode = ModeA(self.freqprof, self.Cursor, self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

        self.update_data_table()

    # Mode B: a specific sequence of 4 button presses moves dot right
    def modeB(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode B")
        timer = Timer()
        self.mode_label = 'B'
        self.screen.game_mode = ModeB(self.freqprof, self.Cursor, self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

        self.update_data_table()

    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode C")
        timer = Timer()
        self.mode_label = 'C'
        self.screen.game_mode = ModeC(self.freqprof, self.Cursor, self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

        self.update_data_table()

    # Mode 1: simplest probabilistic game
    def mode1(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode 1")
        timer = Timer()
        self.mode_label = '1'
        self.screen.game_mode = Mode1(self.freqprof, self.Cursor, self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

        self.update_data_table()

    # Mode C: probability swap between two buttons
    def mode2(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode 2")
        timer = Timer()
        self.mode_label = '2'
        self.screen.game_mode = Mode2(self.freqprof, self.Cursor, self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

        self.update_data_table()

# Run the game
if __name__ == "__main__":

    # testRoot = Tk()
    # testRoot.title("real-time test")

    screen = screen()
    game = Game(screen)

    game.screen.bind("<<DataProcessed>>", game.handle_data)

    # timer = Timer()
    # minigame = ModeA(game.screen.btnB, game.screen.btnR, game.screen.btnG, game.screen.btnY, game.screen.move_left, game.screen.move_right, game.screen.move_up, game.screen.move_down, game.screen, timer)
    # ani = FuncAnimation(plt.gcf(), minigame.animate, interval=500)
    # plt.show()
    # testRoot.mainloop()

    game.screen.mainloop()
