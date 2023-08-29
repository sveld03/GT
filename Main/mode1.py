from infrastructure import *

import random

class Mode1:
    def __init__(self, freqprof, cursor, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.screen = screen
        screen.run = True

        self.blueCounter1 = 4
        self.blueDecrease1 = 1
        
        self.redCounter1 = 4
        self.redDecrease1 = 1
        
        self.yellowCounter1 = 4
        self.yellowDecrease1 = 1

        self.timer = timer

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

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def assign_btnG(self):
        self.btnG.config(command=self.move_green)

    def assign_btnY(self):
        self.btnY.config(command=self.move_yellow)

    def move_blue(self):
        randVal = random.randrange(1, self.blueCounter1)
        # print("blue probability of success: 1/" + str(self.blueCounter1))
        if randVal == 1 and self.blueCounter1 < 10:
            self.move_right(self.freqprof)
            # print("success")
        self.blueDecrease1 += 1
        if self.blueDecrease1 % 4 == 0:
            self.blueCounter1 += 1
        self.screen.button_states['btnB'] = 1

    def move_red(self):
        randVal = random.randrange(1, self.redCounter1)
        if randVal == 1 and self.redCounter1 < 10:
            self.move_right(self.freqprof)
        self.redDecrease1 += 1
        if self.redDecrease1 % 4 == 0:
            self.redCounter1 += 1
        # print("red probability of success: 1/" + str(self.redCounter1))
        self.screen.button_states['btnR'] = 1
    
    def move_green(self):
        randVal = random.randrange(1, 3)
        if randVal == 1:
            self.move_right(self.freqprof)
        self.screen.button_states['btnG'] = 1

    def move_yellow(self):
        randVal = random.randrange(1, self.yellowCounter1)
        if randVal == 1 and self.yellowCounter1 < 10:
            self.move_right(self.freqprof)
        self.yellowDecrease1 += 1
        if self.yellowDecrease1 % 4 == 0:
            self.yellowCounter1 += 1
        # print("yellow probability of success: 1/" + str(self.yellowCounter1))
        self.screen.button_states['btnY'] = 1