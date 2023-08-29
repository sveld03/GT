from modeTemplate import *

import random

class Mode2(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

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

    def move_green(self):
        pass

    def move_yellow(self):
        pass