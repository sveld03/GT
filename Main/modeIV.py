from modeTemplate import *

# Red, yellow, red, yellow -- move functions 1/2 distance
class ModeIV(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.yellowCounter = 0
        self.redCounter = 0

    # Red button moves the dot in the 1st quarter and 3rd quarter, signalling a drop when it stops working
    def move_red(self):
        super().move_red()
        if self.redCounter <= 15:
            self.redCounter += 1
            super().move_right(20)
            if self.redCounter == 15:
                self.redCounter += 1
                self.screen.event_generate("<<redDrop>>")
        if self.yellowCounter > 15 and self.redCounter <= 30:
            self.redCounter += 1
            super().move_right(20)
            if self.redCounter == 30:
                self.redCounter += 1
                self.screen.event_generate("<<redDrop>>")

    # Yellow button moves the dot in the 2nd quarter and 4th quarter, signalling a drop when it stops working
    def move_yellow(self):
        super().move_yellow()
        if self.redCounter > 15:
            self.yellowCounter += 1
            if self.yellowCounter <= 15:
                super().move_right(20)
                if self.yellowCounter == 15:
                    self.yellowCounter += 1
                    self.screen.event_generate("<<yellowDrop>>")
        if self.redCounter > 30:
            super().move_right(20)