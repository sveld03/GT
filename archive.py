# Archived Code


"""game.py"""
# def update_data(self):
    #     if self.screen.button_states['btnB'] == 1:
    #         record_blue(self.screen.game_mode.Cursor, self.screen.game_mode.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
    #     elif self.screen.button_states['btnR'] == 1:
    #         record_red(self.screen.game_mode.Cursor, self.screen.game_mode.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
    #     elif self.screen.button_states['btnG'] == 1:
    #         record_green(self.screen.game_mode.Cursor, self.screen.game_mode.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
    #     elif self.screen.button_states['btnY'] == 1:
    #         record_yellow(self.screen.game_mode.Cursor, self.screen.game_mode.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())
    #     else:
    #         record_none(self.screen.game_mode.Cursor, self.screen.game_mode.freqprof, self.screen.game_mode.timer, self.mode_label, self.screen.nameNtr.get(), self.screen.trialNtr.get())

    #     for button in self.screen.button_states:
    #         self.screen.button_states[button] = 0

    #     self.screen.after(100, self.update_data)


"""ui.R"""
# library(shiny)
# library(magrittr)

# ui <- shinyServer(fluidPage(
#   plotOutput("first_column")
# ))


"""server.R"""
# library(shiny)
# library(magrittr)

# library(shiny)
# library(magrittr)

# ui <- shinyServer(fluidPage(
#   plotOutput("first_column")
# ))

# full_data <<- read.csv("test20.csv", header = TRUE)

# x <- 1

# server <- shinyServer(function(input, output, session){
#   # Function to get new observations
#   get_new_data <- function(){
#     data <- full_data[x:(x+4),] %>% rbind %>% data.frame
#     return(data)
#   }

#   # Initialize my_data
#   my_data <<- get_new_data()

#   # Function to update my_data
#   update_data <- function(){
#     my_data <<- rbind(my_data, get_new_data())
#     x <<- x + 5
#   }

#   # Plot the 30 most recent values
#   output$first_column <- renderPlot({
#     print("Render")
#     invalidateLater(1000, session)
#     update_data()
#     print(my_data)
#     plot(B1 ~ 1, data=my_data, ylim=c(-3, 3), las=1, type="l")
#   })
# })

# # shinyApp(ui=ui, server=server)


"""chatGPTfreq.py"""
# import matplotlib.pyplot as plt
# import threading
# import time

# # Initialize lists to store button press frequencies
# colors = ['blue', 'red', 'green', 'yellow']
# button_presses = [[] for _ in colors]

# # Function to update the plot in real-time
# def update_plot():
#     plt.ion()  # Turn on interactive mode
#     fig, ax = plt.subplots()

#     lines = [ax.plot([], label=color)[0] for color in colors]
#     ax.set_xlim(0, 10)  # Adjust the x-axis limits as needed
#     ax.set_ylim(0, 10)  # Adjust the y-axis limits as needed
#     ax.set_xlabel('Time (seconds)')
#     ax.set_ylabel('Button Press Frequency')
#     ax.legend()

#     while True:
#         for i, line in enumerate(lines):
#             line.set_xdata(list(range(len(button_presses[i]))))
#             line.set_ydata(button_presses[i])
#         ax.relim()
#         ax.autoscale_view()
#         plt.pause(0.1)  # Pause to update the plot

# # Function to simulate button presses and update the lists
# def simulate_button_presses():
#     while True:
#         try:
#             button_index = int(input("Enter button index (0-blue, 1-red, 2-green, 3-yellow): "))
#             if 0 <= button_index < len(colors):
#                 button_presses[button_index].append(len(button_presses[button_index]) + 1)
#         except ValueError:
#             print("Invalid input. Please enter a valid button index.")

# # Start the real-time plot update thread
# plot_thread = threading.Thread(target=update_plot)
# plot_thread.daemon = True  # Allow the thread to exit when the main program exits
# plot_thread.start()

