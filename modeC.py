from infrastructure import *

class ModeC:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.screen = screen

        self.input_seq = []
        self.move_seq1 = ['g', 'g']
        self.move_seq2 = ['r', 'y']
        
        self.timer = timer

        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        self.converter = Converter(self.screen.nameNtr.get(), 'C', self.screen.trialNtr.get())

        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def assign_btnG(self):
        self.btnG.config(command=self.move_green)

    def assign_btnY(self):
        self.btnY.config(command=self.move_yellow)

    def move_blue(self):
        self.input_seq.append('b')
        record_blue(self.Cursor, self.freqprof, self.timer, 'C', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_red(self):
        self.input_seq.append('r')
        record_red(self.Cursor, self.freqprof, self.timer, 'C', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))
    
    def move_green(self):
        self.input_seq.append('g')
        if self.input_seq[-2:] == self.move_seq1 and self.screen.canvas.coords(self.screen.dot)[0] <= 575:
            self.move_right(self.freqprof, self.converter)
            self.move_right(self.freqprof, self.converter)
            self.input_seq = []
        record_green(self.Cursor, self.freqprof, self.timer, 'C', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_yellow(self):
        self.input_seq.append('y')
        if self.input_seq[-2:] == self.move_seq2 and self.screen.canvas.coords(self.screen.dot)[0] > 575:
            self.move_right(self.freqprof, self.converter)
            self.move_right(self.freqprof, self.converter)
        record_yellow(self.Cursor, self.freqprof, self.timer, 'C', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))