"""convert.py"""

import sqlite3

# Read from and write to csv files
import csv

from matplotlib import pyplot as plt

# Selects data for 1 game from SQLite database, then converts it to a CSV file that is ready to be turned into a frequency profile
class Converter:

    # Creates database connection, stores game information: user name, game mode, and trial number
    def __init__(self, name, mode, trial):

        self.raw_data = sqlite3.connect('freqprof.db')
        self.Cursor = self.raw_data.cursor()

        self.name = name
        self.mode = mode
        self.trial = trial

        self.fig, self.axs = plt.subplots(3, 1, sharex=False, sharey=False)

    def convert(self):

        """Frequency Graph"""
        # Select data from database that has the desired user name, game mode, and trial number
        self.Cursor.execute('SELECT id, time, B1, B2, B3, B4 FROM Frequencies WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        freq_subset = self.Cursor.fetchall()

        # Print error message to terminal if sample is not continuous
        for n in range(len(freq_subset) - 1):
            if freq_subset[n][0] + 1 != freq_subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        # Convert database subset to list
        freq_list = []
        for row in freq_subset:
            freq_list.append(list(row))

        # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
        freq_starting_id = freq_list[0][0]

        freq_line1, = self.axs[0].plot(freq_list[1], freq_list[2], 'b', linestyle='solid', label="Behavior 1")
        freq_line2, = self.axs[0].plot(freq_list[1], freq_list[3], 'r', linestyle='solid', label="Behavior 2")
        freq_line3, = self.axs[0].plot(freq_list[1], freq_list[4], 'g', linestyle='solid', label="Behavior 3")
        freq_line4, = self.axs[0].plot(freq_list[1], freq_list[5], 'r', linestyle='solid', label="Behavior 4")


        """Probability Graph"""
        # Select data from database that has the desired user name, game mode, and trial number
        self.Cursor.execute('SELECT id, time, B1, B2, B3, B4 FROM Probabilities WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        prob_subset = self.Cursor.fetchall()

        # Print error message to terminal if sample is not continuous
        for n in range(len(prob_subset) - 1):
            if prob_subset[n][0] + 1 != prob_subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        # Convert database subset to list
        prob_list = []
        for row in prob_subset:
            prob_list.append(list(row))

        # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
        prob_starting_id = prob_list[0][0]

        prob_line1, = self.axs[1].plot(prob_list[1], prob_list[2], 'b', linestyle='solid')
        prob_line2, = self.axs[1].plot(prob_list[1], prob_list[3], 'r', linestyle='solid')
        prob_line1, = self.axs[1].plot(prob_list[1], prob_list[4], 'g', linestyle='solid')
        prob_line1, = self.axs[1].plot(prob_list[1], prob_list[5], 'r', linestyle='solid')


        """Parameter Graph"""
        # Select data from database that has the desired user name, game mode, and trial number
        self.Cursor.execute('SELECT id, time, epsilon, alpha, l12, l13, l14, l21, l23, l24, l31, l32, l34, l41, l42, l43 FROM Parameters WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        param_subset = self.Cursor.fetchall()

        # Print error message to terminal if sample is not continuous
        for n in range(len(param_subset) - 1):
            if param_subset[n][0] + 1 != param_subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        # Convert database subset to list
        param_list = []
        for row in param_subset:
            param_list.append(list(row))

        # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
        param_starting_id = param_list[0][0]

        param_line_ep, = self.axs[2].plot(param_list[1], param_list[2], 'b', linestyle='solid', label="Epsilon")
        param_line_alph, = self.axs[2].plot(param_list[1], param_list[3], 'r', linestyle='solid', label="Alpha")
        param_line_l12, = self.axs[2].plot(param_list[1], param_list[4], 'g', linestyle='solid', label="lambda12")
        param_line_l13, = self.axs[2].plot(param_list[1], param_list[5], 'y', linestyle='solid', label="lambda13")
        param_line_l14, = self.axs[2].plot(param_list[1], param_list[6], 'b', linestyle='dashed', label="lambda14")
        param_line_l21, = self.axs[2].plot(param_list[1], param_list[7], 'r', linestyle='dashed', label="lambda21")
        param_line_l23, = self.axs[2].plot(param_list[1], param_list[8], 'g', linestyle='dashed', label="lambda23")
        param_line_l24, = self.axs[2].plot(param_list[1], param_list[9], 'y', linestyle='dashed', label="lambda24")
        param_line_l31, = self.axs[2].plot(param_list[1], param_list[10], 'c', linestyle='solid', label="lambda31")
        param_line_l32, = self.axs[2].plot(param_list[1], param_list[11], 'm', linestyle='solid', label="lambda32")
        param_line_l34, = self.axs[2].plot(param_list[1], param_list[12], 'k', linestyle='solid', label="lambda34")
        param_line_l41, = self.axs[2].plot(param_list[1], param_list[13], 'c', linestyle='dashed', label="lambda41")
        param_line_l42, = self.axs[2].plot(param_list[1], param_list[14], 'm', linestyle='dashed', label="lambda42")
        param_line_l43, = self.axs[2].plot(param_list[1], param_list[15], 'k', linestyle='dashed', label="lambda43")

        self.fig.legend()
        self.fig.set_figheight(9)

        self.axs[2].set_xlabel("Time")
        self.axs[0].set_ylabel("Frequencies")
        self.axs[1].set_ylabel("Probabilities")
        self.axs[2].set_ylabel("Parameters")

        plt.show()

converter = Converter('Steven8', 'A', 1)
converter.convert()