# # Start the button press simulation thread
# simulate_thread = threading.Thread(target=simulate_button_presses)
# simulate_thread.daemon = True
# simulate_thread.start()

# # Keep the main thread running
# while True:
#     pass


"""convert.py"""
# Database
# import sqlite3

# # Read from and write to csv files
# import csv

# # Selects data for 1 game from SQLite database, then converts it to a CSV file that is ready to be turned into a frequency profile
# class Converter:

#     # Creates database connection, stores game information: user name, game mode, and trial number
#     def __init__(self, name, mode, trial):

#         self.raw_data = sqlite3.connect('freqprof.db')
#         self.Cursor = self.raw_data.cursor()

#         self.name = name
#         self.mode = mode
#         self.trial = trial

#     # Conversion function: inserts additional rows of all zeros such that the CSV file has 1 row for every .1 seconds of the trial
#     def convert(self):

#         # Select data from database that has the desired user name, game mode, and trial number
#         self.Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ?', 
#                     (self.name, self.mode, self.trial))
#         subset = self.Cursor.fetchall()

#         # Print error message to terminal if sample is not continuous
#         for n in range(len(subset) - 1):
#             if subset[n][0] + 1 != subset[n + 1][0]:
#                 print("Error: sample is not continuous, may be a combination of multiple trials")

#         # List to record how many additional data points need to be inserted after each row; 0th element stores row IDs and 1st element stores # of rows to add
#         toAdd = [[], []]

#         # Convert database subset to list
#         subset_list = []
#         for row in subset:
#             subset_list.append(list(row))

#         # Keep track of ID of first row of subset, to be subtracted from other IDs for indexing purposes
#         starting_id = subset_list[0][0]

#         # Round the 1st timestamp to the nearest 1/10 of a second
#         subset_list[0][6] = (int(10 * subset_list[0][6])) / 10

#         # For each row in the data, calculate how many rows we must add after this row
#         for n in range(len(subset_list) - 1):

#             # Round next timestamp to the nearest 1/10 of a second
#             subset_list[n + 1][6] = (int(10 * subset_list[n + 1][6])) / 10

#             # Calculate how many 1/10 second intervals are missing between this data point and the next
#             interval = subset_list[n + 1][6] - subset_list[n][6]
#             numMissing = round(interval * 10) - 1
#             # print("n: " + str(subset_list[n][6]) + "  n + 1: " + str(subset_list[n + 1][6]) + "  numMissing: " + str(numMissing))

#             # Store information about how many rows to add and where to add them
#             toAdd[0].append(subset_list[n][0])
#             toAdd[1].append(numMissing)

#         new_row_counter = 0

#         # Add rows after each row
#         for i in range(len(toAdd[0])):
            
#             # Index into data using the toAdd list, then add the correct number of rows filled with all zeros
#             new_rows = []
#             for j in range(toAdd[1][i]):
#                 new_rows.append([subset_list[toAdd[0][i] - starting_id + new_row_counter][0] + 0.5, 0, 0, 0, 0, 0, round((10 * (subset_list[toAdd[0][i] - starting_id + new_row_counter][6] + (j + 1)/10))) / 10, self.mode, self.name, self.trial])
#             subset_list = subset_list[:toAdd[0][i] - starting_id + 1 + new_row_counter] + new_rows + subset_list[toAdd[0][i] - starting_id + 1 + new_row_counter:]
            
#             # Keep track of how many rows were added, for indexing purposes
#             new_row_counter += toAdd[1][i]

#         # Export only the behavioral data, the labeling data will be stored in the title of the CSV file
#         to_export = [row[1:5] for row in subset_list]

#         # CSV file title with user name, game mode, and trial number
#         test_file = f"Data/{self.name}_{self.mode}_{self.trial}.csv"

#         # Write data to CSV file
#         with open(test_file, 'w', newline='') as file:
#             csv_writer = csv.writer(file)
            
#             column_names = ['B1', 'B2', 'B3', 'B4']
#             csv_writer.writerow(column_names)

