# real-time generativity grapher: update parameters at frequent intervals using feedback from frequency profile, predict a moving window


# outline

    # user entry: 
        # initial parameter values: epsilon, alpha, lambda matrix, behavioral probabilities
        # information about changes during trial:
            # which parameter values will change? at what time? to what value / by what percent?
    # test submit
        # "time" parameter
        # the 1st of 2 submit buttons, this will generate a static graph showing what we'd get with no feedback from freq prof
        # user can x out of this graph to return back to the input screen, where they can change parameters and test again
    # actual submit
        # starts real-time generativity grapher. 
        # At this time, researcher should tell subject to begin the game
        # the data from the game will also be fed to this program
    # create bvals list for 1st second
        # display on screen as graph
    # create frequency profile list
        # starts empty
        # as data comes in, entries are added to the list and immediately plotted on graph (same graph as prob prof, later may switch to below)
    # create new bvals list for 0.1-1.1s
        # we use the data in the frequency profile list to determine what changes should be made to parameters, then generate bvals list with these parameters
    # repeat for 0.2-1.2s, 0.3-1.3s, etc.
    # 

import threading
import time

from fakeFreq import *

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

# menu: help + # of behaviors
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
lambdaLbl = Label(root, text = "Lambda Matrix", pady=15)
lambdaLbl.grid(column = 1, row = 9)

# independent and dependent labels
indep = Label(root, text="Independent")
indep.grid(column = 1, row = 10)

dep = Label(root, text = "Dependent")
dep.grid(column = 0, row = 11)

# lambda matrix
class matrix(Frame):
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
data = matrix()
data.grid(column = 1, row = 11)

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
def genGraphs():

    plt.ion()

    # lambda matrix
    lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    # allows for asymmetry
    if data.entries[7].get() != '':
        lm[1][2] = float(data.entries[7].get())
    
    if data.entries[11].get() != '':
        lm[2][1] = float(data.entries[11].get())

    if data.entries[8].get() != '':
        lm[1][3] = float(data.entries[8].get())

    if data.entries[16].get() != '':
        lm[3][1] = float(data.entries[16].get())

    if data.entries[9].get() != '':
        lm[1][4] = float(data.entries[9].get())

    if data.entries[21].get() != '':
        lm[4][1] = float(data.entries[21].get())

    if data.entries[13].get() != '':
        lm[2][3] = float(data.entries[13].get())

    if data.entries[17].get() != '':
        lm[3][2] = float(data.entries[17].get())

    if data.entries[14].get() != '':
        lm[2][4] = float(data.entries[14].get())
    
    if data.entries[22].get() != '':
        lm[4][2] = float(data.entries[22].get())

    if data.entries[19].get() != '':
        lm[3][4] = float(data.entries[19].get())

    if data.entries[23].get() != '':
        lm[4][3] = float(data.entries[23].get())

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

    # b10 = float(behaviors[0][1].get())
    # b20 = float(behaviors[1][1].get())
    # b30 = float(behaviors[2][1].get())
    # b40 = float(behaviors[3][1].get())

    # points = int(dataNtr.get())
    # ep = float(epNtr.get())
    # alph = float(alphNtr.get())

    b10 = .15
    b20 = .01
    b30 = .01
    b40 = .01

    points = 100
    ep = .06
    alph = 0

    b_values = generate(b10, b20, b30, b40, ep, alph, points)
    plt.plot(range(len(b_values[1])), b_values[1], 'b', linestyle='solid', label="Probability 1")
    plt.plot(range(len(b_values[2])), b_values[2], 'r', linestyle='solid', label="Probability 2")
    plt.plot(range(len(b_values[3])), b_values[3], 'g', linestyle='solid', label="Probability 3")
    plt.plot(range(len(b_values[4])), b_values[4], 'y', linestyle='solid', label="Probability 4")
    plt.xlabel('Time')
    plt.ylabel('Probability of Behavior')
    plt.ylim(0, 1)
    plt.legend()

    

    makePlot()

    plt.show()

