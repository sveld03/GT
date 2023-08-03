from canvas import *

import random

class Mode2:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.assign_btnB()
        self.assign_btnR()

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.screen = screen

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def move_blue(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 10)
        else:
            randVal = random.randrange(1, 3)
        if randVal == 1:
            self.move_right()

    def move_red(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 3)
        else:
            randVal = random.randrange(1, 10)
        if randVal == 1:
            self.move_right()