from infrastructure import *

import random

class Mode2:
    def __init__(self, freqprof, cursor, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.screen = screen
        screen.run = True

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.timer = timer

        # self.converter = Converter(self.screen.nameNtr.get(), '2', self.screen.trialNtr.get()) 

        self.assign_btnB()
        self.assign_btnR()

        # Connect to database
        self.freqprof = freqprof
        self.Cursor = cursor

        self.button_clicks = {"Up": 0, "Down": 0, "Left": 0, "Right": 0}
        self.timestamps = []

    def update_clicks(self, button):
        self.button_clicks[button] += 1
        self.timestamps.append(time())

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)
        self.screen.button_states['btnB'] = 1

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)
        self.screen.button_states['btnR'] = 1

    def move_blue(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 10)
        else:
            randVal = random.randrange(1, 3)
        if randVal == 1:
            self.move_right(self.freqprof)
        self.screen.button_states['btnG'] = 1

    def move_red(self):
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 3)
        else:
            randVal = random.randrange(1, 10)
        if randVal == 1:
            self.move_right(self.freqprof)
        self.screen.button_states['btnY'] = 1