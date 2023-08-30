from modeTemplate import *

class ModeC(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

        self.input_seq = []
        self.move_seq1 = ['g', 'g']
        self.move_seq2 = ['r', 'y']

    def move_blue(self):
        super().move_blue()
        self.input_seq.append('b')

    def move_red(self):
        super().move_red()
        self.input_seq.append('r')
    
    def move_green(self):
        super().move_green()
        self.input_seq.append('g')
        if self.input_seq[-2:] == self.move_seq1 and self.screen.canvas.coords(self.screen.dot)[0] <= 575:
            super().move_right()
            super().move_right()
            self.input_seq = []

    def move_yellow(self):
        super().move_yellow()
        self.input_seq.append('y')
        if self.input_seq[-2:] == self.move_seq2 and self.screen.canvas.coords(self.screen.dot)[0] > 575:
            super().move_right()
            super().move_right()