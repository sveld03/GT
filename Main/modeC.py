from modeTemplate import *

class ModeC(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

        self.input_seq = []
        self.move_seq1 = ['g', 'g']
        self.move_seq2 = ['r', 'y']

    def move_blue(self):
        self.input_seq.append('b')
        self.screen.button_states['btnB'] = 1

    def move_red(self):
        self.input_seq.append('r')
        self.screen.button_states['btnR'] = 1
    
    def move_green(self):
        self.input_seq.append('g')
        if self.input_seq[-2:] == self.move_seq1 and self.screen.canvas.coords(self.screen.dot)[0] <= 575:
            self.move_right(self.freqprof)
            self.move_right(self.freqprof)
            self.input_seq = []
        self.screen.button_states['btnG'] = 1

    def move_yellow(self):
        self.input_seq.append('y')
        if self.input_seq[-2:] == self.move_seq2 and self.screen.canvas.coords(self.screen.dot)[0] > 575:
            self.move_right(self.freqprof)
            self.move_right(self.freqprof)
        self.screen.button_states['btnY'] = 1