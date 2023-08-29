from infrastructure import *

class ModeB:
    def __init__(self, freqprof, cursor, btnB, btnR, btnG, btnY, move_left, move_right, move_up, move_down, screen, timer):

        self.btnB = btnB
        self.btnR = btnR
        self.btnG = btnG
        self.btnY = btnY

        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

        self.screen = screen
        screen.run = True

        self.input_seq = []
        self.move_seq = ['g', 'y', 'r', 'b']

        self.timer = timer

        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

        # Connect to database
        self.freqprof = freqprof
        self.Cursor = cursor

        self.button_clicks = {"Up": 0, "Down": 0, "Left": 0, "Right": 0}
        self.timestamps = []

    def update_clicks(self, button):
        self.button_clicks[button] += 1
        self.timestamps.append(time())

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