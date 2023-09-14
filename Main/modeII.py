from modeTemplate import *

class ModeII(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.blueCounter = 1

    # Move dot right, then record blue button click
    def move_blue(self):
        super().move_blue()
        self.blueCounter += 1
        if self.blueCounter <= 15:
            super().move_right()
            if self.blueCounter == 15:
                self.blueCounter += 1
                self.screen.event_generate("<<blueDrop>>")

    # Move dot left, then record red button click
    def move_green(self):
        super().move_green()
        if self.blueCounter > 15:
            super().move_right()