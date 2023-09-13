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

    @property
    def freq_data(self):
        return self.game.game_mode.freq_data
    
    def start(self, event):

        self.Cursor = self.game.Cursor
        self.freqprof = self.game.freqprof

        self.prob_data = [[self.params.b10], [self.params.b20], [self.params.b30], [self.params.b40]]
        # self.freq_data = self.game.game_mode.freq_data      
        self.acc_data = [[], [], [], [], [], []]
        
        self.x_data = [0]
        self.ep = self.params.ep
        self.alph = self.params.alph
        self.points = self.params.points
        self.beta = self.params.beta
        self.lm = self.params.lm

        self.fig = self.game.game_mode.fig
        self.ax = self.game.game_mode.axs[1]
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid')
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid')
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid')
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid')

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
                self.prob_data[num].append(data[num])

        self.game.game_mode.screen.bind("<<buttonClicked>>", self.animate)


    """ Prediction Generation"""
    def generate_one_cycle(self, frame):

        self.correct()
        
        length = len(self.prob_data[0])
        if length == 1:
            bvals = [[self.prob_data[0][0]], [self.prob_data[1][0]], [self.prob_data[2][0]], [self.prob_data[3][0]]]
        else:
            bvals = [[self.prob_data[0][-2], self.prob_data[0][-1]], [self.prob_data[1][-2], self.prob_data[1][-1]], [self.prob_data[2][-2], self.prob_data[2][-1]], [self.prob_data[3][-2], self.prob_data[3][-1]]]

        # extinction matrix (quantity of decrease by extinction for each behavior)
        em = []

        # reinforcement matrix (quantity of increase by reinforcement for each behavior)
        am = []

        # Dominance matrix (quantity of increase by dominance for each behavior)
        bm = [0, 0, 0, 0]

        # interaction matrix (the interaction effects between each pair of self.behaviors, before summation)
        # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
        im = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        freq_data = self.game.game_mode.freq_data
        if len(freq_data) < 2:
            freq_data = [0, 0]

        Rule_Change = False
        
        # populate matrices with values for this cycle
        for y in range(4):
            em.append(self.calc_ext_change(bvals[y][-1]))
            am.append(self.calc_reinf_change(bvals[y][-1]))
            
            if len(freq_data[0]) >= SLOPERANGE:
                for z in range(4):
                    if (y != z):
                        im[y][z] += (self.calc_resurg_delay(y, z) + self.calc_auto_delay(y, z)
                                     + self.calc_replace_delay(y, z) + self.calc_dissol_delay(y, z))

                        if Rule_Change:
                            im[y][z] += (self.calc_resurg_immed(y, z) + self.calc_auto_immed(y, z)
                                         + self.calc_replace_immed(y, z) + self.calc_dissol_immed(y, z))
                            
                bm[y] = self.calc_domin(y, bvals[y][-1])

        new_predictions = []

        # For each behavior, calculate the probability of this behavior for this cycle and append it to bvals
        # corrections = self.correct()
        for y in range(4):
            epEffect = em[y]
            alphEffect = am[y]
            dominanceEffect = bm[y]
            intEffect = 0
            for z in range(4):
                intEffect += im[y][z]
            cur = bvals[y][-1]

            change = epEffect + alphEffect + dominanceEffect + intEffect
            bNext = cur + change
            if bNext > 1:
                bNext = 1
            if bNext < 0:
                bNext = 0
            new_predictions.append(bNext)
        
        return new_predictions

    def correct(self):
        freq_data = self.game.game_mode.freq_data
        if len(freq_data[0]) >= SLOPERANGE:
            self.change_ext()
            self.change_reinf()

            for y in range(4):
                for z in range(4):
                    self.change_resurg(y, z)
                    self.change_auto(y, z)
                self.change_domin(y)

        if self.ep < 0:
            self.ep = 0
        if self.ep > 1:
            self.ep = 1
        if self.alph < 0:
            self.alph = 0
        if self.alph > 1:
            self.alph = 1
        if self.beta < 0:
            self.beta = 0
        if self.beta > 1:
            self.beta = 1
        
        for y in range(4):
            for z in range(4):
                if self.lm[y][z] < -1:
                    self.lm[y][z] = -1
                if self.lm[y][z] > 1:
                    self.lm[y][z] = 1

   
    """ PARAMETER APPLICATION EQUATIONS"""
    def calc_ext_change(self, cur):
        return -self.ep*cur
        #return -self.ep/HYPER_EP_APP
    
    def calc_reinf_change(self, cur):
        return -self.alph*(1 - cur)
        #return self.alph/HYPER_ALPH_APP
    
    def calc_resurg_delay(self, y, y_prime):
        if self.lm[y][y_prime] < 0 and self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE] < 0:
            return self.lm[y][y_prime] * (self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE])
        return 0
    
    def calc_resurg_immed(self, y, y_prime):
        if self.lm[y][y_prime] < 0 and self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE] < 0:
            return self.lm[y][y_prime] * (self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE])
        return 0
        
    def calc_auto_delay(self, y, y_prime):
        if self.lm[y][y_prime] > 0 and self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE] > 0:
            return (1 - self.prob_data[y][-1]) * self.lm[y][y_prime] * self.prob_data[y_prime][-1]
        return 0
    
    def calc_auto_immed(self, y, y_prime):
        if self.lm[y][y_prime] > 0 and self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE] > 0:
            return (1 - self.prob_data[y][-1]) * self.lm[y][y_prime] * self.prob_data[y_prime][-1]
        
    def calc_replace_delay(self, y, y_prime):
        # TO DO: add phi matrix
        return 0

    def calc_replace_immed(self, y, y_prime):
        # TO DO: add phi matrix
        return 0

    def calc_dissol_delay(self, y, y_prime):
        # TO DO: add phi matrix
        return 0

    def calc_dissol_immed(self, y, y_prime):
        # TO DO: add phi matrix
        return 0

    def calc_domin(self, y, cur):
        dominanceCounter = 0
        dominanceDenominator = self.beta

        if len(self.freq_data[0]) >= SLOPERANGE:
            freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
            
            for z in range(4):
                if y != z:
                    freq_slope_z = self.freq_data[z][-1] - self.freq_data[z][-SLOPERANGE]
                    dominanceDenominator += self.freq_data[z][-1]

                    if self.freq_data[y][-1] > self.freq_data[z][-1] or freq_slope_y > freq_slope_z:
                        dominanceCounter += 1
                    
            if dominanceCounter == 3 and freq_slope_y >= 0 and dominanceDenominator != 0:
                return (1 - cur) * self.beta/(HYPER_BETA_APP*dominanceDenominator)
            return 0
        
        else:
            for z in range(4):
                if y != z:
                    dominanceDenominator += self.prob_data[z][-1]
                    if self.prob_data[y][-1] > self.prob_data[z][-1]:
                        dominanceCounter += 1
            if dominanceCounter == 3 and dominanceDenominator != 0:
                return (1 - cur) * self.beta/(HYPER_BETA_APP*dominanceDenominator)
            return 0

    
    """ PARAMETER UPDATE EQUATIONS """
    def change_ext(self):
        low_freq_val = False
        overshoot_count = 0
        deltas = []
        for n in range(4):
            if self.freq_data[n][-1] < self.prob_data[n][-1]:
                low_freq_val = True

            freq_slope = self.freq_data[n][-1] - self.freq_data[n][-SLOPERANGE]
            prob_slope = self.prob_data[n][-1 - PREDICTION_TIME] - self.prob_data[n][-SLOPERANGE - PREDICTION_TIME]
            if prob_slope >= freq_slope:
                overshoot_count += 1
            deltas.append(freq_slope - prob_slope)

        ep_change = 0
        alph_change = 0
        if low_freq_val == True and overshoot_count == 4:
            for n in range(4):
                ep_change -= deltas[n]
                alph_change += deltas[n]
            ep_change /= HYPER_EP_CHANGE
            alph_change /= HYPER_ALPH_CHANGE

        self.ep += ep_change
        self.alph += alph_change

    def change_reinf(self):
        high_freq_count = 0
        sum_slope_diffs = 0
        deltas = []
        for n in range(4):
            if self.freq_data[n][-1] < self.prob_data[n][-1]:
                high_freq_count += 1

            freq_slope = self.freq_data[n][-1] - self.freq_data[n][-SLOPERANGE]
            prob_slope = self.prob_data[n][-1 - PREDICTION_TIME] - self.prob_data[n][-SLOPERANGE - PREDICTION_TIME]
            sum_slope_diffs += freq_slope - prob_slope
            deltas.append(freq_slope - prob_slope)

        alph_change = 0
        ep_change = 0
        if high_freq_count == 4 and sum_slope_diffs > 0:
            alph_change = sum_slope_diffs/HYPER_ALPH_CHANGE
            ep_change = -sum_slope_diffs/HYPER_EP_CHANGE

        self.ep += ep_change
        self.alph += alph_change
    
    def change_resurg(self, y, y_prime):
        freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        freq_slope_y_prime = self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE]

        prob_slope_y = self.prob_data[y][-1 - PREDICTION_TIME] - self.prob_data[y][-SLOPERANGE - PREDICTION_TIME]

        if freq_slope_y > 0 and freq_slope_y_prime < 0:
            self.lm[y][y_prime] -= (freq_slope_y - prob_slope_y) / HYPER_RESURG_CHANGE

    def change_auto(self, y, y_prime):
        freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        freq_slope_y_prime = self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE]

        prob_slope_y = self.prob_data[y][-1 - PREDICTION_TIME] - self.prob_data[y][-SLOPERANGE - PREDICTION_TIME]
        prob_slope_y_prime = self.prob_data[y_prime][-1 - PREDICTION_TIME] - self.prob_data[y_prime][-SLOPERANGE - PREDICTION_TIME]

        if freq_slope_y > 0 and freq_slope_y_prime > 0:
            self.lm[y][y_prime] += (freq_slope_y - prob_slope_y) / HYPER_AUTO_CHANGE
            self.lm[y_prime][y] += (freq_slope_y_prime - prob_slope_y_prime) / HYPER_AUTO_CHANGE

    def change_domin(self, y):
        freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        prob_slope_y = self.prob_data[y][-1 - PREDICTION_TIME] - self.prob_data[y][-SLOPERANGE - PREDICTION_TIME]
        
        dominanceCounter = 0
        
        for z in range(4):
            if y != z:

                if self.freq_data[y][-1] > self.freq_data[z][-1]:
                    dominanceCounter += 1
                
        if dominanceCounter == 3 and freq_slope_y >= 0:
            # self.beta += (freq_slope_y - prob_slope_y) / HYPER_BETA_CHANGE
            self.beta += 0

    
    """ Graph Generation """
    def accuracy_graph(self, frame):
        freq_data = self.freq_data
        if len(freq_data[0]) >= 1:
            if len(freq_data[0]) >= 1 + PREDICTION_TIME * 10:
                mean = 0
                for n in range(4):
                    null_hyp = freq_data[n][-(1 + PREDICTION_TIME * 10)]
                    null_error = abs(null_hyp - freq_data[n][-1])
                    prob_error = abs(self.prob_data[n][-(1 + PREDICTION_TIME * 10)] - freq_data[n][-1])
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
                    prob_error = abs(self.prob_data[n][-(1 + PREDICTION_TIME * 10)] - freq_data[n][-1])
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
    
    def genGraph(self, frame):

        # Generate a list of behavioral probabilities over time
        b_values = self.generate_one_cycle(frame)


        self.x_data.append((frame * .1) + PREDICTION_TIME)
        for num in range(4):
            # bval_smooth = b_values[num]
            # if len(self.prob_data[num]) >= 40:
            #     for m in range(1, 40):
            #         bval_smooth += self.prob_data[num][-m]
            #     bval_smooth /= 40
            self.prob_data[num].append(b_values[num])

        window_start = 0
        if frame <= 100:
            self.line1.set_data(self.x_data, self.prob_data[0])
            self.line2.set_data(self.x_data, self.prob_data[1])
            self.line3.set_data(self.x_data, self.prob_data[2])
            self.line4.set_data(self.x_data, self.prob_data[3])

        if frame > 100:
            window_start = frame/10 - 10

            self.line1.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[0][-100 - 10 * PREDICTION_TIME:])
            self.line2.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[1][-100 - 10 * PREDICTION_TIME:])
            self.line3.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[2][-100 - 10 * PREDICTION_TIME:])
            self.line4.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[3][-100 - 10 * PREDICTION_TIME:])

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

    
    """ Other Functions """
    def record(self):
        freq = self.game.game_mode.freq_data
        mode = self.game.game_mode.mode_char
        name = self.game.game_mode.player_name
        time = self.game.game_mode.timer.time_elapsed()
        trial = self.game.game_mode.trial_number

        self.Cursor.execute('INSERT INTO Frequencies(B1, B2, B3, B4, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (freq[0][-1], freq[1][-1], freq[2][-1], freq[3][-1], mode, name, time, trial))
        self.Cursor.execute('INSERT INTO Probabilities(B1, B2, B3, B4, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (self.prob_data[0][-(1 + PREDICTION_TIME * 10)], self.prob_data[1][-(1 + PREDICTION_TIME * 10)], self.prob_data[2][-(1 + PREDICTION_TIME * 10)], self.prob_data[3][-(1 + PREDICTION_TIME * 10)], 
                             mode, name, time, trial))
        self.Cursor.execute('INSERT INTO Accuracies(B1, B2, B3, B4, mean, cumulative, mode, name, time, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (self.acc_data[0][-1], self.acc_data[1][-1], self.acc_data[2][-1], self.acc_data[3][-1], self.acc_data[4][-1], self.acc_data[5][-1], 
                            mode, name, time, trial))
        self.Cursor.execute('INSERT INTO upParameters(alpha, beta, l12, l13, l14, l21, l23, l24, l31, l32, l34, l41, l42, l43, time, mode, name, trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                            (self.alph, self.beta, self.lm[0][1], self.lm[0][2], self.lm[0][3], self.lm[1][0], self.lm[1][2], self.lm[1][3],
                            self.lm[2][0], self.lm[2][1], self.lm[2][3], self.lm[3][0], self.lm[3][1], self.lm[3][2], 
                            time, mode, name, trial))
        self.Cursor.execute('INSERT INTO downParameters(epsilon, time, mode, name, trial) VALUES (?, ?, ?, ?, ?)',
                            (self.ep, time, mode, name, trial))

    def stop(self, event):
        self.ani.event_source.stop()