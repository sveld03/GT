from modeTemplate import *

class ModeD(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.blueCounter = 0

    # Move dot right, then record blue button click
    def move_blue(self):
        super().move_blue()
        self.blueCounter += 1
        if self.blueCounter == 2:
            super().move_right()
            self.blueCounter += 1

    # Move dot left, then record red button click
    def move_red(self):
        super().move_red()
        if self.blueCounter > 2:
            super().move_right()