#             csv_writer.writerows(to_export)

# # Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? ORDER BY id ASC LIMIT 1',
# #                        ('RealSteven', 'B', 2))
# # first = Cursor.fetchall()

# # Cursor.execute('SELECT * FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? ORDER BY id DESC LIMIT 1',
# #                        ('RealSteven', 'B', 2))
# # last = Cursor.fetchall()

# # Cursor.execute("CREATE TABLE test ")

# # print(first)
# # print(last)
# # print(last[0][6] - first[0][6])


"""full.py"""
# # touchscreen.py

# # # import modeA

# # # graphics library
# # from tkinter import *

# # # # data visualization
# # # import matplotlib as mpl
# # # import matplotlib.pyplot as plt
# # # import numpy as np

# # import random

# # random.seed(1965)

# from utilities import *

# from modeA import *

# class Game(Tk):
#     def __init__(self):
#         super().__init__()

#         # for the easy version
#         self.title("The Hard Easy Game")

#         # set geometry (widthxheight)
#         self.geometry('1360x710')

#         self.resizable(width=False, height=False)

#         # instructions
#         subtitle = Label(self, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
#         subtitle.place(anchor='nw')

#         self.finish = Label(self, text="Finish Line")
#         self.finish.place(x=1235, y=125)

#         self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')

#         self.canvas = Canvas(self, bg="white", width=1250, height = 500)
#         self.canvas.place(x=50, y=150)
#         # self.canvas.pack(fill=BOTH, padx=50, pady=150, expand=True)

#         # self.canvas.bind("<Configure>", self.on_resize)

#         # initial position of dot
#         dot_radius = 20
#         self.init_x1 = 50 - dot_radius
#         self.init_y1 = 250 - dot_radius
#         self.init_x2 = 50 + dot_radius
#         self.init_y2 = 250 + dot_radius

#         # create dot
#         self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
#                          self.init_x2, self.init_y2,
#                          outline='red', fill='red')
        
#         self.line = self.canvas.create_line(1225, 0, 1225, 500)
        
#         # self.update_dot_position("<Configure>")
        
#         self.game_mode = None

#         self.create_buttons()
#         self.create_menu()

#         self.move_B = ['g', 'y', 'r', 'b']
#         self.move_C1 = ['g', 'g']
#         self.move_C2 = ['r', 'y']
#         self.input_seqB = []
#         self.input_seqC = []

#         self.blueCounter1 = 4
#         self.blueDecrease1 = 1
        
#         self.redCounter1 = 4
#         self.redDecrease1 = 1
        
#         self.yellowCounter1 = 4
#         self.yellowDecrease1 = 1

#         # self.bind("<Configure>", self.on_resize)

#     # def on_resize(self, event):
#     #         # self.canvas_width = event.width
#     #         # self.canvas_height = event.height
#     #         # self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
#     #         self.update_dot_position

#     # def update_dot_position(self, event):
#     #     canvas_width = event.width
#     #     canvas_height = event.height

#     #     center_x = canvas_width // 2
#     #     center_y = canvas_height // 2

#     #     self.canvas.coords(self.dot, center_x - 10, center_y - 10, 
#     #                         center_x + 10, center_y + 10)
    
#     def create_buttons(self):
#         self.btnB = Button(self, width='14', height='6', bg='blue', command=self.move_blue)
#         self.btnR = Button(self, width='14', height='6', bg='red', command=self.move_red)
#         self.btnG = Button(self, width='14', height='6', bg='green', command=self.move_green)
#         self.btnY = Button(self, width='14', height='6', bg='yellow', command=self.move_yellow)

#         self.btnB.place(x='75', y='30')
#         self.btnR.place(x='200', y='30')
#         self.btnG.place(x='325', y='30')
#         self.btnY.place(x='450', y='30')

#     def create_menu(self):
#         menubar = Menu(self)
#         self.config(menu=menubar)

