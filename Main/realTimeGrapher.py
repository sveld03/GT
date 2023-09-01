# function to generate and display graph when submit is clicked

from params import *
from game import *

class realTimeGrapher:

    def __init__(self, params, game):

        self.params = params
        # self.params.bind("<<startGraph>>", self.start)

        self.game = game
        self.game.screen.bind("<<startPrediction>>", self.start)

    def start(self, event):

        self.x_data = [0]
        self.y_data = [[self.params.b10], [self.params.b20], [self.params.b30], [self.params.b40]]
        self.ep = self.params.ep
        self.alph = self.params.alph
        self.points = self.params.points
        self.lm = self.params.lm

        self.fig = self.game.game_mode.fig
        self.ax = self.game.game_mode.axs[1]
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid')
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid')
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid')
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid')

        self.ax.set_ylim(0, 1)
        self.ax.set_xlim(0, 13)
        self.ax.set_xticks([0, 2, 4, 6, 8, 10, 12], labels=["-10", "-8", "-6", "-4", "-2", "0", "+2"])

        self.game.game_mode.screen.bind("<<stopGraph>>", self.stop)

        for num in range(1, 31):
            data = self.generate_one_cycle(-1)
            self.x_data.append(num * .1)
            for num in range(4):
                self.y_data[num].append(data[num])

        self.animate()

    def generate_one_cycle(self, frame):

        length = len(self.y_data[0])
        if length == 1:
            bvals = [[-2], [self.y_data[0][0]], [self.y_data[1][0]], [self.y_data[2][0]], [self.y_data[3][0]]]
        else:
            bvals = [[-2, -2], [self.y_data[0][-2], self.y_data[0][-1]], [self.y_data[1][-2], self.y_data[1][-1]], [self.y_data[2][-2], self.y_data[2][-1]], [self.y_data[3][-2], self.y_data[3][-1]]]

        # extinction matrix (quantity of decrease by extinction for each behavior)
        em = [0]

        # reinforcement matrix (quantity of increase by reinforcement for each behavior)
        am = [0]

        # interaction matrix (the interaction effects between each pair of self.behaviors, before summation)
        # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
        im = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        # populate matrices with values for this cycle
        for y in range(1, 5):
            em.append(-bvals[y][-1] * self.ep)
            am.append((1 - bvals[y][-1]) * self.alph)
            for z in range(1, 5):
                if (y != z and len(bvals[z]) >= 2 and self.lm[y][z] >= -1 and self.lm[y][z] <= 1):
                    if (self.lm[y][z] < 0 and bvals[z][-1] - bvals[z][-2] < 0):
                        im[y][z] = (1 - bvals[y][-1]) * -self.lm[y][z] * bvals[z][-1]
                    if (self.lm[y][z] > 0 and bvals[z][-1] - bvals[z][-2] > 0):
                        im[y][z] = (1 - bvals[y][-1]) * self.lm[y][z] * bvals[z][-1]
        
        new_bvals = []

        # For each behavior, calculate the probability of this behavior for this cycle and append it to bvals
        for y in range(1, 5):
            epEffect = em[y]
            alphEffect = am[y]
            intEffect = 0
            for z in range(1, 5):
                intEffect += im[y][z]
            cur = bvals[y][-1]

            correction = 0
            if frame > 0:
                correction = self.correct(cur, y - 1)

            change = epEffect + alphEffect + intEffect + correction
            bNext = cur + change
            new_bvals.append(bNext)
        
        return new_bvals

    def correct(self, prediction, behavior):
        if len(self.game.game_mode.y_data[behavior]) >= 1:
            actual = self.game.game_mode.y_data[behavior][-1]
            difference = actual - prediction
            return .1 * difference
        return 0
        
    
    def genGraph(self, frame):

        # Generate a list of behavioral probabilities over time
        b_values = self.generate_one_cycle(frame)


        self.x_data.append((frame * .1) + 3)
        for num in range(4):
            self.y_data[num].append(b_values[num])

        window_start = 0
        if frame <= 100:
            self.line1.set_data(self.x_data, self.y_data[0])
            self.line2.set_data(self.x_data, self.y_data[1])
            self.line3.set_data(self.x_data, self.y_data[2])
            self.line4.set_data(self.x_data, self.y_data[3])

        if frame > 100:
            window_start = frame/10 - 10

            self.line1.set_data(self.x_data[-130 : -1], self.y_data[0][-130 : -1])
            self.line2.set_data(self.x_data[-130 : -1], self.y_data[1][-130 : -1])
            self.line3.set_data(self.x_data[-130 : -1], self.y_data[2][-130 : -1])
            self.line4.set_data(self.x_data[-130 : -1], self.y_data[3][-130 : -1])

        self.ax.set_xlim(window_start, window_start + 13)

        self.game.game_mode.record_data(frame)

        return self.game.game_mode.line1, self.game.game_mode.line2, self.game.game_mode.line3, self.game.game_mode.line4, self.line1, self.line2, self.line3, self.line4

    def animate(self):
        self.ani = FuncAnimation(self.fig, self.genGraph, frames=itertools.count(), interval=100, blit=True, save_count=MAX_FRAMES)

        # self.fig.set_figwidth(9.75)
        # self.game.game_mode.fig.set_figwidth(7.5)
        
        self.ax.set_xlabel('Time to present (seconds)')
        self.ax.set_ylabel('Behavioral Probabilities')
        self.fig.legend()

        self.game.game_mode.ax.set_xlabel('Time to present (seconds)')
        self.game.game_mode.ax.set_ylabel('Behavioral Frequencies')
        self.game.game_mode.fig.legend()

        plt.show()

    def stop(self, event):
        self.ani.event_source.stop()