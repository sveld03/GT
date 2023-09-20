from modeTemplate import *

# To make success a matter of probability
import random

# probability swap between two buttons (first red is high, then blue is high)
class Mode2(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

    def move_blue(self):
        super().move_blue()

        # If the dot is on the left half of the screen, blue has a 1/10 chance of working; on the right side it has a 1/3 chance
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 10)
        else:
            randVal = random.randrange(1, 3)
        if randVal == 1:
            super().move_right()

    def move_red(self):
        super().move_red()

        # If the dot is on the left half of the screen, blue has a 1/3 chance of working; on the right side it has a 1/10 chance
        if self.screen.canvas.coords(self.screen.dot)[0] <= 500:
            randVal = random.randrange(1, 3)
        else:
            randVal = random.randrange(1, 10)
        if randVal == 1:
            super().move_right()