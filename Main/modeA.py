from modeTemplate import *

class ModeA(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

    # Move dot right, then record blue button click
    def move_blue(self):
        super().move_blue()
        super().move_right()

    # Move dot left, then record red button click
    def move_red(self):
        super().move_red()
        super().move_left()
    
    # Move dot up, then record green button click
    def move_green(self):
        super().move_green()
        super().move_up()

    # Move dot down, then record yellow button click
    def move_yellow(self):
        super().move_yellow()
        super().move_down()