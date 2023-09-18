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

        freq_line1, = self.axs[0].plot([row[1] for row in freq_list], [row[2] for row in freq_list], 'b', linestyle='solid', label="Behavior 1")
        freq_line2, = self.axs[0].plot([row[1] for row in freq_list], [row[3] for row in freq_list], 'r', linestyle='solid', label="Behavior 2")
        freq_line3, = self.axs[0].plot([row[1] for row in freq_list], [row[4] for row in freq_list], 'g', linestyle='solid', label="Behavior 3")
        freq_line4, = self.axs[0].plot([row[1] for row in freq_list], [row[5] for row in freq_list], 'y', linestyle='solid', label="Behavior 4")


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

        prob_line1, = self.axs[1].plot([row[1] for row in prob_list], [row[2] for row in prob_list], 'b', linestyle='solid')
        prob_line2, = self.axs[1].plot([row[1] for row in prob_list], [row[3] for row in prob_list], 'r', linestyle='solid')
        prob_line1, = self.axs[1].plot([row[1] for row in prob_list], [row[4] for row in prob_list], 'g', linestyle='solid')
        prob_line1, = self.axs[1].plot([row[1] for row in prob_list], [row[5] for row in prob_list], 'y', linestyle='solid')


        """Parameter Graph"""
        # Select data from database that has the desired user name, game mode, and trial number
        self.Cursor.execute('SELECT id, time, beta, alpha, l12, l13, l14, l21, l23, l24, l31, l32, l34, l41, l42, l43 FROM upParameters WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        param_subset = self.Cursor.fetchall()

        self.Cursor.execute('SELECT id, time, epsilon from downParameters WHERE name = ? AND mode = ? AND trial = ?',
                            (self.name, self.mode, self.trial))
        epsilon_subset = self.Cursor.fetchall()

        # Print error message to terminal if sample is not continuous
        for n in range(len(param_subset) - 1):
            if param_subset[n][0] + 1 != param_subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        # Convert database subset to list
        param_list = []
        for row in param_subset:
            param_list.append(list(row))
        
        epsilon_list = []
        for row in epsilon_subset:
            epsilon_list.append(list(row))

        # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
        param_starting_id = param_list[0][0]

        param_line_beta, = self.axs[2].plot([row[1] for row in param_list], [row[2] for row in param_list], 'b', linestyle='dotted', label="Beta")
        param_line_alph, = self.axs[2].plot([row[1] for row in param_list], [row[3] for row in param_list], 'r', linestyle='dotted', label="Alpha")
        param_line_l12, = self.axs[2].plot([row[1] for row in param_list], [row[4] for row in param_list], 'g', linestyle='dotted', label="lambda12")
        param_line_l13, = self.axs[2].plot([row[1] for row in param_list], [row[5] for row in param_list], 'y', linestyle='dotted', label="lambda13")
        param_line_l14, = self.axs[2].plot([row[1] for row in param_list], [row[6] for row in param_list], 'b', linestyle='dashed', label="lambda14")
        param_line_l21, = self.axs[2].plot([row[1] for row in param_list], [row[7] for row in param_list], 'r', linestyle='dashed', label="lambda21")
        param_line_l23, = self.axs[2].plot([row[1] for row in param_list], [row[8] for row in param_list], 'g', linestyle='dashed', label="lambda23")
        param_line_l24, = self.axs[2].plot([row[1] for row in param_list], [row[9] for row in param_list], 'y', linestyle='dashed', label="lambda24")
        param_line_l31, = self.axs[2].plot([row[1] for row in param_list], [row[10] for row in param_list], 'c', linestyle='solid', label="lambda31")
        param_line_l32, = self.axs[2].plot([row[1] for row in param_list], [row[11] for row in param_list], 'm', linestyle='solid', label="lambda32")
        param_line_l34, = self.axs[2].plot([row[1] for row in param_list], [row[12] for row in param_list], 'k', linestyle='solid', label="lambda34")
        param_line_l41, = self.axs[2].plot([row[1] for row in param_list], [row[13] for row in param_list], 'c', linestyle='dashed', label="lambda41")
        param_line_l42, = self.axs[2].plot([row[1] for row in param_list], [row[14] for row in param_list], 'm', linestyle='dashed', label="lambda42")
        param_line_l43, = self.axs[2].plot([row[1] for row in param_list], [row[15] for row in param_list], 'k', linestyle='dashed', label="lambda43")
        param_line_ep, = self.axs[2].plot([row[1] for row in epsilon_list], [row[2] for row in epsilon_list], 'c', linestyle='dotted', label="Epsilon")


        self.fig.legend()
        self.fig.set_figheight(9)

        self.axs[2].set_xlabel("Time")
        self.axs[0].set_ylabel("Frequencies")
        self.axs[1].set_ylabel("Probabilities")
        self.axs[2].set_ylabel("Parameters")

        plt.show()

converter = Converter('Vicky', '1', 1)
converter.convert()
