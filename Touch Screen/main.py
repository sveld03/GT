from canvas import *

from modeA import ModeA

class Game:
    def __init__(self, screen):
        
        self.screen = screen

        self.game_mode = None

        self.screen.game_menu.add_command(label='A', command=self.modeA) 
        # self.screen.game_menu.add_command(label='B', command=self.modeB)
        # self.screen.game_menu.add_command(label='C', command=self.modeC)
        # self.screen.game_menu.add_command(label='1', command=self.mode1)

    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.screen.mode_label.config(text="Game Mode A")
        self.game_mode = ModeA(self.screen.btnB, self.screen.btnR, self.screen.btnG, self.screen.btnY, self.screen.move_left, self.screen.move_right, self.screen.move_up, self.screen.move_down)
        self.screen.congrats.place_forget()

    # # Mode B: a specific sequence of 4 button presses moves dot right
    # def modeB(self):
    #     self.game_mode = modeB()
    #     # self.congrats.place_forget()

    # # Mode C: double-click green for 1st half, red-yellow for 2nd half
    # def modeC(self):
    #     self.game_mode = modeC()
    #     # self.congrats.place_forget()

    # def mode1(self):
    #     self.game_mode = mode1()
    #     # self.congrats.place_forget()

if __name__ == "__main__":
    screen = canvas()
    game = Game(screen)
    game.screen.mainloop()
