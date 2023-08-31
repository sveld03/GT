# Runs both the grapher and the game

from game import *
from params import *
from realTimeGrapher import *

class Main:
    def __init__(self):
        self.params = Params()

        self.screen = Screen()
        self.game = Game(self.screen, self.params)

        self.real_time_grapher = realTimeGrapher(self.params, self.game)

    def run_grapher(self):
        self.params.mainloop()

    def run_game(self):
        self.game.screen.mainloop()

if __name__ == "__main__":

    main = Main()

    main.run_grapher()
    main.run_game()

    # grapher_thread = threading.Thread(target=main.run_grapher)
    # game_thread = threading.Thread(target=main.run_game)

    # grapher_thread.start()
    # game_thread.start()

    # grapher_thread.join()
    # game_thread.join()