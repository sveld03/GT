# primary graphics library
from tkinter import *

from tkinter import ttk

# # data visualization

# import matplotlib as mpl
import matplotlib.pyplot as plt

# # Arrays
# import numpy as np

# lambda matrix
class matrix(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        
        # Create 5x5 Frame
        self.entries = {}
        self.tableheight = 5
        self.tablewidth = 5
        counter = 0

        for row in range(self.tableheight):
            for column in range(self.tablewidth):

                # Leave top left corner blank
                if row == 0 and column == 0:
                    self.entries[counter] = Label(self, text = "")
                    self.entries[counter].grid(row=row, column=column) 
                    counter += 1
                    continue

                # In first row and first column, label behavior numbers
                elif row == 0:
                    self.entries[counter] = Label(self, text = str(column))
                elif column == 0:
                    self.entries[counter] = Label(self, text = str(row))

                # Remaining 4x4 grid is for lambda entry
                else:
                    self.entries[counter] = Entry(self, width=5)
                    self.entries[counter].insert(0, '0')
                self.entries[counter].grid(row=row, column=column) 
                counter += 1

class Params(Tk):
    def __init__(self):
        super().__init__()

        # self window title and dimension
        self.title("Generativity Grapher 2.0")

        # set geometry (widthxheight)
        self.geometry('700x400')

        # add label to self window
        lbl = Label(self, text = "Delta")
        lbl.grid(column = 2, row = 0)


        # parameter input

        # epsilon
        epLbl = Label(self, text = "Epsilon: ")
        epLbl.grid(column = 0, row = 1)
        self.epNtr = Entry(self, width=10)
        self.epNtr.grid(column=1, row=1)
        self.epNtr.insert(0, '.01')

        self.deltENtr = Entry(self, width=10)
        self.deltENtr.grid(column = 2, row = 1)
        self.deltENtr.insert(0, '.05')

        # alpha
        alphLbl = Label(self, text = "Alpha: ")
        alphLbl.grid(column = 0, row = 2)
        self.alphNtr = Entry(self, width=10)
        self.alphNtr.grid(column=1, row=2)
        self.alphNtr.insert(0, '.01')

        self.deltANtr = Entry(self, width=10)
        self.deltANtr.grid(column = 2, row = 2)
        self.deltANtr.insert(0, '.05')

        # reinforcer
        rfLbl = Label(self, text = "Reinforcer: ")
        rfLbl.grid(column = 0, row = 3)
        self.rfNtr = Entry(self, width=10)
        self.rfNtr.grid(column=1, row=3)
        self.rfNtr.insert(0, '0')

        self.deltRNtr = Entry(self, width=10)
        self.deltRNtr.grid(column = 2, row = 3)
        self.deltRNtr.insert(0, '.05')

        # self.behaviors
        probLbl = Label(self, text ="Initial Probabilities")
        probLbl.grid(column=0, row = 4)

        # Display labels and entry fields for initial behavioral probabilities
        self.behaviors = [[], [], [], []]
        for num in range(4):
            self.behaviors[num].append(Label(self, text = "Behavior " + str(num + 1) + ": "))
            self.behaviors[num][0].grid(column = 0, row = num + 5)

            self.behaviors[num].append(Entry(self, width = 10))
            self.behaviors[num][1].grid(column = 1, row = num + 5)
            self.behaviors[num][1].insert(0, '.01')

        # lambda matrix title
        lambdaLbl = Label(self, text = "Lambda Matrix", pady=15)
        lambdaLbl.grid(column = 1, row = 9)

        # independent and dependent labels
        indep = Label(self, text="Independent")
        indep.grid(column = 1, row = 10)

        dep = Label(self, text = "Dependent")
        dep.grid(column = 0, row = 11)

        # display lambda matrix
        self.data = matrix()
        self.data.grid(column = 1, row = 11)

        self.lm = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # User name
        self.nameLbl = Label(self, text="Enter your name here: ")
        self.nameLbl.grid(column=4, row=1)
        self.nameNtr = Entry(self, width=10)
        self.nameNtr.grid(column=5, row=1)

        # Trial number
        self.trialLbl = Label(self, text = "Trial: ")
        self.trialLbl.grid(column=4, row=2)
        self.trialNtr = Entry(self, width=10)
        self.trialNtr.grid(column=5, row=2)
        self.trialNtr.insert(0, '1')

        # data points
        dataLbl = Label(self, text = "Data Points: ")
        dataLbl.grid(column = 4, row = 4)
        self.dataNtr = Entry(self, width=10)
        self.dataNtr.grid(column=5, row=4)
        self.dataNtr.insert(0, '99999')

        # iterations
        iterLbl = Label(self, text = "Iterations: ")
        iterLbl.grid(column = 4, row = 5)
        self.iterNtr = Entry(self, width=10)
        self.iterNtr.grid(column=5, row=5)
        self.iterNtr.insert(0, '1')

        game_settings = Label(self, text="Game Settings:")
        game_settings.grid(column=4, row=7)

        self.present_modes()

        windowLbl = Label(self, text = "Frequency profile window length (seconds):")
        windowLbl.grid(column = 4, row = 11)
        self.windowNtr = Entry(self, width=10)
        self.windowNtr.grid(column = 5, row = 11)
        self.windowNtr.insert(0, '3')

        # submit button
        submit = Button(self, text = "Generate Graph", fg = "red", command=self.store_params)

        # set Button grid
        submit.grid(column=5, row=13)

    # Game mode menu
    def present_modes(self):
        self.mode = StringVar(self, "none")
        
        self.btnA = ttk.Radiobutton(self, text="Game Mode A", value="A", variable=self.mode)
        self.btnA.grid(column=4, row=8)
        self.btnB = ttk.Radiobutton(self, text="Game Mode B", value="B", variable=self.mode)
        self.btnB.grid(column=5, row=8)
        self.btnC = ttk.Radiobutton(self, text="Game Mode C", value="C", variable=self.mode)
        self.btnC.grid(column=4, row=9)
        self.btn1 = ttk.Radiobutton(self, text="Game Mode 1", value="1", variable=self.mode)
        self.btn1.grid(column=5, row=9)
        self.btn2 = ttk.Radiobutton(self, text="Game Mode 2", value="2", variable=self.mode)
        self.btn2.grid(column=4, row=10)

    def store_params(self):
        # Fill in lambda matrix list with user-inputted values
        if self.data.entries[7].get() != '':
            self.lm[0][1] = float(self.data.entries[7].get())
        
        if self.data.entries[11].get() != '':
            self.lm[1][0] = float(self.data.entries[11].get())

        if self.data.entries[8].get() != '':
            self.lm[0][2] = float(self.data.entries[8].get())

        if self.data.entries[16].get() != '':
            self.lm[2][0] = float(self.data.entries[16].get())

        if self.data.entries[9].get() != '':
            self.lm[0][3] = float(self.data.entries[9].get())

        if self.data.entries[21].get() != '':
            self.lm[3][0] = float(self.data.entries[21].get())

        if self.data.entries[13].get() != '':
            self.lm[1][2] = float(self.data.entries[13].get())

        if self.data.entries[17].get() != '':
            self.lm[2][1] = float(self.data.entries[17].get())

        if self.data.entries[14].get() != '':
            self.lm[1][3] = float(self.data.entries[14].get())
        
        if self.data.entries[22].get() != '':
            self.lm[3][1] = float(self.data.entries[22].get())

        if self.data.entries[19].get() != '':
            self.lm[2][3] = float(self.data.entries[19].get())

        if self.data.entries[23].get() != '':
            self.lm[3][2] = float(self.data.entries[23].get())

        # If any lambda values have abs value greater than 1, throw error
        for row in range(4):
            for column in range(4):
                if self.lm[row][column] < -1 or self.lm[row][column] > 1:
                    errMessage = Label(self, text = "lamda values should be between -1 and 1.", fg = "red")
                    errMessage.grid(column = 1, row = 10)

        # Initialize behavioral probabilities with user input
        self.b10 = float(self.behaviors[0][1].get())
        self.b20 = float(self.behaviors[1][1].get())
        self.b30 = float(self.behaviors[2][1].get())
        self.b40 = float(self.behaviors[3][1].get())

        # Initialize values for number of data points, epsilon, and alpha with user input
        self.points = int(self.dataNtr.get())
        self.ep = float(self.epNtr.get())
        self.alph = float(self.alphNtr.get())

        self.event_generate("<<startGame>>")
        self.event_generate("<<startGraph>>")
    
    def get_window(self):
        return int(self.windowNtr.get())
