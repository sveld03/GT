from modeTemplate import *

class ModeA(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

    # Move dot right, then record blue button click
    def move_blue(self):
        self.move_right(self.freqprof)
        self.screen.button_states['btnB'] = 1

    # Move dot left, then record red button click
    def move_red(self):
        self.move_left()
        self.screen.button_states['btnR'] = 1
    
    # Move dot up, then record green button click
    def move_green(self):
        self.move_up()
        self.screen.button_states['btnG'] = 1

    # Move dot down, then record yellow button click
    def move_yellow(self):
        self.move_down()
        self.screen.button_states['btnY'] = 1