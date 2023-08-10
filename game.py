from infrastructure import *

from modeA import ModeA
from modeB import ModeB
from modeC import ModeC
from mode1 import Mode1
from mode2 import Mode2

class Game:
    def __init__(self, screen):
        
        self.screen = screen

        self.game_mode = None

        self.screen.game_menu.add_command(label='A', command=self.modeA) 
        self.screen.game_menu.add_command(label='B', command=self.modeB)
        self.screen.game_menu.add_command(label='C', command=self.modeC)
        self.screen.game_menu.add_command(label='1', command=self.mode1)
        self.screen.game_menu.add_command(label='2', command=self.mode2)

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode A")
        timer = Timer()
        self.game_mode = ModeA(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

    # Mode B: a specific sequence of 4 button presses moves dot right
    def modeB(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode B")
        timer = Timer()
        self.game_mode = ModeB(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

    # Mode C: double-click green for 1st half, red-yellow for 2nd half
    def modeC(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode C")
        timer = Timer()
        self.game_mode = ModeC(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

    # Mode 1: simplest probabilistic game
    def mode1(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode 1")
        timer = Timer()
        self.game_mode = Mode1(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

    # Mode C: probability swap between two buttons
    def mode2(self):
        self.screen.reset()
        self.screen.mode_label.config(text="Game Mode 2")
        timer = Timer()
        self.game_mode = Mode2(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down, self.screen, timer)
        self.screen.congrats.place_forget()

if __name__ == "__main__":
    screen = canvas()
    game = Game(screen)
    game.screen.mainloop()
