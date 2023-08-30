# Runs both the grapher and the game

from game import *
from grapher import *

def run_game():
    screen = Screen()
    game = Game(screen)
    game.screen.mainloop()

def run_grapher():
    grapher = Grapher()
    grapher.mainloop()

if __name__ == "__main__":
    grapher_thread = threading.Thread(target=run_grapher)
    game_thread = threading.Thread(target=run_game)

    grapher_thread.start()
    game_thread.start()

    grapher_thread.join()
    game_thread.join()