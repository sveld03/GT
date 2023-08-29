from modeTemplate import *

class ModeB(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer):
        super().__init__(freqprof, cursor, screen, timer)

        self.input_seq = []
        self.move_seq = ['g', 'y', 'r', 'b']

    def move_blue(self):
        self.input_seq.append('b')
        self.move_up()
        if self.input_seq[-4:] == self.move_seq:
            for num in range(4):
                self.move_right(self.freqprof)
        self.screen.button_states['btnB'] = 1

    def move_red(self):
        self.input_seq.append('r')
        self.move_down()
        self.screen.button_states['btnR'] = 1
    
    def move_green(self):
        self.input_seq.append('g')
        self.move_down()
        self.screen.button_states['btnG'] = 1

    def move_yellow(self):
        self.input_seq.append('y')
        self.move_up()
        self.screen.button_states['btnY'] = 1