# Database
import sqlite3

# Read from and write to csv files
import csv

# Selects data for 1 game from SQLite database, then converts it to a CSV file that is ready to be turned into a frequency profile
class Converter:

    # Creates database connection, stores game information: user name, game mode, and trial number
    def __init__(self, name, mode, trial):

        self.raw_data = sqlite3.connect('freqprof.db')
        self.Cursor = self.raw_data.cursor()

        self.name = name
        self.mode = mode
        self.trial = trial

    # Conversion function: inserts additional rows of all zeros such that the CSV file has 1 row for every .1 seconds of the trial
    def convert(self):

        # Select data from database that has the desired user name, game mode, and trial number
        self.Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        subset = self.Cursor.fetchall()

        # Print error message to terminal if sample is not continuous
        for n in range(len(subset) - 1):
            if subset[n][0] + 1 != subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        # List to record how many additional data points need to be inserted after each row; 0th element stores row IDs and 1st element stores # of rows to add
        toAdd = [[], []]

        # Convert database subset to list
        subset_list = []
        for row in subset:
            subset_list.append(list(row))

        # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
        starting_id = subset_list[0][0]

        # Round the 1st timestamp to the nearest 1/10 of a second
        subset_list[0][6] = (int(10 * subset_list[0][6])) / 10

        # For each row in the data, calculate how many rows we must add after this row
        for n in range(len(subset_list) - 1):

            # Round next timestamp to the nearest 1/10 of a second
            subset_list[n + 1][6] = (int(10 * subset_list[n + 1][6])) / 10

            # Calculate how many 1/10 second intervals are missing between this data point and the next
            interval = subset_list[n + 1][6] - subset_list[n][6]
            numMissing = round(interval * 10) - 1
            # print("n: " + str(subset_list[n][6]) + "  n + 1: " + str(subset_list[n + 1][6]) + "  numMissing: " + str(numMissing))

            # Store information about how many rows to add and where to add them
            toAdd[0].append(subset_list[n][0])
            toAdd[1].append(numMissing)

        new_row_counter = 0

        # Add rows after each row
        for i in range(len(toAdd[0])):
            
            # Index into data using the toAdd list, then add the correct number of rows filled with all zeros
            new_rows = []
            for j in range(toAdd[1][i]):
                new_rows.append([subset_list[toAdd[0][i] - starting_id + new_row_counter][0] + 0.5, 0, 0, 0, 0, 0, round((10 * (subset_list[toAdd[0][i] - starting_id + new_row_counter][6] + (j + 1)/10))) / 10, self.mode, self.name, self.trial])
            subset_list = subset_list[:toAdd[0][i] - starting_id + 1 + new_row_counter] + new_rows + subset_list[toAdd[0][i] - starting_id + 1 + new_row_counter:]
            
            # Keep track of how many rows were added, for indexing purposes
            new_row_counter += toAdd[1][i]

        # Export only the behavioral data, the labeling data will be stored in the title of the CSV file
        to_export = [row[1:5] for row in subset_list]

        # CSV file title with user name, game mode, and trial number
        test_file = f"{self.name}_{self.mode}_{self.trial}.csv"

        # Write data to CSV file
        with open(test_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            
            column_names = ['B1', 'B2', 'B3', 'B4']
            csv_writer.writerow(column_names)

            csv_writer.writerows(to_export)

# Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? ORDER BY id ASC LIMIT 1',
#                        ('RealSteven', 'B', 2))
# first = Cursor.fetchall()

# Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? ORDER BY id DESC LIMIT 1',
#                        ('RealSteven', 'B', 2))
# last = Cursor.fetchall()

# Cursor.execute("CREATE TABLE test ")

# print(first)
# print(last)
# print(last[0][6] - first[0][6])
