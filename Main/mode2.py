from modeTemplate import *

import random

class Mode2(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

    def move_blue(self):
        super().move_blue()
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 10)
        else:
            randVal = random.randrange(1, 3)
        if randVal == 1:
            super().move_right()

    def move_red(self):
        super().move_red()
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 3)
        else:
            randVal = random.randrange(1, 10)
        if randVal == 1:
            super().move_right()