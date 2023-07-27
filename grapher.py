# primary graphics library
from tkinter import *

# data visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# create root window
root = Tk()

# root window title and dimension
root.title("Generativity Grapher 2.0")

# set geometry (widthxheight)
root.geometry('700x400')

# help button on menu
def helpClicked():
    lbl.configure(text = "epsilon is the extinction rate," \
                         " change this value and see how the graph changes")
    
# def fourClicked():
#     prob = Label(lvl2, text = "Enter Initial Probabilities")
#     prob.grid(column = 0, row = 0)
#     behav1 = Label(lvl2, text = "Behavior 1: ")
#     behav1.grid(column = 0, row = 1)
#     behav1Ntr = Entry(lvl2, width = 10)
#     behav1Ntr.grid(column = 1, row = 1)
#     lbl.configure(text = prob + behav1 + behav1Ntr)

# adding menu bar in root window
# new item in menu bar labelled as "New"
# adding more items in menu bar
menu = Menu(root)
lvl1 = Menu(menu)
lvl2 = Menu(lvl1)
menu.add_cascade(label='Menu', menu=lvl1)
lvl1.add_command(label='Help', command=helpClicked)
lvl1.add_cascade(label="# of Behaviors", menu=lvl2)
lvl2.add_command(label='4')
lvl2.add_command(label='5')
root.config(menu=menu)

# add label to root window
lbl = Label(root, text = "Delta")
lbl.grid(column = 2, row = 0)

# parameter input

# epsilon
epLbl = Label(root, text = "Epsilon: ")
epLbl.grid(column = 0, row = 1)
epNtr = Entry(root, width=10)
epNtr.grid(column=1, row=1)
deltENtr = Entry(root, width=10)
deltENtr.grid(column = 2, row = 1)

# alpha
alphLbl = Label(root, text = "Alpha: ")
alphLbl.grid(column = 0, row = 2)
alphNtr = Entry(root, width=10)
alphNtr.grid(column=1, row=2)
deltANtr = Entry(root, width=10)
deltANtr.grid(column = 2, row = 2)

# reinforcer
rfLbl = Label(root, text = "Reinforcer: ")
rfLbl.grid(column = 0, row = 3)
rfNtr = Entry(root, width=10)
rfNtr.grid(column=1, row=3)
deltRNtr = Entry(root, width=10)
deltRNtr.grid(column = 2, row = 3)

# behaviors
probLbl = Label(root, text ="Initial Probabilities")
probLbl.grid(column=0, row = 4)

behaviors = [[], [], [], []]
for num in range(4):
    behaviors[num].append(Label(root, text = "Behavior " + str(num + 1) + ": "))
    behaviors[num][0].grid(column = 0, row = num + 5)

    behaviors[num].append(Entry(root, width = 10))
    behaviors[num][1].grid(column = 1, row = num + 5)

# b1Lbl = Label(root, text = "Behavior 1: ")
# b1Lbl.grid(column = 0, row = 5)
# b1Ntr = Entry(root, width = 10)
# b1Ntr.grid(column = 1, row = 5)

# b2Lbl = Label(root, text = "Behavior 2: ")
# b2Lbl.grid(column = 0, row = 6)
# b2Ntr = Entry(root, width = 10)
# b2Ntr.grid(column = 1, row = 6)

# b3Lbl = Label(root, text = "Behavior 3: ")
# b3Lbl.grid(column = 0, row = 7)
# b3Ntr = Entry(root, width = 10)
# b3Ntr.grid(column = 1, row = 7)

# b4Lbl = Label(root, text = "Behavior 4: ")
# b4Lbl.grid(column = 0, row = 8)
# b4Ntr = Entry(root, width = 10)
# b4Ntr.grid(column = 1, row = 8)

# lambda matrix title
lambdaLbl = Label(root, text = "Lambda Matrix")
lambdaLbl.grid(column = 0, row = 9)

