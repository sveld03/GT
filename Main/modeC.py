from modeTemplate import *

# double-click green for 1st half, red-yellow for 2nd half
class ModeC(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        # When buttons are clicked they are appended to the input sequence, which is compared against the move sequences to see if the last 2 values match
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

        # If on the first half of the screen and green was clicked twice in a row, move the dot right
        if self.input_seq[-2:] == self.move_seq1 and self.screen.canvas.coords(self.screen.dot)[0] <= 575:
            super().move_right()
            super().move_right()
            self.input_seq = []

    def move_yellow(self):
        super().move_yellow()
        self.input_seq.append('y')

        # If on the second half of the screen and red was clicked before yellow, move the dot right
        if self.input_seq[-2:] == self.move_seq2 and self.screen.canvas.coords(self.screen.dot)[0] > 575:
            super().move_right()
            super().move_right()