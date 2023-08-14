import sqlite3

import csv

class Converter:
    def __init__(self, name, mode, trial):

        self.raw_data = sqlite3.connect('freqprof.db')
        self.Cursor = self.raw_data.cursor()

        self.name = name
        self.mode = mode
        self.trial = trial

    def convert(self):

        self.Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ?', 
                    (self.name, self.mode, self.trial))
        subset = self.Cursor.fetchall()

        for n in range(len(subset) - 1):
            if subset[n][0] + 1 != subset[n + 1][0]:
                print("Error: sample is not continuous, may be a combination of multiple trials")

        toAdd = [[], []]

        subset_list = []
        for row in subset:
            subset_list.append(list(row))

        starting_id = subset_list[0][0]

        subset_list[0][6] = (int(10 * subset_list[0][6])) / 10
        for n in range(len(subset_list) - 1):
            subset_list[n + 1][6] = (int(10 * subset_list[n + 1][6])) / 10
            interval = subset_list[n + 1][6] - subset_list[n][6]
            numMissing = round(interval * 10) - 1
            # print("n: " + str(subset_list[n][6]) + "  n + 1: " + str(subset_list[n + 1][6]) + "  numMissing: " + str(numMissing))
            toAdd[0].append(subset_list[n][0])
            toAdd[1].append(numMissing)

        new_row_counter = 0

        for i in range(len(toAdd[0])):
        #for i in range(2):
            new_rows = []
            for j in range(toAdd[1][i]):
                new_rows.append([subset_list[toAdd[0][i] - starting_id + new_row_counter][0] + 0.5, 0, 0, 0, 0, 0, round((10 * (subset_list[toAdd[0][i] - starting_id + new_row_counter][6] + (j + 1)/10))) / 10, 'B', 'RealSteven', 2])
            subset_list = subset_list[:toAdd[0][i] - starting_id + 1 + new_row_counter] + new_rows + subset_list[toAdd[0][i] - starting_id + 1 + new_row_counter:]
            new_row_counter += toAdd[1][i]

        to_export = [row[1:5] for row in subset_list]

        test_file = f"{self.name}_{self.mode}_{self.trial}.csv"

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
