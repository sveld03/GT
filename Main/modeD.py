from modeTemplate import *

# Second blue button click moves the dot; after that red moves the dot
class ModeD(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.blueCounter = 0

    # Move dot right, then record blue button click
    def move_blue(self):
        super().move_blue()
        self.blueCounter += 1

        # If this is the second time the blue button has been clicked, move the dot
        if self.blueCounter == 2:
            super().move_right()
            self.blueCounter += 1

    # Move dot left, then record red button click
    def move_red(self):
        super().move_red()

        # So long as blue has already been clicked twice, move the dot
        if self.blueCounter > 2:
            super().move_right()