from modeTemplate import *

import random

class Mode1(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

        self.blueCounter1 = 4
        self.blueDecrease1 = 1
        
        self.redCounter1 = 4
        self.redDecrease1 = 1
        
        self.yellowCounter1 = 4
        self.yellowDecrease1 = 1

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