# lambda matrix
class app(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        self.tableheight = 5
        self.tablewidth = 5
        counter = 0
        for row in range(self.tableheight):
            for column in range(self.tablewidth):
                if row == 0 and column == 0:
                    self.entries[counter] = Label(self, text = "")
                    self.entries[counter].grid(row=row, column=column) 
                    counter += 1
                    continue
                elif row == 0:
                    self.entries[counter] = Label(self, text = str(column))
                elif column == 0:
                    self.entries[counter] = Label(self, text = str(row))
                elif row >= column:
                    self.entries[counter] = Entry(self, width=5, state=DISABLED)
                else:
                    self.entries[counter] = Entry(self, width=5)
                self.entries[counter].grid(row=row, column=column) 
                counter += 1

# display lambda matrix
prog = app()

# data points
dataLbl = Label(root, text = "Data Points: ")
dataLbl.grid(column = 4, row = 1)
dataNtr = Entry(root, width=10)
dataNtr.grid(column=5, row=1)

# iterations
iterLbl = Label(root, text = "Iterations: ")
iterLbl.grid(column = 4, row = 2)
iterNtr = Entry(root, width=10)
iterNtr.grid(column=5, row=2)

# function to generate and display graph when submit is clicked
def genGraph():
    
    points = 50
    ep = .06
    alph = .0

    # points = int(dataNtr.get())
    # ep = float(epNtr.get())
    # alph = float(alphNtr.get())

    # lambda matrix
    lm = [[-2, -2, -2, -2, -2], [-2, -2], [-2, -2, -2], [-2, -2, -2, -2], [-2, -2, -2, -2, -2]]

    if prog.entries[7].get() == '':
        lm[1].append(0)
    else:
        lm[1].append(float(prog.entries[7].get()))

    if prog.entries[8].get() == '':
        lm[1].append(0)
    else:
        lm[1].append(float(prog.entries[8].get()))

    if prog.entries[9].get() == '':
        lm[1].append(0)
    else:
        lm[1].append(float(prog.entries[9].get()))

    if prog.entries[13].get() == '':
        lm[2].append(0)
    else:
        lm[2].append(float(prog.entries[13].get()))

    if prog.entries[14].get() == '':
        lm[2].append(0)
    else:
        lm[2].append(float(prog.entries[14].get()))

    if prog.entries[19].get() == '':
        lm[3].append(0)
    else:
        lm[3].append(float(prog.entries[19].get()))

    # for r in range(5):
    #     for c in range(5):
    #         lamVal = Label(root, text = str(lm[r][c]))
    #         lamVal.grid(column = c + 6, row = r)

    # generate 2D array storing probability data points over time for all behaviors
    def ext_rein(b10, b20, b30, b40, epsilon, alpha, dataPoints):

        # store initial behavioral probabilities
        bvals = [[b10], [b20], [b30], [b40]]

        # recursively calculate subsequent probabilty data points for each behavior
        for num in range(dataPoints):
            
            b1n = bvals[0][-1]
            b2n = bvals[1][-1]
            b3n = bvals[2][-1]
            b4n = bvals[3][-1]

            for y in range(4):
                ext = bvals[y][-1] * epsilon
                rein = (1 - bvals[y][-1]) * alpha
                for z in range(4):
                    if (lm[y+1][z+1] == -2 or lm[y+1][z+1] >= 0 or bvals[z][-1] - bvals[z][-2] >= 0):
                        

            # behavior 1
            b1ext = b1n * epsilon
            b1rein = (1 - b1n) * alpha
            b1res = ((1 - b1n) * -lm[1][2] * b2n) + ((1 - b1n) * -lm[1][3] * b3n) + ((1 - b1n) * -lm[1][4] * b4n)
            # b1chain = ((1 - b1n) * l12 * b2n) + ((1 - b1n) * l13 * b3n) + ((1 - b1n) * l14 * b4n)
            next_b1 = b1n - b1ext + b1rein + b1res
            b_values[0].append(next_b1)

            # behavior 2
            b2ext = b2n * epsilon
            b2rein = (1 - b2n) * alpha
            b2res = ((1 - b2n) * -lm[1][2] * b1n) + ((1 - b2n) * -lm[2][3] * b3n) + ((1 - b2n) * -lm[2][4] * b4n)
            next_b2 = b2n - b2ext + b2rein + b2res
            b_values[1].append(next_b2)

            # behavior 3
            b3ext = b3n * epsilon
            b3rein = (1 - b3n) * alpha
            b3res = ((1 - b3n) * -lm[2][3] * b2n) + ((1 - b3n) * -lm[1][3] * b1n) + ((1 - b3n) * -lm[3][4] * b4n)
            next_b3 = b3n - b3ext + b3rein + b3res
            b_values[2].append(next_b3)

            # behavior 4
            b4ext = b4n * epsilon
            b4rein = (1 - b4n) * alpha
            b4res = ((1 - b4n) * -lm[1][4] * b1n) + ((1 - b4n) * -lm[2][4] * b2n) + ((1 - b4n) * -lm[3][4] * b3n)
            next_b4 = b4n - b4ext + b4rein + b4res
            b_values[3].append(next_b4)

        return b_values

    b10 = .4
    b20 = .01
    b30 = .1
    b40 = .01

    b_values = ext_rein(b10, b20, b30, b40, ep, alph, points)
    plt.plot(range(len(b_values[0])), b_values[0], 'b', linestyle='solid', label="Behavior 1")
    plt.plot(range(len(b_values[1])), b_values[1], 'r', linestyle='solid', label="Behavior 2")
    plt.plot(range(len(b_values[2])), b_values[2], 'g', linestyle='solid', label="Behavior 3")
    plt.plot(range(len(b_values[3])), b_values[3], 'y', linestyle='solid', label="Behavior 4")
    plt.xlabel('Time')
    plt.ylabel('Probability of Behavior')
    plt.legend()
    plt.show()

# submit button
submit = Button(root, text = "Generate Graph", fg = "red", command=genGraph)

# set Button grid
submit.grid(column=10, row=20)

# execute Tkinter
root.mainloop()
