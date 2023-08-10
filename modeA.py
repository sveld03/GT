from infrastructure import *

class ModeA:
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

        self.timer = timer

        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

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
        self.move_right(self.freqprof)
        record_blue(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_red(self):
        self.move_left()
        record_red(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))
    
    def move_green(self):
        self.move_up()
        record_green(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))

    def move_yellow(self):
        self.move_down()
        record_yellow(self.Cursor, self.freqprof, self.timer, 'A', self.screen.nameNtr.get(), int(self.screen.trialNtr.get()))