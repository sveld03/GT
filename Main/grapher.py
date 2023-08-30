from game import *

# primary graphics library
from tkinter import *


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
                self.entries[counter].grid(row=row, column=column) 
                counter += 1

class Grapher(Tk):
    def __init__(self):
        super().__init__()

        # self window title and dimension
        self.title("Generativity Grapher 2.0")

        # set geometry (widthxheight)
        self.geometry('700x400')

        # help button on menu
        def helpClicked():
            lbl.configure(text = "epsilon is the extinction rate," \
                                " change this value and see how the graph changes")

        # menu: help + # of self.behaviors
        menu = Menu(self)
        lvl1 = Menu(menu)
        lvl2 = Menu(lvl1)
        menu.add_cascade(label='Menu', menu=lvl1)
        lvl1.add_command(label='Help', command=helpClicked)
        lvl1.add_cascade(label="# of self.behaviors", menu=lvl2)
        lvl2.add_command(label='4')
        lvl2.add_command(label='5')
        self.config(menu=menu)

        # add label to self window
        lbl = Label(self, text = "Delta")
        lbl.grid(column = 2, row = 0)


        # parameter input

        # epsilon
        epLbl = Label(self, text = "Epsilon: ")
        epLbl.grid(column = 0, row = 1)
        self.epNtr = Entry(self, width=10)
        self.epNtr.grid(column=1, row=1)
        self.deltENtr = Entry(self, width=10)
        self.deltENtr.grid(column = 2, row = 1)

        # alpha
        alphLbl = Label(self, text = "Alpha: ")
        alphLbl.grid(column = 0, row = 2)
        self.alphNtr = Entry(self, width=10)
        self.alphNtr.grid(column=1, row=2)
        self.deltANtr = Entry(self, width=10)
        self.deltANtr.grid(column = 2, row = 2)

        # reinforcer
        rfLbl = Label(self, text = "Reinforcer: ")
        rfLbl.grid(column = 0, row = 3)
        self.rfNtr = Entry(self, width=10)
        self.rfNtr.grid(column=1, row=3)
        self.deltRNtr = Entry(self, width=10)
        self.deltRNtr.grid(column = 2, row = 3)

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

        # data points
        dataLbl = Label(self, text = "Data Points: ")
        dataLbl.grid(column = 4, row = 1)
        self.dataNtr = Entry(self, width=10)
        self.dataNtr.grid(column=5, row=1)

        # iterations
        iterLbl = Label(self, text = "Iterations: ")
        iterLbl.grid(column = 4, row = 2)
        self.iterNtr = Entry(self, width=10)
        self.iterNtr.grid(column=5, row=2)

        # submit button
        submit = Button(self, text = "Generate Graph", fg = "red", command=self.genGraph)

        # set Button grid
        submit.grid(column=10, row=20)

    # function to generate and display graph when submit is clicked
    def genGraph(self):

        # lambda matrix
        lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        # Fill in lambda matrix list with user-inputted values
        if self.data.entries[7].get() != '':
            lm[1][2] = float(self.data.entries[7].get())
        
        if self.data.entries[11].get() != '':
            lm[2][1] = float(self.data.entries[11].get())

        if self.data.entries[8].get() != '':
            lm[1][3] = float(self.data.entries[8].get())

        if self.data.entries[16].get() != '':
            lm[3][1] = float(self.data.entries[16].get())

        if self.data.entries[9].get() != '':
            lm[1][4] = float(self.data.entries[9].get())

        if self.data.entries[21].get() != '':
            lm[4][1] = float(self.data.entries[21].get())

        if self.data.entries[13].get() != '':
            lm[2][3] = float(self.data.entries[13].get())

        if self.data.entries[17].get() != '':
            lm[3][2] = float(self.data.entries[17].get())

        if self.data.entries[14].get() != '':
            lm[2][4] = float(self.data.entries[14].get())
        
        if self.data.entries[22].get() != '':
            lm[4][2] = float(self.data.entries[22].get())

        if self.data.entries[19].get() != '':
            lm[3][4] = float(self.data.entries[19].get())

        if self.data.entries[23].get() != '':
            lm[4][3] = float(self.data.entries[23].get())

        # If any lambda values have abs value greater than 1, throw error
        for row in range(5):
            for column in range(5):
                if lm[row][column] < -1 or lm[row][column] > 1:
                    errMessage = Label(self, text = "lamda values should be between -1 and 1.", fg = "red")
                    errMessage.grid(column = 1, row = 10)

        # generate 2D array storing probability data points over time for all self.behaviors
        def generate(b10, b20, b30, b40, epsilon, alpha, dataPoints):

            # store initial behavioral probabilities
            bvals = [[-2], [b10], [b20], [b30], [b40]]

            # recursively calculate subsequent probabilty data points for each behavior
            for num in range(dataPoints):

                # extinction matrix (quantity of decrease by extinction for each behavior)
                em = [0]

                # reinforcement matrix (quantity of increase by reinforcement for each behavior)
                am = [0]

                # interaction matrix (the interaction effects between each pair of self.behaviors, before summation)
                # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
                im = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

                # populate matrices with values for this cycle
                for y in range(1, 5):
                    em.append(-bvals[y][-1] * epsilon)
                    am.append((1 - bvals[y][-1]) * alpha)
                    for z in range(1, 5):
                        if (y != z and len(bvals[z]) >= 2 and lm[y][z] >= -1 and lm[y][z] <= 1):
                            if (lm[y][z] < 0 and bvals[z][-1] - bvals[z][-2] < 0):
                                im[y][z] = (1 - bvals[y][-1]) * -lm[y][z] * bvals[z][-1]
                            if (lm[y][z] > 0 and bvals[z][-1] - bvals[z][-2] > 0):
                                im[y][z] = (1 - bvals[y][-1]) * lm[y][z] * bvals[z][-1]
                        # print(im[y][z], end=" ")
                    # print()
                
                # For each behavior, calculate the probability of this behavior for this cycle and append it to bvals
                for y in range(1, 5):
                    epEffect = em[y]
                    alphEffect = am[y]
                    intEffect = 0
                    for z in range(1, 5):
                        intEffect += im[y][z]
                    cur = bvals[y][-1]
                    change = epEffect + alphEffect + intEffect
                    bNext = cur + change
                    bvals[y].append(bNext)
            
            return bvals

        # Initialize behavioral probabilities with user input
        b10 = float(self.behaviors[0][1].get())
        b20 = float(self.behaviors[1][1].get())
        b30 = float(self.behaviors[2][1].get())
        b40 = float(self.behaviors[3][1].get())

        # Initialize values for number of data points, epsilon, and alpha with user input
        points = int(self.dataNtr.get())
        ep = float(self.epNtr.get())
        alph = float(self.alphNtr.get())

        # Generate a list of behavioral probabilities over time
        b_values = generate(b10, b20, b30, b40, ep, alph, points)

        # Plot the probability profile for each behavior, overlaid on top of each other
        plt.plot(range(len(b_values[1])), b_values[1], 'b', linestyle='solid', label="Behavior 1")
        plt.plot(range(len(b_values[2])), b_values[2], 'r', linestyle='solid', label="Behavior 2")
        plt.plot(range(len(b_values[3])), b_values[3], 'g', linestyle='solid', label="Behavior 3")
        plt.plot(range(len(b_values[4])), b_values[4], 'y', linestyle='solid', label="Behavior 4")

        # Label axes
        plt.xlabel('Time')
        plt.ylabel('Probability of Behavior')

        # Tells which color corresponds to which behavior
        plt.legend()

        # Display probability profile
        plt.show()

if __name__ == "__main__":
    # execute Tkinter
    grapher = Grapher()
    grapher.mainloop()
