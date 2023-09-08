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

        self.Cursor = self.game.Cursor
        self.freqprof = self.game.freqprof
        
        self.x_data = [0]
        self.y_data = [[self.params.b10], [self.params.b20], [self.params.b30], [self.params.b40]]
        self.ep = self.params.ep
        self.alph = self.params.alph
        self.points = self.params.points
        self.lm = self.params.lm

        # self.real_time_ep = [self.ep]
        # self.real_time_alph = [self.alph]
        # self.real_time_lm = [self.lm]

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
        self.ax.set_xlim(0, 10 + PREDICTION_TIME)
        self.ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["-10", "-8", "-6", "-4", "-2", "0", "+2", "+4", "+6"])

        self.acc_ax.set_ylim(-1, 1)

        self.game.game_mode.screen.bind("<<stopGraph>>", self.stop)

        for num in range(1, 1 + PREDICTION_TIME * 10):
            data = self.generate_one_cycle(-1)
            self.x_data.append(num * .1)
            for num in range(4):
                self.y_data[num].append(data[num])

        self.game.game_mode.screen.bind("<<buttonClicked>>", self.animate)

    def generate_one_cycle(self, frame):

        length = len(self.y_data[0])
        if length == 1:
            bvals = [[self.y_data[0][0]], [self.y_data[1][0]], [self.y_data[2][0]], [self.y_data[3][0]]]
        else:
            bvals = [[self.y_data[0][-2], self.y_data[0][-1]], [self.y_data[1][-2], self.y_data[1][-1]], [self.y_data[2][-2], self.y_data[2][-1]], [self.y_data[3][-2], self.y_data[3][-1]]]

        # extinction matrix (quantity of decrease by extinction for each behavior)
        em = []

        # reinforcement matrix (quantity of increase by reinforcement for each behavior)
        am = []

        # interaction matrix (the interaction effects between each pair of self.behaviors, before summation)
        # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
        im = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # self.correct()

        freq_data = self.game.game_mode.freq_data
        if len(freq_data) < 2:
            freq_data = [0, 0]
        
        # populate matrices with values for this cycle
        for y in range(4):
            em.append(-bvals[y][-1] * self.ep)
            am.append((1 - bvals[y][-1]) * self.alph)
            for z in range(4):
                if (y != z and len(bvals[z]) >= 2 and self.lm[y][z] >= -1 and self.lm[y][z] <= 1):
                    if (self.lm[y][z] < 0 and bvals[z][-1] - bvals[z][-2] < 0):
                        im[y][z] = (1 - bvals[y][-1]) * -self.lm[y][z] * bvals[z][-1]
                    if (self.lm[y][z] > 0 and bvals[z][-1] - bvals[z][-2] > 0):
                        im[y][z] = (1 - bvals[y][-1]) * self.lm[y][z] * bvals[z][-1]
                    # if (self.lm[y][z] < 0 and freq_data[z][-1] - freq_data[z][-2] < 0):
                    #     im[y][z] = (1 - bvals[y][-1]) * -self.lm[y][z] * bvals[z][-1]
                    # if (self.lm[y][z] > 0 and freq_data[z][-1] - freq_data[z][-2] > 0):
                    #     im[y][z] = (1 - bvals[y][-1]) * self.lm[y][z] * bvals[z][-1]
        
        # print("blue -- ep effect: " + str(em[0]) + "  alph effect: " + str(am[0]))
        # print("red -- ep effect: " + str(em[1]) + "  alph effect: " + str(am[1]))
        # print("green -- ep effect: " + str(em[2]) + "  alph effect: " + str(am[2]))
        # print("yellow -- ep effect: " + str(em[3]) + "  alph effect: " + str(am[3]))
        # print()

        new_bvals = []

        # For each behavior, calculate the probability of this behavior for this cycle and append it to bvals
        # corrections = self.correct()
        for y in range(4):
            epEffect = em[y]
            alphEffect = am[y]
            intEffect = 0
            for z in range(4):
                intEffect += im[y][z]
            cur = bvals[y][-1]

            change = epEffect + alphEffect + intEffect
            bNext = cur + change
            if bNext > 1:
                bNext = 1
            if bNext < 0:
                bNext = 0
            new_bvals.append(bNext)
        
        return new_bvals

    """ Functionality and mechanics of the correct function:
            1. Changes the alpha, epsilon, and lambdas
            2. Over the course of the trial, perhaps we would hope to see fewer changes as its previously-generated values are more honed for accurate predictions. Maybe we can measure the amount of change in parameters over time
            3. CHECK: Increases a given lambda when it sees two behaviors rising together
            4. CHECK: Decreases a given lambda when it sees a rise in one behavior causing a fall in another
            5. CHECK: Increases alpha when the frequency profile is rising faster than the probability profile overall
            6. CHECK: Decreases alpha when the frequency profile is rising slower than the probability profile overall
            7. CHECK: Increases epsilon when the frequency profile is falling faster than the probability profile overall
            8. CHECK: Decreases epsilon when the frequency profile is falling slower than the probability profile overall"""
    def correct(self):
        freq_data = self.game.game_mode.freq_data
        prob_data = self.y_data
        if len(freq_data[0]) >= 1 + PREDICTION_TIME * 10:
            prob_values = []
            freq_values = []
            diffs = []

            for n in range(4):
                prob_values.append(prob_data[n][-(1 + PREDICTION_TIME * 10)])
                freq_values.append(freq_data[n][-1])
                diffs.append(freq_values[n] - prob_values[n])

            mean_error = 0
            # If undershooting on average, increase alpha and decrease epsilon. If overshooting on average, increase epsilon and decrease alpha
            for i in range(4):
                mean_error += diffs[i]
            mean_error /= 4
            self.alph += mean_error / 50
            self.ep -= mean_error / 50
            if self.alph < 0:
                self.alph = 0
            if self.ep < 0:
                self.ep = 0
            if self.alph > 1:
                self.alph = 1
            if self.ep > 1:
                self.ep = 1
            
            prob_slopes = []
            freq_slopes = []
            slope_diffs = []

            for n in range(4):
                prob_slopes.append((prob_data[n][-(1 + PREDICTION_TIME * 10)] - prob_data[n][-(6 + PREDICTION_TIME * 10)]) / 5)
                freq_slopes.append((freq_data[n][-1] - freq_data[n][-6]) / 5)
                slope_diffs.append(freq_slopes[n] - prob_slopes[n])

            # mean_slope_error = 0
            # # If undershooting on average, increase alpha and decrease epsilon. If overshooting on average, increase epsilon and decrease alpha
            # for i in range(4):
            #     mean_slope_error += slope_diffs[i]
            # mean_slope_error /= 4
            # self.alph += mean_slope_error / 10
            # self.ep -= mean_slope_error / 10
            # if self.alph < 0:
            #     self.alph = 0
            # if self.ep < 0:
            #     self.ep = 0

            for i in range(4):
                for j in range(4):
                    # Behaviors i and j are rising together; if undershooting, increase lambda. If overshooting, decrease lambda but not below 0
                    if i != j and freq_slopes[i] > 0 and freq_slopes[j] > 0:
                        neg = False
                        if self.lm[i][j] < 0 or self.lm[j][i] < 0:
                            neg = True

                        self.lm[i][j] += slope_diffs[i]
                        self.lm[j][i] += slope_diffs[j]

                        if neg == False:
                            if self.lm[i][j] < 0:
                                self.lm[i][j] = 0
                            if self.lm[j][i] < 0:
                                self.lm[j][i] = 0

                    # Behavior i is falling and behavior j is rising, indicating resurgence. If undershooting j, decrease lambda; if overshooting j, increase lambda but not above 0
                    if i != j and freq_slopes[i] < 0 and freq_slopes [j] > 0:
                        pos = False
                        if self.lm[j][i] > 0:
                            pos = True

                        self.lm[j][i] -= slope_diffs[j]

                        if pos == False:
                            if self.lm[j][i] > 0:
                                self.lm[j][i] = 0
                    
                    if self.lm[i][j] > 1:
                        self.lm[i][j] = 1
                    if self.lm[j][i] > 1:
                        self.lm[j][i] = 1
            # print("yellow lambdas: " + str(self.lm[0][3]) + " " + str(self.lm[1][3]) + " " + str(self.lm[2][3]))

    def accuracy_graph(self, frame):
        freq_data = self.game.game_mode.freq_data
        if len(freq_data[0]) >= 1:
            if len(freq_data[0]) >= 1 + PREDICTION_TIME * 10:
                mean = 0
                for n in range(4):
                    null_hyp = freq_data[n][-(1 + PREDICTION_TIME * 10)]
                    null_error = abs(null_hyp - freq_data[n][-1])
                    prob_error = abs(self.y_data[n][-(1 + PREDICTION_TIME * 10)] - freq_data[n][-1])
                    acc = null_error - prob_error
                    self.acc_data[n].append(acc)
                    mean += acc
                mean /= 4
                self.acc_data[4].append(mean)
            else:
                mean = 0
                for n in range(4):
                    null_hyp = freq_data[n][0]
                    null_error = abs(null_hyp - freq_data[n][-1])
                    prob_error = abs(self.y_data[n][-(1 + PREDICTION_TIME * 10)] - freq_data[n][-1])
                    acc = null_error - prob_error
                    self.acc_data[n].append(acc)
                    mean += acc
                mean /= 4
                self.acc_data[4].append(mean)
        
            x_data = self.game.game_mode.x_data

            avg_mean_acc = 0
            length = len(self.acc_data[0])
            if length >= 1:
                for i in range(length):
                    avg_mean_acc += self.acc_data[4][i]
                avg_mean_acc /= length
                self.acc_data[5].append(avg_mean_acc)

            
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
    
    def record(self):
        freq = self.game.game_mode.freq_data
        mode = self.game.game_mode.mode_char
        name = self.game.game_mode.player_name
        time = self.game.game_mode.timer.time_elapsed()
        trial = self.game.game_mode.trial_number

        self.Cursor.execute('INSERT INTO Frequencies(B1, B2, B3, B4, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (freq[0][-1], freq[1][-1], freq[2][-1], freq[3][-1], mode, name, time, trial))
        self.Cursor.execute('INSERT INTO Probabilities(B1, B2, B3, B4, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (self.y_data[0][-(1 + PREDICTION_TIME * 10)], self.y_data[1][-(1 + PREDICTION_TIME * 10)], self.y_data[2][-(1 + PREDICTION_TIME * 10)], self.y_data[3][-(1 + PREDICTION_TIME * 10)], 
                             mode, name, time, trial))
        self.Cursor.execute('INSERT INTO Accuracies(B1, B2, B3, B4, mean, cumulative, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (self.acc_data[0][-1], self.acc_data[1][-1], self.acc_data[2][-1], self.acc_data[3][-1], self.acc_data[4][-1], self.acc_data[5][-1], 
                            mode, name, time, trial))
        self.Cursor.execute('INSERT INTO Parameters(epsilon, alpha, l12, l13, l14, l21, l23, l24, l31, l32, l34, l41, l42, l43, time, mode, name, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                            (self.ep, self.alph, self.lm[0][1], self.lm[0][2], self.lm[0][3], self.lm[1][0], self.lm[1][2], self.lm[1][3],
                            self.lm[2][0], self.lm[2][1], self.lm[2][3], self.lm[3][0], self.lm[3][1], self.lm[3][2], 
                            time, mode, name, trial))
    
    def genGraph(self, frame):

        # Generate a list of behavioral probabilities over time
        b_values = self.generate_one_cycle(frame)


        self.x_data.append((frame * .1) + PREDICTION_TIME)
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

            self.line1.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.y_data[0][-100 - 10 * PREDICTION_TIME:])
            self.line2.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.y_data[1][-100 - 10 * PREDICTION_TIME:])
            self.line3.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.y_data[2][-100 - 10 * PREDICTION_TIME:])
            self.line4.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.y_data[3][-100 - 10 * PREDICTION_TIME:])

        self.ax.set_xlim(window_start, window_start + 10 + PREDICTION_TIME)

        self.game.game_mode.record_data(frame)

        self.accuracy_graph(frame)

        self.record()

        return (self.game.game_mode.line1, self.game.game_mode.line2, self.game.game_mode.line3, self.game.game_mode.line4, 
                self.line1, self.line2, self.line3, self.line4,
                self.acc1, self.acc2, self.acc3, self.acc4, self.acc_mean, self.acc_cumul)
    
    def animate(self, event):
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