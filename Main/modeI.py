from modeTemplate import *

# Simplest mode of all -- blue works
class ModeI(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

    # Move dot right, then record blue button click
    def move_blue(self):
        super().move_blue()
        super().move_right()