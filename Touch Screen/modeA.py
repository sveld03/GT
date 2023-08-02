from utilities import *

from main import Game

class ModeA(Tk):
    def __init__(self):
        # super().__init__()

        # self.title("The Hard Easy Game: Mode A")

        # # set geometry (widthxheight)
        # self.geometry('1360x710')
        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

    def assign_btnB(self):
        Game.btnB.config(command=self.move_blue)

# if __name__ == "__main__":
#     game = ModeA()
#     game.mainloop()