from modeTemplate import *

class ModeB(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.input_seq = []
        self.move_seq = ['g', 'y', 'r', 'b']

    def move_blue(self):
        super().move_blue()
        self.input_seq.append('b')
        super().move_up()
        if self.input_seq[-4:] == self.move_seq:
            for num in range(4):
                super().move_right()

    def move_red(self):
        super().move_red()
        self.input_seq.append('r')
        super().move_down()
    
    def move_green(self):
        super().move_green()
        self.input_seq.append('g')
        super().move_down()

    def move_yellow(self):
        super().move_yellow()
        self.input_seq.append('y')
        super().move_up()