# run experiment
def runExp():
    # lambda matrix
    lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    # allows for asymmetry
    if data.entries[7].get() != '':
        lm[1][2] = float(data.entries[7].get())
    
    if data.entries[11].get() != '':
        lm[2][1] = float(data.entries[11].get())

    if data.entries[8].get() != '':
        lm[1][3] = float(data.entries[8].get())

    if data.entries[16].get() != '':
        lm[3][1] = float(data.entries[16].get())

    if data.entries[9].get() != '':
        lm[1][4] = float(data.entries[9].get())

    if data.entries[21].get() != '':
        lm[4][1] = float(data.entries[21].get())

    if data.entries[13].get() != '':
        lm[2][3] = float(data.entries[13].get())

    if data.entries[17].get() != '':
        lm[3][2] = float(data.entries[17].get())

    if data.entries[14].get() != '':
        lm[2][4] = float(data.entries[14].get())
    
    if data.entries[22].get() != '':
        lm[4][2] = float(data.entries[22].get())

    if data.entries[19].get() != '':
        lm[3][4] = float(data.entries[19].get())

    if data.entries[23].get() != '':
        lm[4][3] = float(data.entries[23].get())

    for row in range(5):
        for column in range(5):
            if lm[row][column] < -1 or lm[row][column] > 1:
                errMessage = Label(root, text = "lambda values should be between -1 and 1.", fg = "red")
                errMessage.grid(column = 1, row = 10)

    # generate 2D array storing probability data points over time for all behaviors
    def generate(b10, b20, b30, b40, epsilon, alpha):

        # store initial behavioral probabilities
        gvals = [[-2], [b10], [b20], [b30], [b40]]

        fvals = []

        # recursively calculate subsequent probabilty data points for each behavior
        for num in range(10):

            # extinction matrix (quantity of decrease by extinction for each behavior)
            em = [0]

            # reinforcement matrix (quantity of increase by reinforcement for each behavior)
            am = [0]

            # interaction matrix (the interaction effects between each pair of behaviors, before summation)
            # encapsulates equations 3 (resurgence) and 4 (automatic chaining)
            im = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

            # populate matrices with values for this cycle
            for y in range(1, 5):
                em.append(-gvals[y][-1] * epsilon)
                am.append((1 - gvals[y][-1]) * alpha)
                for z in range(1, 5):
                    if (y != z and len(gvals[z]) >= 2 and lm[y][z] >= -1 and lm[y][z] <= 1):
                        if (lm[y][z] < 0 and gvals[z][-1] - gvals[z][-2] < 0):
                            im[y][z] = (1 - gvals[y][-1]) * -lm[y][z] * gvals[z][-1]
                        if (lm[y][z] > 0 and gvals[z][-1] - gvals[z][-2] > 0):
                            im[y][z] = (1 - gvals[y][-1]) * lm[y][z] * gvals[z][-1]
                    # print(im[y][z], end=" ")
                # print()
            
            for y in range(1, 5):
                epEffect = em[y]
                alphEffect = am[y]
                intEffect = 0
                for z in range(1, 5):
                    intEffect += im[y][z]
                cur = gvals[y][-1]
                change = epEffect + alphEffect + intEffect
                bNext = cur + change
                gvals[y].append(bNext)
        
        return gvals
    
    # b10 = float(behaviors[0][1].get())
    # b20 = float(behaviors[1][1].get())
    # b30 = float(behaviors[2][1].get())
    # b40 = float(behaviors[3][1].get())

    # points = int(dataNtr.get())
    # ep = float(epNtr.get())
    # alph = float(alphNtr.get())

    b10 = .15
    b20 = .01
    b30 = .01
    b40 = .01

    ep = .06
    alph = 0

    b_values = generate(b10, b20, b30, b40, ep, alph)
    plt.plot(range(len(b_values[1])), b_values[1], 'b', linestyle='solid', label="Probability 1")
    plt.plot(range(len(b_values[2])), b_values[2], 'r', linestyle='solid', label="Probability 2")
    plt.plot(range(len(b_values[3])), b_values[3], 'g', linestyle='solid', label="Probability 3")
    plt.plot(range(len(b_values[4])), b_values[4], 'y', linestyle='solid', label="Probability 4")
    plt.xlabel('Time')
    plt.ylabel('Probability of Behavior')
    plt.legend()
    plt.show()

# submit button
test = Button(root, text = "Test Model", fg = "red", command=genGraphs)

# set Button grid
test.grid(column=10, row=20)

# button to run experiment
run = Button(root, text="Run Experiment", fg="green", command=runExp)
run.grid(column = 11, row = 20)

# execute Tkinter
root.mainloop()