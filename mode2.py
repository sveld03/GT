from infrastructure import *

import random

class Mode2:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.screen = screen

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.timer = timer

        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        self.converter = Converter(self.screen.nameNtr.get(), '2', self.screen.trialNtr.get()) 

        self.assign_btnB()
        self.assign_btnR()

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)
        record_blue(self.Cursor, self.freqprof, self.timer, '2', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)
        record_red(self.Cursor, self.freqprof, self.timer, '2', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_blue(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 10)
        else:
            randVal = random.randrange(1, 3)
        if randVal == 1:
            self.move_right(self.freqprof, self.converter)
        record_green(self.Cursor, self.freqprof, self.timer, '2', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_red(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 3)
        else:
            randVal = random.randrange(1, 10)
        if randVal == 1:
            self.move_right(self.freqprof, self.converter)
        record_yellow(self.Cursor, self.freqprof, self.timer, '2', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))