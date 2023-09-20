# realTimeGrapher -- class to generate and display graph when submit is clicked

from math import *

from params import *
from game import *

class realTimeGrapher:

    def __init__(self, params, game):

        # Store parameter info
        self.params = params

        # Store game info, and bind the startPrediction event to the start function
        self.game = game
        self.game.screen.bind("<<startPrediction>>", self.start)

    # For ease and readability; just use self.freq_data to access the frequency data
    @property
    def freq_data(self):
        return self.game.game_mode.freq_data
    
    # Starts the graph
    def start(self, event):

        # database connection
        self.Cursor = self.game.Cursor
        self.freqprof = self.game.freqprof

        # Probability data and accuracy data (frequency data is generated in modeTemplate.py)
        self.prob_data = [[self.params.b10], [self.params.b20], [self.params.b30], [self.params.b40]]      
        self.acc_data = [[], [], [], [], [], []]
        
        self.x_data = [0] # Will continue with 0.1, 0.2, ...

        # Store parameters
        self.ep = self.params.ep
        self.alph = self.params.alph
        self.points = self.params.points
        self.beta = self.params.beta
        self.lm = self.params.lm

        # To store information right after a rule change
        self.drop_counters = [0, 0, 0, 0]
        self.rise_counters = [0, 0, 0, 0]

        self.fig = self.game.game_mode.fig
        self.ax = self.game.game_mode.axs[1] # Probability graph axis

        # Probability profile lines
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid')
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid')
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid')
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid')

        self.acc_ax = self.game.game_mode.axs[0] # Accuracy graph axis

        # Accuracy profile lines
        self.acc1, = self.acc_ax.plot([], [], 'b', linestyle='dashed')
        self.acc2, = self.acc_ax.plot([], [], 'r', linestyle='dashed')
        self.acc3, = self.acc_ax.plot([], [], 'g', linestyle='dashed')
        self.acc4, = self.acc_ax.plot([], [], 'y', linestyle='dashed')
        self.acc_mean, = self.acc_ax.plot([], [], 'k', linestyle='solid', label='Mean Accuracy')
        self.acc_cumul, = self.acc_ax.plot([], [], 'm', linestyle='solid', label='Cumulative Accuracy')

        self.ax.set_ylim(0, 1) # Probabilities range from 0 to 1
        self.ax.set_xlim(0, 10 + PREDICTION_TIME) # With a prediction time of 1s, the x axis goes from 0 to 11
        self.ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["-10", "-8", "-6", "-4", "-2", "0", "+2", "+4", "+6"])

        # Accuracy ranges from -1 to 1
        self.acc_ax.set_ylim(-1, 1)

        # When a rule change occurs, trigger the corresponding graph changes
        self.game.game_mode.screen.bind("<<blueDrop>>", self.blue_drop)
        self.game.game_mode.screen.bind("<<redDrop>>", self.red_drop)
        self.game.game_mode.screen.bind("<<greenDrop>>", self.green_drop)
        self.game.game_mode.screen.bind("<<yellowDrop>>", self.yellow_drop)

        # Stop the graph when the game ends or the stop graph button is clicked
        self.game.game_mode.screen.bind("<<stopGraph>>", self.stop)

        # Before the graph is displayed, generate the first 1s (or whatever the prediction time is) of predictions
        for num in range(1, 1 + PREDICTION_TIME * 10):
            data = self.generate_one_cycle(-1)
            self.x_data.append(num * .1)
            for num in range(4):
                self.prob_data[num].append(data[num])

        # When a button is clicked, display the graphs and start the animation
        self.game.game_mode.screen.bind("<<buttonClicked>>", self.animate)


    """ Prediction Generation"""
    # generate our predictions for the next frame
    def generate_one_cycle(self, frame):

        self.correct() # Change the parameter values to improve our predictions
        
        # Store the last 1-2 cycles of data
        length = len(self.prob_data[0])
        if length == 1:
            bvals = [[self.prob_data[0][0]], [self.prob_data[1][0]], [self.prob_data[2][0]], [self.prob_data[3][0]]]
        else:
            bvals = [[self.prob_data[0][-2], self.prob_data[0][-1]], [self.prob_data[1][-2], self.prob_data[1][-1]], [self.prob_data[2][-2], self.prob_data[2][-1]], [self.prob_data[3][-2], self.prob_data[3][-1]]]

        # extinction matrix (quantity of decrease by extinction for each behavior)
        em = []

        # reinforcement matrix (quantity of increase by reinforcement for each behavior)
        # am = [] -- commented because it is not in use at the moment

        # Dominance matrix (quantity of increase by dominance for each behavior)
        bm = [0, 0, 0, 0]

        # interaction matrix (the interaction effects between each pair of self.behaviors, before summation)
        # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
        im = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        # populate matrices with values for this cycle
        for y in range(4):
            epEffect = self.calc_ext_change(bvals[y][-1])
            # alphEffect = self.calc_reinf_change(bvals[y][-1])

            em.append(epEffect)
            # am.append(alphEffect)
            bm[y] = self.calc_domin(y, bvals[y][-1], epEffect)

            intEffect = 0
            
            if len(self.freq_data[0]) >= SLOPERANGE:
                for z in range(4):
                    if (y != z):
                        if self.drop_counters[z] > 0: # when we have a rule change, resurgence should happen immediately
                            im[y][z] += self.calc_resurg_immed(y, z)
                        else: # when there is no rule change, resurgence should happen when the frequency curve starts to drop
                            im[y][z] += self.calc_resurg_delay(y, z)

                        if self.rise_counters[z] > 0: # when we have a rule change, autochaining should happen immediately
                            im[y][z] += self.calc_auto_immed(y, z)
                        else: # when there is no rule change, autochaining should happen when the frequency profile starts to rise
                            im[y][z] += self.calc_auto_delay(y, z)
                        

        new_predictions = []

        # For each behavior, calculate the probability of this behavior for this cycle and append it to bvals
        for y in range(4):
            epEffect = em[y]
            # alphEffect = am[y]
            dominanceEffect = bm[y]
            intEffect = 0
            for z in range(4):
                intEffect += im[y][z]
            cur = bvals[y][-1]

            # When a button stops working, we preemptively assume that the dominance of that behavior will go away
            if self.drop_counters[y] > 0:
                dominanceEffect = 0

            # The change in our probability prediction is the sum of all the effects
            change = epEffect + dominanceEffect + intEffect # + alphEffect
            
            # For the first couple frames after a rule change, the curve will be a flat line
            if self.drop_counters[y] > 0:
                # change = -HYPER_DROP_SUBTRACT
                self.drop_counters[y] -= 1
                if self.drop_counters[y] >= HYPER_DROP_LENGTH * 10 - 3:
                    change = 0

            # If we expect initial dominance and program in a higher initial probability for one behavior, we should have at least a small increase in probability for 4s
            init_dominance_counter = 0
            for z in range(4):
                if self.prob_data[y][0] > self.prob_data[z][0]:
                    init_dominance_counter += 1
            if len(self.freq_data[0]) < 40 and init_dominance_counter == 3 and dominanceEffect == 0 and self.drop_counters[y] == 0:
                change = HYPER_BETA_APP_INIT * self.beta

            # Calculate our next prediction, making sure it is between 0 and 1
            bNext = cur + change
            if bNext > 1:
                bNext = 1
            if bNext < 0:
                bNext = 0
            new_predictions.append(bNext)
        
        return new_predictions

    # Update the values of the parameters in response to disparities between the frequency and probability profiles
    def correct(self):
        if len(self.freq_data[0]) >= SLOPERANGE:
            self.change_ep()

            for y in range(4):
                for z in range(4):
                    self.change_resurg(y, z)
                    self.change_auto(y, z)
                self.change_domin(y)

        # Make sure the parameters are still within acceptable ranges
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

   
    """ RULE CHANGE RESPONSE """
    # When we have a rule change, add to the drop counters or rise counters for the correct behavior to initiate graph changes
    def blue_drop(self, event):
        if self.drop_counters[0] == 0:
            self.drop_counters[0] = HYPER_DROP_LENGTH * 10

    def red_drop(self, event):
        if self.drop_counters[1] == 0:
            self.drop_counters[1] = HYPER_DROP_LENGTH * 10

    def green_drop(self, event):
        if self.drop_counters[2] == 0:
            self.drop_counters[2] = HYPER_DROP_LENGTH * 10

    def yellow_drop(self, event):
        if self.drop_counters[3] == 0:
            self.drop_counters[3] = HYPER_DROP_LENGTH * 10
    
    
    """ PARAMETER APPLICATION EQUATIONS"""
    # extinction
    def calc_ext_change(self, cur):
        # return -self.ep*cur -- alternative option for extinction where the rate of decrease depends on the behavioral value; leads to exponential decay and difficulty reaching high values
        return -self.ep/HYPER_EP_APP
    
    # def calc_reinf_change(self, cur):
    #     return -self.alph*(1 - cur)
    #     #return self.alph/HYPER_ALPH_APP
    
    # Delayed resurgence -- one behavior decreasing causes another to rise
    def calc_resurg_delay(self, y, y_prime):
        # if another behavior's frequency curve is decreasing and has a negative lambda with behavior y
        if self.lm[y][y_prime] < 0 and self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE] < 0:
            # the change is dependent upon the lambda value and the slope of the alternate behavior; the greater the absolute value of either, the greater the effect
            return HYPER_RESURG_DELAY_APP * self.lm[y][y_prime] * (self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE])
        return 0
    
    # same as delayed resurgence, but looks at slope of probability curve rather than frequency curve
    def calc_resurg_immed(self, y, y_prime):
        if self.lm[y][y_prime] < 0 and self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE] < 0:
            return HYPER_RESURG_IMMED_APP * self.lm[y][y_prime] * (self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE])
        return 0
        
    # delayed autochaining -- one behavior increasing causes another to rise
    def calc_auto_delay(self, y, y_prime):
        # if another behavior's frequency curve is decreasing and has a positive lambda with y
        if self.lm[y][y_prime] > 0 and self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE] > 0:
            # change is dependent upon the probability value of y and y prime -- the effect is stronger when y is smaller and y prime is greater (y prime "pulls up" y)
            return (1 - self.prob_data[y][-1]) * self.lm[y][y_prime] * self.prob_data[y_prime][-1]
        return 0
    
    # Same as delayed autochaining but the if condition checks probability slope instead of frequency slope
    def calc_auto_immed(self, y, y_prime):
        if self.lm[y][y_prime] > 0 and self.prob_data[y_prime][-1] - self.prob_data[y_prime][-SLOPERANGE] > 0:
            return (1 - self.prob_data[y][-1]) * self.lm[y][y_prime] * self.prob_data[y_prime][-1]
        return 0
        
    # The next four equations all rely upon a yet-to-be implemented parameter called phi; while the previous equations all generate increase, these generate decrease
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

    # Dominance effect -- one behavior being greater than all the others causes it to rise
    def calc_domin(self, y, cur, epEffect):
        dominanceCounter = 0
        dominanceDenominator = self.beta # when beta is greater, the other components of the denominator play a lesser role and the increase is greater

        if len(self.freq_data[0]) >= SLOPERANGE:
            freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
            
            for z in range(4):
                if y != z:
                    freq_slope_z = self.freq_data[z][-1] - self.freq_data[z][-SLOPERANGE]
                    dominanceDenominator += self.freq_data[z][-1] # add to the denominator the frequency value of each other denominator -- the smaller they are, the greater the increase

                    # if frequency of y is greater than frequency of z
                    if self.freq_data[y][-1] > self.freq_data[z][-1] + .1:
                        dominanceCounter += 1
                    
            # if y is greater than all other behaviors and its frequency profile does not have 0 slope
            if dominanceCounter == 3 and freq_slope_y >= -0.03 and dominanceDenominator != 0:
                # effect is greater when y probability value is lower, when beta is higher, and when the other frequency values are lower
                if cur < .5:
                    return .5 * self.beta * self.beta/(HYPER_BETA_APP*dominanceDenominator)
                if cur >= .5:
                    return (1 - cur) * self.beta * self.beta/(HYPER_BETA_APP*dominanceDenominator)
            return 0
        
        # If we don't yet have any frequency data to work with
        else:
            for z in range(4):
                if y != z:
                    dominanceDenominator += self.prob_data[z][-1]
                    if self.prob_data[y][-1] > self.prob_data[z][-1]:
                        dominanceCounter += 1
            # If the researcher expects initial dominance, create a very slight increase
            if dominanceCounter == 3 and dominanceDenominator != 0:
                return HYPER_BETA_APP_INIT * self.beta - epEffect
            return 0

    
    """ PARAMETER UPDATE EQUATIONS """
    # Update parameters in response to frequency profile feedback

    # Change epsilon
    def change_ep(self):
        change = 0
        for n in range(4):
            freq_slope = self.freq_data[n][-1] - self.freq_data[n][-SLOPERANGE]
            prob_slope = self.prob_data[n][-1 - PREDICTION_TIME] - self.prob_data[n][-SLOPERANGE - PREDICTION_TIME]
            
            # if the frequency slope is negative, then extinction is occuring, so we can use this as a learning opportunity
            if freq_slope < -0.01:
                change += prob_slope - freq_slope # If we are overshooting, increase epsilon to strengthen extinction, and vice versa
        self.ep += change / HYPER_EP_CHANGE
    
    # Change lambda in the context of resurgence
    def change_resurg(self, y, y_prime):
        freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        freq_slope_y_prime = self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE]

        prob_slope_y = self.prob_data[y][-1 - PREDICTION_TIME] - self.prob_data[y][-SLOPERANGE - PREDICTION_TIME]

        # if resurgence is occurring
        if freq_slope_y > 0 and freq_slope_y_prime < 0:
            # Make lambda more negative if we are undershooting to increase strength of resurgence, and vice versa
            self.lm[y][y_prime] -= (freq_slope_y - prob_slope_y) / HYPER_RESURG_CHANGE

    # Change lambda in the context of autochaining
    def change_auto(self, y, y_prime):
        freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        freq_slope_y_prime = self.freq_data[y_prime][-1] - self.freq_data[y_prime][-SLOPERANGE]

        prob_slope_y = self.prob_data[y][-1 - PREDICTION_TIME] - self.prob_data[y][-SLOPERANGE - PREDICTION_TIME]
        prob_slope_y_prime = self.prob_data[y_prime][-1 - PREDICTION_TIME] - self.prob_data[y_prime][-SLOPERANGE - PREDICTION_TIME]

        # if autochaining is occuring
        if freq_slope_y > 0 and freq_slope_y_prime > 0:
            # for both lambdas, increase lambda if we are undershooting and decrease it if we are overshooting
            self.lm[y][y_prime] += (freq_slope_y - prob_slope_y) / HYPER_AUTO_CHANGE
            self.lm[y_prime][y] += (freq_slope_y_prime - prob_slope_y_prime) / HYPER_AUTO_CHANGE

    # Change beta when dominance is occuring
    def change_domin(self, y):

        # freq_slope_y = self.freq_data[y][-1] - self.freq_data[y][-SLOPERANGE]
        
        dominanceCounter = 0
        for z in range(4):
            if y != z:

                if self.freq_data[y][-1] > self.freq_data[z][-1]:
                    dominanceCounter += 1
                
        # if dominanceCounter == 3 and freq_slope_y >= -0.03: -- alternate condition where we ensure that the frequency profile is not decreasing
        if dominanceCounter == 3: # if dominance is occurring
            # self.beta += (freq_slope_y - prob_slope_y) / HYPER_BETA_CHANGE --  alternate change mechanism where we use slope instead of value
            change = (self.freq_data[y][-1] - self.prob_data[y][-1 - PREDICTION_TIME]) / HYPER_BETA_CHANGE # if we are undershooting increase beta, and vice versa
            self.beta += change

    
    """ Graph Generation """
    def accuracy_graph(self, frame):
            
        # Calculate Cohen's kappa for agreement between probability profile and frequency profile at each frame
        if len(self.freq_data[0]) >= 1:
            avg_po = 0 # average percentage agreement between probability profile and frequency profile at this frame

            pe = 2/3 # expected percentage agreement between probability and frequency profiles, given that the average distance between 2 numbers between 0 and 1 is 1/3
            for n in range(4): # for each behavior
                po = 1 - abs(self.freq_data[n][-1] - self.prob_data[n][-1 - PREDICTION_TIME * 10]) # percentage agreement is 1 minus the distance between the curves
                numerator = po - pe
                denominator = 1 - pe
                kappa = numerator / denominator # positive if we are doing better than chance, negative if we are doing worse
                self.acc_data[n].append(kappa) # add this to the accuracy data over time for this behavior

                avg_po += po

            # Calculate general kappa
            avg_po /= 4
            numerator = avg_po - pe
            denominator = 1 - pe
            general_kappa = numerator / denominator
            self.acc_data[4].append(general_kappa)
        
            x_data = self.game.game_mode.x_data

            # Calculate the average general kappa across the trial thus far
            avg_mean_acc = 0
            length = len(self.acc_data[0])
            if length >= 1:
                for i in range(length):
                    avg_mean_acc += self.acc_data[4][i]
                avg_mean_acc /= length
                self.acc_data[5].append(avg_mean_acc)

            # if we are <10s in, show all the data
            if frame <= 100:
                self.acc1.set_data(x_data, self.acc_data[0])
                self.acc2.set_data(x_data, self.acc_data[1])
                self.acc3.set_data(x_data, self.acc_data[2])
                self.acc4.set_data(x_data, self.acc_data[3])
                self.acc_mean.set_data(x_data, self.acc_data[4])
                self.acc_cumul.set_data(x_data, self.acc_data[5])

            # if we are >10s in, only show the last 10s of data
            if frame > 100:
                self.acc1.set_data(x_data[-100:], self.acc_data[0][-100:])
                self.acc2.set_data(x_data[-100:], self.acc_data[1][-100:])
                self.acc3.set_data(x_data[-100:], self.acc_data[2][-100:])
                self.acc4.set_data(x_data[-100:], self.acc_data[3][-100:])
                self.acc_mean.set_data(x_data[-100:], self.acc_data[4][-100:])
                self.acc_cumul.set_data(x_data[-100:], self.acc_data[5][-100:])
    
    def genGraph(self, frame):
        # Generate a list of behavioral probabilities over time
        
        # get the probability values for this frame
        b_values = self.generate_one_cycle(frame)

        # append the timestamp and the probability values at that timestamp
        self.x_data.append((frame * .1) + PREDICTION_TIME)
        for num in range(4):
            self.prob_data[num].append(b_values[num])

        # if we are less than 10s in, the window is 0-10
        window_start = 0
        if frame <= 100:
            self.line1.set_data(self.x_data, self.prob_data[0])
            self.line2.set_data(self.x_data, self.prob_data[1])
            self.line3.set_data(self.x_data, self.prob_data[2])
            self.line4.set_data(self.x_data, self.prob_data[3])

        # if we are more than 10s in, the window is the last 10s
        if frame > 100:
            window_start = frame/10 - 10

            self.line1.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[0][-100 - 10 * PREDICTION_TIME:])
            self.line2.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[1][-100 - 10 * PREDICTION_TIME:])
            self.line3.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[2][-100 - 10 * PREDICTION_TIME:])
            self.line4.set_data(self.x_data[-100 - 10 * PREDICTION_TIME:], self.prob_data[3][-100 - 10 * PREDICTION_TIME:])

        # set the x limits to reflect our window
        self.ax.set_xlim(window_start, window_start + 10 + PREDICTION_TIME)

        # record frequency data
        self.game.game_mode.record_data(frame)

        # generate accuracy data
        self.accuracy_graph(frame)

        # store all the data in the databases for post-hoc analysis
        self.record()

        # return frequency lines, probability lines, and accuracy lines
        return (self.game.game_mode.line1, self.game.game_mode.line2, self.game.game_mode.line3, self.game.game_mode.line4, 
                self.line1, self.line2, self.line3, self.line4,
                self.acc1, self.acc2, self.acc3, self.acc4, self.acc_mean, self.acc_cumul)
    
    # show and animate the graphs
    def animate(self, event):
        # run genGraph to update the graphs every 100 ms (.1s)
        self.ani = FuncAnimation(self.fig, self.genGraph, frames=itertools.count(), interval=100, blit=True, save_count=MAX_FRAMES)

        self.fig.set_figheight(7)
        
        # Labels
        self.ax.set_ylabel('Behavioral Probabilities')
        self.fig.legend()

        self.game.game_mode.ax.set_xlabel('Time to present (seconds)')
        self.game.game_mode.ax.set_ylabel('Behavioral Frequencies')
        self.game.game_mode.fig.legend()

        self.acc_ax.set_ylabel("Accuracy (Cohen's kappa)")

        plt.show()

    
    """ Other Functions """
    # Store data in tables so we can access and graph later
    def record(self):
        freq = self.game.game_mode.freq_data
        mode = self.game.game_mode.mode_char
        name = self.game.game_mode.player_name
        time = self.game.game_mode.timer.time_elapsed()
        trial = self.game.game_mode.trial_number

        # Store data on Frequencies, Probabilities, Accuracies, and Parameters over the course of the trial
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

    # stop the animation
    def stop(self, event):
        self.ani.event_source.stop()