from modeTemplate import *

class ModeIV(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.yellowCounter = 0
        self.redCounter = 0

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