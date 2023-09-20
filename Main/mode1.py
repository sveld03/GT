from modeTemplate import *

# To make success a matter of probability
import random

# simplest probabilistic game -- green has high probability, the others have decreasing probability
class Mode1(ModeTemplate):
    def __init__(self, freqprof, cursor, screen, timer, window):
        super().__init__(freqprof, cursor, screen, timer, window)

        # The first counter for each button is the initial denominator of the probability of success.
        # The second counter increases when the button is clicked, and when it hits a multiple of 4 it increases the value of the first counter, reducing probability of success

        self.blueCounter1 = 4
        self.blueDecrease1 = 1
        
        self.redCounter1 = 4
        self.redDecrease1 = 1
        
        self.yellowCounter1 = 4
        self.yellowDecrease1 = 1

    def move_blue(self):
        super().move_blue() # all super() functions can be found in modeTemplate.py

        # Depending on how many times the blue button has been clicked, there is between a 1/4 and 1/10 chance of moving the dot. When it gets lower then it stops working
        randVal = random.randrange(1, self.blueCounter1)
        if randVal == 1 and self.blueCounter1 < 10:
            super().move_right()

        # Increment the counters to reduce probability of success
        self.blueDecrease1 += 1
        if self.blueDecrease1 % 4 == 0:
            self.blueCounter1 += 1

    def move_red(self):
        super().move_red()
        randVal = random.randrange(1, self.redCounter1)
        if randVal == 1 and self.redCounter1 < 10:
            super().move_right()
        self.redDecrease1 += 1
        if self.redDecrease1 % 4 == 0:
            self.redCounter1 += 1
    
    def move_green(self):
        super().move_green()

        # The green button has a constant probability of success of 1/3
        randVal = random.randrange(1, 3)
        if randVal == 1:
            super().move_right()

    def move_yellow(self):
        super().move_yellow()
        randVal = random.randrange(1, self.yellowCounter1)
        if randVal == 1 and self.yellowCounter1 < 10:
            super().move_right()
        self.yellowDecrease1 += 1
        if self.yellowDecrease1 % 4 == 0:
            self.yellowCounter1 += 1