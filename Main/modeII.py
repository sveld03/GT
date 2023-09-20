from modeTemplate import *

# Blue works, then green works
class ModeII(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        self.blueCounter = 1

    # If blue has been clicked <= 15 times, move the dot right
    def move_blue(self):
        super().move_blue()
        self.blueCounter += 1
        if self.blueCounter <= 15:
            super().move_right()

            # On the 15th click, trigger an event that causes the blue probability line to start falling
            if self.blueCounter == 15:
                self.blueCounter += 1
                self.screen.event_generate("<<blueDrop>>")

    # Move dot right, then record green button click
    def move_green(self):
        super().move_green()

        # So long as blue has been clicked 15 times, move the dot right
        if self.blueCounter > 15:
            super().move_right()