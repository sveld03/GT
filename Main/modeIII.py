from modeTemplate import *

# Yellow works, then red, then green
class ModeIII(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.yellowCounter = 1
        self.redCounter = 1

    # If yellow has been clicked <= 10 times, move the dot right
    def move_yellow(self):
        super().move_yellow()
        self.yellowCounter += 1
        if self.yellowCounter <= 10:
            super().move_right()

            # on the 10th click, signal for the yellow prediction to start dropping
            if self.yellowCounter == 10:
                self.yellowCounter += 1
                self.screen.event_generate("<<yellowDrop>>")

    # If yellow has been clicked > 10 times and red <= 10 times, move the dot right
    def move_red(self):
        super().move_red()
        if self.yellowCounter > 10:
            self.redCounter += 1
            if self.redCounter <= 10:
                super().move_right()

                # on the 10th click, signal for the red prediction to start dropping
                if self.redCounter == 10:
                    self.redCounter += 1
                    self.screen.event_generate("<<redDrop>>")

    # If red has been clicked > 10 times, move the dot right
    def move_green(self):
        super().move_green()
        if self.redCounter > 10:
            super().move_right()