#         game_menu = Menu(menubar, tearoff=0)
#         game_menu.add_command(label='A', command=self.modeA)
#         game_menu.add_command(label='B', command=self.modeB)
#         game_menu.add_command(label='C', command=self.modeC)
#         game_menu.add_command(label='1', command=self.mode1)

#         menubar.add_cascade(label="Game Modes", menu=game_menu)

#     # Mode A: simplest version, blue button moves dot right
#     def modeA(self):
#         gameA = ModeA()
#         gameA.mainloop()
#         # self.game_mode = "A"
#         # self.congrats.place_forget()

#     # Mode B: a specific sequence of 4 button presses moves dot right
#     def modeB(self):
#         self.game_mode = "B"
#         self.congrats.place_forget()

#     # Mode C: double-click green for 1st half, red-yellow for 2nd half
#     def modeC(self):
#         self.game_mode = "C"
#         self.congrats.place_forget()

#     def mode1(self):
#         self.game_mode = "1"
#         self.congrats.place_forget()

#     def check_completion(self):
#         if self.canvas.coords(self.dot)[2] >= 1225:
#             self.game_mode = None
#             self.congrats.place(x=50, y=675)

#             x1, y1, x2, y2 = self.canvas.coords(self.dot)
#             dx = self.init_x1 - x1
#             dy = self.init_y1 - y1
#             self.canvas.move(self.dot, dx, dy)

#     def move_left(self):
#         if self.canvas.coords(self.dot)[0] > 0:
#             self.canvas.move(self.dot, -20, 0)

#     def move_right(self):
#         if self.canvas.coords(self.dot)[2] < 1250:
#             self.canvas.move(self.dot, 20, 0)
#             self.check_completion()

#     def move_up(self):
#         if self.canvas.coords(self.dot)[1] > 0:
#             self.canvas.move(self.dot, 0, -20)

#     def move_down(self):
#         if self.canvas.coords(self.dot)[3] < 500:
#             self.canvas.move(self.dot, 0, 20)

#     # blue button
#     def move_blue(self):
        
#         if self.game_mode == "A":
#             self.move_right()

#         elif self.game_mode == "B":
#             self.input_seqB.append('b')
#             self.move_up()
#             if self.input_seqB[-4:] == self.move_B:
#                 for num in range(4):
#                     self.move_right()

#         elif self.game_mode == "C":
#             self.input_seqC.append('b')

#         elif self.game_mode == "1":
#             randVal = random.randrange(1, self.blueCounter1)
#             if randVal == 1 and self.blueCounter1 < 10:
#                 self.move_right()
#             self.blueDecrease1 += 1
#             if self.blueDecrease1 % 4 == 0:
#                 self.blueCounter1 += 1

#     # red button
#     def move_red(self):

#         if self.game_mode == "A":
#             self.move_left()

#         elif self.game_mode == "B":
#             self.input_seqB.append('r')
#             self.move_down()

#         elif self.game_mode == "C":
#             self.input_seqC.append('r')

#         elif self.game_mode == "1":
#             randVal = random.randrange(1, self.redCounter1)
#             if randVal == 1 and self.redCounter1 < 10:
#                 self.move_right()
#             self.redDecrease1 += 1
#             if self.redDecrease1 % 4 == 0:
#                 self.redCounter1 += 1

#     # green button
#     def move_green(self):
#         if self.game_mode == "A":
#             self.move_up()

#         elif self.game_mode == "B":
#             self.input_seqB.append('g')
#             self.move_down()

#         elif self.game_mode == "C":
#             self.input_seqC.append('g')
#             if self.input_seqC[-2:] == self.move_C1 and self.canvas.coords(self.dot)[0] <= 575:
#                 self.move_right()
#                 self.move_right()
#                 self.input_seqC = []

#         elif self.game_mode == "1":
#             randVal = random.randrange(1, 3)
#             if randVal == 1:
#                 self.move_right()

#     # yellow button
#     def move_yellow(self):

#         if self.game_mode == "A":
#             self.move_down()

