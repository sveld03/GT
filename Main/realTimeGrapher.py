# function to generate and display graph when submit is clicked

from params import *

class realTimeGrapher:

    def __init__(self, params):

        self.params = params

        self.params.bind("<<startGraph>>", self.genGraph)

    def generate(self, b10, b20, b30, b40, epsilon, alpha, dataPoints):

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
                    if (y != z and len(bvals[z]) >= 2 and self.params.lm[y][z] >= -1 and self.params.lm[y][z] <= 1):
                        if (self.params.lm[y][z] < 0 and bvals[z][-1] - bvals[z][-2] < 0):
                            im[y][z] = (1 - bvals[y][-1]) * -self.params.lm[y][z] * bvals[z][-1]
                        if (self.params.lm[y][z] > 0 and bvals[z][-1] - bvals[z][-2] > 0):
                            im[y][z] = (1 - bvals[y][-1]) * self.params.lm[y][z] * bvals[z][-1]
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

    def genGraph(self, event):

        # Generate a list of behavioral probabilities over time
        b_values = self.generate(self.params.b10, self.params.b20, self.params.b30, self.params.b40, self.params.ep, self.params.alph, self.params.points)

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