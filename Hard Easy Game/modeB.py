from canvas import *

class ModeB:
    def __init__(self, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, timer):

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

        self.input_seq = []
        self.move_seq = ['g', 'y', 'r', 'b']

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
        self.move_up()
        if self.input_seq[-4:] == self.move_seq:
            for num in range(4):
                self.move_right()
        record_blue(self.timer)

    def move_red(self):
        self.input_seq.append('r')
        self.move_down()
        record_red(self.timer)
    
    def move_green(self):
        self.input_seq.append('g')
        self.move_down()
        record_green(self.timer)

    def move_yellow(self):
        self.input_seq.append('y')
        self.move_up()
        record_yellow(self.timer)