#         elif self.game_mode == "B":
#             self.input_seqB.append('y')
#             self.move_up()

#         elif self.game_mode == "C":
#             self.input_seqC.append('y')
#             if self.input_seqC[-2:] == self.move_C2 and self.canvas.coords(self.dot)[0] > 575:
#                 self.move_right()
#                 self.move_right()

#         elif self.game_mode == "1":
#             randVal = random.randrange(1, self.yellowCounter1)
#             if randVal == 1 and self.yellowCounter1 < 10:
#                 self.move_right()
#             self.yellowDecrease1 += 1
#             if self.yellowDecrease1 % 4 == 0:
#                 self.yellowCounter1 += 1

# if __name__ == "__main__":
#     game = Game()
#     game.mainloop()


"""fakeFreq.py"""
# # Generate a sample frequency profile to inform the real-time generativity grapher

# from tkinter import *

# import matplotlib.pyplot as plt

# from random import *

# # fRoot = Tk()

# # fRoot.title("Frequency Profile")

# # fRoot.geometry('700x400')

# def genProf(b10, b20, b30, b40, epsilon, alpha, dataPoints):
    
#     plt.ion()
    
#     # store initial behavioral probabilities
#     bvals = [[-2], [b10], [b20], [b30], [b40]]

#     # recursively calculate subsequent probabilty data points for each behavior
#     for num in range(dataPoints):

#         # lambda matrix
#         lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, -.2, 0, 0, 0], [0, 0, -.2, 0, 0], [0, 0, 0, -.1, 0]]

#         # extinction matrix (quantity of decrease by extinction for each behavior)
#         em = [0]

#         # reinforcement matrix (quantity of increase by reinforcement for each behavior)
#         am = [0]

#         # interaction matrix (the interaction effects between each pair of behaviors, before summation)
#         # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
#         im = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

#         # populate matrices with values for this cycle
#         for y in range(1, 5):
#             em.append(-bvals[y][-1] * epsilon)
#             am.append((1 - bvals[y][-1]) * alpha)
#             for z in range(1, 5):
#                 if (y != z and len(bvals[z]) >= 2 and lm[y][z] >= -1 and lm[y][z] <= 1):
#                     if (lm[y][z] < 0 and bvals[z][-1] - bvals[z][-2] < 0):
#                         im[y][z] = (1 - bvals[y][-1]) * -lm[y][z] * bvals[z][-1]
#                     if (lm[y][z] > 0 and bvals[z][-1] - bvals[z][-2] > 0):
#                         im[y][z] = (1 - bvals[y][-1]) * lm[y][z] * bvals[z][-1]
#                 # print(im[y][z], end=" ")
#             # print()
            
#         for y in range(1, 5):
#             epEffect = em[y]
#             alphEffect = am[y]
#             intEffect = 0
#             for z in range(1, 5):
#                 intEffect += im[y][z]
#             cur = bvals[y][-1]
#             # add randomness
#             wiggle = 0
#             if cur > .01:
#                 wiggle = .005 * randrange(-1, 1)
#             change = epEffect + alphEffect + intEffect + wiggle
#             bNext = cur + change
#             bvals[y].append(bNext)
        
#     return bvals

# def makePlot():
#     fvals = genProf(.15, .01, .01, .01, .06, 0, 100)
#     plt.plot(range(len(fvals[1])), fvals[1], 'b', linestyle='dashed', label="Frequency 1")
#     plt.plot(range(len(fvals[2])), fvals[2], 'r', linestyle='dashed', label="Frequency 2")
#     plt.plot(range(len(fvals[3])), fvals[3], 'g', linestyle='dashed', label="Frequency 3")
#     plt.plot(range(len(fvals[4])), fvals[4], 'y', linestyle='dashed', label="Frequency 4")
#     plt.xlabel('Time')
#     plt.ylabel('Probability of Behavior')
#     plt.ylim(0, 1)
#     plt.legend()

