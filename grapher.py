from tkinter import *

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# create root window
root = Tk()

# root window title and dimension
root.title("Generativity Grapher 2.0")

# set geometry (widthxheight)
root.geometry('700x400')

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

for n in range(4):
    behavLbl = Label(root, text = "Behavior " + str(n + 1) + ": ")
    behavLbl.grid(column = 0, row = n + 5)
    behavNtr = Entry(root, width = 10)
    behavNtr.grid(column = 1, row = n + 5)

# lambda matrix
lambdaLbl = Label(root, text = "Lambda Matrix")
lambdaLbl.grid(column = 0, row = 9)

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
                else:
                    self.entries[counter] = Entry(self, width=5)
                self.entries[counter].grid(row=row, column=column) 
                counter += 1

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

# function to display graph when submit is clicked
def genGraph():
    
    points = int(dataNtr.get())
    ep = float(epNtr.get())
    alph = float(alphNtr.get())

    def ext_rein(y0, epsilon, alpha, dataPoints):
        y_values = [y0]
        for num in range(dataPoints):
            yn = y_values[-1]
            next_y = yn - (yn * epsilon) + ((1 - yn) * alpha)
            y_values.append(next_y)
        return y_values

    y0 = .15

    y_values = ext_rein(y0, ep, alph, points)
    plt.plot(range(len(y_values)), y_values, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Probability of Behavior')
    plt.show()

# submit button
submit = Button(root, text = "Generate Graph", fg = "red", command=genGraph)

# set Button grid
submit.grid(column=10, row=20)

# execute Tkinter
root.mainloop()
