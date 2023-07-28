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
                # enforces symmetry
                # elif row >= column:
                #     self.entries[counter] = Entry(self, width=5, state=DISABLED)
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

    # lambda matrix
    lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    # enforces symmetry
    # if prog.entries[7].get() != '':
    #     lm[1][2] = float(prog.entries[7].get())
    #     lm[2][1] = float(prog.entries[7].get())

    # if prog.entries[8].get() != '':
    #     lm[1][3] = float(prog.entries[8].get())
    #     lm[3][1] = float(prog.entries[8].get())

    # if prog.entries[9].get() != '':
    #     lm[1][4] = float(prog.entries[9].get())
    #     lm[4][1] = float(prog.entries[9].get())

    # if prog.entries[13].get() != '':
    #     lm[2][3] = float(prog.entries[13].get())
    #     lm[3][2] = float(prog.entries[13].get())

    # if prog.entries[14].get() != '':
    #     lm[2][4] = float(prog.entries[14].get())
    #     lm[4][2] = float(prog.entries[14].get())

    # if prog.entries[19].get() != '':
    #     lm[3][4] = float(prog.entries[19].get())
    #     lm[4][3] = float(prog.entries[19].get())

    # allows for asymmetry
    if prog.entries[7].get() != '':
        lm[1][2] = float(prog.entries[7].get())
    
    if prog.entries[11].get() != '':
        lm[2][1] = float(prog.entries[11].get())

    if prog.entries[8].get() != '':
        lm[1][3] = float(prog.entries[8].get())

    if prog.entries[16].get() != '':
        lm[3][1] = float(prog.entries[16].get())

    if prog.entries[9].get() != '':
        lm[1][4] = float(prog.entries[9].get())

    if prog.entries[21].get() != '':
        lm[4][1] = float(prog.entries[21].get())

    if prog.entries[13].get() != '':
        lm[2][3] = float(prog.entries[13].get())

    if prog.entries[17].get() != '':
        lm[3][2] = float(prog.entries[17].get())

    if prog.entries[14].get() != '':
        lm[2][4] = float(prog.entries[14].get())
    
    if prog.entries[22].get() != '':
        lm[4][2] = float(prog.entries[22].get())

    if prog.entries[19].get() != '':
        lm[3][4] = float(prog.entries[19].get())

    if prog.entries[23].get() != '':
        lm[4][3] = float(prog.entries[23].get())

    for row in range(5):
        for column in range(5):
            if lm[row][column] < -1 or lm[row][column] > 1:
                errMessage = Label(root, text = "lamda values should be between -1 and 1.", fg = "red")
                errMessage.grid(column = 1, row = 10)

    # generate 2D array storing probability data points over time for all behaviors
    def generate(b10, b20, b30, b40, epsilon, alpha, dataPoints):

        # store initial behavioral probabilities
        bvals = [[-2], [b10], [b20], [b30], [b40]]

        # recursively calculate subsequent probabilty data points for each behavior
        for num in range(dataPoints):

            # extinction matrix (quantity of decrease by extinction for each behavior)
            em = [0]

            # reinforcement matrix (quantity of increase by reinforcement for each behavior)
            am = [0]

            # interaction matrix (the interaction effects between each pair of behaviors, before summation)
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

    b10 = float(behaviors[0][1].get())
    b20 = float(behaviors[1][1].get())
    b30 = float(behaviors[2][1].get())
    b40 = float(behaviors[3][1].get())

    points = int(dataNtr.get())
    ep = float(epNtr.get())
    alph = float(alphNtr.get())

    b_values = generate(b10, b20, b30, b40, ep, alph, points)
    plt.plot(range(len(b_values[1])), b_values[1], 'b', linestyle='solid', label="Behavior 1")
    plt.plot(range(len(b_values[2])), b_values[2], 'r', linestyle='solid', label="Behavior 2")
    plt.plot(range(len(b_values[3])), b_values[3], 'g', linestyle='solid', label="Behavior 3")
    plt.plot(range(len(b_values[4])), b_values[4], 'y', linestyle='solid', label="Behavior 4")
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
