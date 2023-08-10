# Generate a sample frequency profile to inform the real-time generativity grapher

from tkinter import *

import matplotlib.pyplot as plt

from random import *

# fRoot = Tk()

# fRoot.title("Frequency Profile")

# fRoot.geometry('700x400')

def genProf(b10, b20, b30, b40, epsilon, alpha, dataPoints):
    
    plt.ion()
    
    # store initial behavioral probabilities
    bvals = [[-2], [b10], [b20], [b30], [b40]]

    # recursively calculate subsequent probabilty data points for each behavior
    for num in range(dataPoints):

        # lambda matrix
        lm = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, -.2, 0, 0, 0], [0, 0, -.2, 0, 0], [0, 0, 0, -.1, 0]]

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
            # add randomness
            wiggle = 0
            if cur > .01:
                wiggle = .005 * randrange(-1, 1)
            change = epEffect + alphEffect + intEffect + wiggle
            bNext = cur + change
            bvals[y].append(bNext)
        
    return bvals

def makePlot():
    fvals = genProf(.15, .01, .01, .01, .06, 0, 100)
    plt.plot(range(len(fvals[1])), fvals[1], 'b', linestyle='dashed', label="Frequency 1")
    plt.plot(range(len(fvals[2])), fvals[2], 'r', linestyle='dashed', label="Frequency 2")
    plt.plot(range(len(fvals[3])), fvals[3], 'g', linestyle='dashed', label="Frequency 3")
    plt.plot(range(len(fvals[4])), fvals[4], 'y', linestyle='dashed', label="Frequency 4")
    plt.xlabel('Time')
    plt.ylabel('Probability of Behavior')
    plt.ylim(0, 1)
    plt.legend()
    