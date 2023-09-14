from modeTemplate import *

class ModeIII(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.yellowCounter = 1
        self.redCounter = 1

    # Move dot right, then record blue button click
    def move_yellow(self):
        super().move_yellow()
        self.yellowCounter += 1
        if self.yellowCounter <= 10:
            super().move_right()
            if self.yellowCounter == 10:
                self.yellowCounter += 1
                self.screen.event_generate("<<yellowDrop>>")

    # Move dot left, then record red button click
    def move_red(self):
        super().move_red()
        if self.yellowCounter > 10:
            self.redCounter += 1
            if self.redCounter <= 10:
                super().move_right()
                if self.redCounter == 10:
                    self.redCounter += 1
                    self.screen.event_generate("<<redDrop>>")


    def move_green(self):
        super().move_green()
        if self.redCounter > 10:
            super().move_right()