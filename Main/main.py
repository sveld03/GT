# Runs both the grapher and the game

from game import *
from params import *
from realTimeGrapher import *

class Main:
    def __init__(self):
        self.params = Params() # initializes the parameter input screen

        self.screen = Screen() # initializes the game screen
        self.game = Game(self.screen, self.params) # initializes the game

        self.real_time_grapher = realTimeGrapher(self.params, self.game) # initializes the grapher

    # Displays the parameter input screen
    def run_grapher(self):
        self.params.mainloop()

    # Displays the game screen
    def run_game(self):
        self.game.screen.mainloop()

# Run the application
if __name__ == "__main__":

    main = Main()

    main.run_grapher()
    main.run_game()