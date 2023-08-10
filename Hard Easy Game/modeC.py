from canvas import *

class ModeC:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.screen = screen

        self.input_seq = []
        self.move_seq1 = ['g', 'g']
        self.move_seq2 = ['r', 'y']
        
        self.timer = timer

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
        record_blue(self.timer)

    def move_red(self):
        self.input_seq.append('r')
        record_red(self.timer)
    
    def move_green(self):
        self.input_seq.append('g')
        if self.input_seq[-2:] == self.move_seq1 and self.screen.canvas.coords(self.screen.dot)[0] <= 575:
            self.move_right()
            self.move_right()
            self.input_seq = []
        record_green(self.timer)

    def move_yellow(self):
        self.input_seq.append('y')
        if self.input_seq[-2:] == self.move_seq2 and self.screen.canvas.coords(self.screen.dot)[0] > 575:
            self.move_right()
            self.move_right()
        record_yellow(self.timer)