# function to generate and display graph when submit is clicked

from math import *

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

        self.real_time_ep = [self.ep]
        self.real_time_alph = [self.alph]
        self.real_time_lm = [self.lm]

        self.fig = self.game.game_mode.fig
        self.ax = self.game.game_mode.axs[1]
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid')
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid')
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid')
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid')

        self.acc_data = [[], [], [], [], [], []]

        self.acc_ax = self.game.game_mode.axs[0]
        self.acc1, = self.acc_ax.plot([], [], 'b', linestyle='dashed')
        self.acc2, = self.acc_ax.plot([], [], 'r', linestyle='dashed')
        self.acc3, = self.acc_ax.plot([], [], 'g', linestyle='dashed')
        self.acc4, = self.acc_ax.plot([], [], 'y', linestyle='dashed')
        self.acc_mean, = self.acc_ax.plot([], [], 'k', linestyle='solid', label='Mean Accuracy')
        self.acc_cumul, = self.acc_ax.plot([], [], 'm', linestyle='solid', label='Cumulative Accuracy')

        self.ax.set_ylim(0, 1)
        self.ax.set_xlim(0, 11)
        self.ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14], labels=["-10", "-8", "-6", "-4", "-2", "0", "+2", "+4"])

        self.acc_ax.set_ylim(-1, 1)

        self.game.game_mode.screen.bind("<<stopGraph>>", self.stop)

        for num in range(1, 11):
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
        corrections = self.correct()
        for y in range(1, 5):
            epEffect = em[y]
            alphEffect = am[y]
            intEffect = 0
            for z in range(1, 5):
                intEffect += im[y][z]
            cur = bvals[y][-1]

            # correction = 0
            # if frame > 0:
            #     correction = self.correct(cur, y - 1)

            change = epEffect + alphEffect + intEffect + corrections[y - 1]
            bNext = cur + change
            new_bvals.append(bNext)
        
        return new_bvals

    """ Functionality and mechanics of the correct function:
            1. Changes the alpha, epsilon, and lambdas
            2. Over the course of the trial, perhaps we would hope to see fewer changes as its previously-generated values are more honed for accurate predictions. Maybe we can measure the amount of change in parameters over time
            3. Increases a given lambda when it sees two behaviors rising together
            4. Decreases a given lambda when it sees a rise in one behavior causing a fall in another
            5. Increases alpha when the frequency profile is rising faster than the probability profile overall
            6. Decreases alpha when the frequency profile is rising slower than the probability profile overall
            7. Increases epsilon when the frequency profile is falling faster than the probability profile overall
            8. Decreases epsilon when the frequency profile is falling slower than the probability profile overall"""
    def correct(self):
        freq_data = self.game.game_mode.freq_data
        prob_data = self.y_data
        if len(freq_data[0]) >= 2:
            prob_slopes = [[], [], [], []]
            freq_slopes = [[], [], [], []]
            slope_diffs = [[], [], [], []]

            for n in range(4):
                prob_slopes[n] = prob_data[n][-11] - prob_data[n][-12]
                freq_slopes[n] = freq_data[n][-1] - freq_data[n][-2]
                slope_diffs[n] = freq_slopes[n] - prob_slopes[n]

            return slope_diffs

        # if len(freq_data[behavior]) >= 1:
        #     correction = freq_data[behavior][-1] - cur
        #     return correction
        
        return [0, 0, 0, 0]
        
    def accuracy_graph(self, frame):
        freq_data = self.game.game_mode.freq_data
        if len(freq_data[0]) >= 1:
            if len(freq_data[0]) >= 11:
                mean = 0
                for n in range(4):
                    null_hyp = freq_data[n][-11]
                    null_error = abs(null_hyp - freq_data[n][-1])
                    prob_error = abs(self.y_data[n][-11] - freq_data[n][-1])
                    acc = null_error - prob_error
                    # acc_smooth = acc
                    # for m in range(1, 5):
                    #     acc_smooth += self.acc_data[n][-m]
                    # acc_smooth /= 5
                    self.acc_data[n].append(acc)
                    mean += acc
                mean /= 4
                # mean_smooth = mean
                # for m in range(1, 5):
                #     mean_smooth += self.acc_data[4][-m]
                # mean_smooth /= 5
                self.acc_data[4].append(mean)
            else:
                mean = 0
                for n in range(4):
                    null_hyp = freq_data[n][0]
                    null_error = abs(null_hyp - freq_data[n][-1])
                    prob_error = abs(self.y_data[n][-11] - freq_data[n][-1])
                    acc = null_error - prob_error
                    self.acc_data[n].append(acc)
                    mean += acc
                mean /= 4
                self.acc_data[4].append(mean)
        
            x_data = self.game.game_mode.x_data

            blue_mean_across_time = 0
            length = len(self.acc_data[0])
            if length >= 1:
                for n in range(length):
                    blue_mean_across_time += self.acc_data[0][n]
                blue_mean_across_time /= length
                self.acc_data[5].append(blue_mean_across_time)

            
            if frame <= 100:
                self.acc1.set_data(x_data, self.acc_data[0])
                self.acc2.set_data(x_data, self.acc_data[1])
                self.acc3.set_data(x_data, self.acc_data[2])
                self.acc4.set_data(x_data, self.acc_data[3])
                self.acc_mean.set_data(x_data, self.acc_data[4])
                self.acc_cumul.set_data(x_data, self.acc_data[5])

            if frame > 100:
                self.acc1.set_data(x_data[-100:], self.acc_data[0][-100:])
                self.acc2.set_data(x_data[-100:], self.acc_data[1][-100:])
                self.acc3.set_data(x_data[-100:], self.acc_data[2][-100:])
                self.acc4.set_data(x_data[-100:], self.acc_data[3][-100:])
                self.acc_mean.set_data(x_data[-100:], self.acc_data[4][-100:])
                self.acc_cumul.set_data(x_data[-100:], self.acc_data[5][-100:])
    
    def genGraph(self, frame):

        # Generate a list of behavioral probabilities over time
        b_values = self.generate_one_cycle(frame)


        self.x_data.append((frame * .1) + 1)
        for num in range(4):
            # bval_smooth = b_values[num]
            # if len(self.y_data[num]) >= 40:
            #     for m in range(1, 40):
            #         bval_smooth += self.y_data[num][-m]
            #     bval_smooth /= 40
            self.y_data[num].append(b_values[num])

        window_start = 0
        if frame <= 100:
            self.line1.set_data(self.x_data, self.y_data[0])
            self.line2.set_data(self.x_data, self.y_data[1])
            self.line3.set_data(self.x_data, self.y_data[2])
            self.line4.set_data(self.x_data, self.y_data[3])

        if frame > 100:
            window_start = frame/10 - 10

            self.line1.set_data(self.x_data[-110:], self.y_data[0][-110:])
            self.line2.set_data(self.x_data[-110:], self.y_data[1][-110:])
            self.line3.set_data(self.x_data[-110:], self.y_data[2][-110:])
            self.line4.set_data(self.x_data[-110:], self.y_data[3][-110:])

        self.ax.set_xlim(window_start, window_start + 11)

        self.game.game_mode.record_data(frame)

        self.accuracy_graph(frame)

        return (self.game.game_mode.line1, self.game.game_mode.line2, self.game.game_mode.line3, self.game.game_mode.line4, 
                self.line1, self.line2, self.line3, self.line4,
                self.acc1, self.acc2, self.acc3, self.acc4, self.acc_mean, self.acc_cumul)
    
    def animate(self):
        self.ani = FuncAnimation(self.fig, self.genGraph, frames=itertools.count(), interval=100, blit=True, save_count=MAX_FRAMES)

        self.fig.set_figheight(7)
        
        self.ax.set_ylabel('Behavioral Probabilities')
        self.fig.legend()

        self.game.game_mode.ax.set_xlabel('Time to present (seconds)')
        self.game.game_mode.ax.set_ylabel('Behavioral Frequencies')
        self.game.game_mode.fig.legend()

        self.acc_ax.set_ylabel('Accuracy')

        plt.show()

    def stop(self, event):
        self.ani.event_source.stop()