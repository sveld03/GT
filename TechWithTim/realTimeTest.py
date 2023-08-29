import matplotlib as mat
mat.use("Tkagg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt
import time

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

LARGE_FONT = ("Verdana", 12)
style.use('ggplot')

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

fig = plt.figure()
ax1 = fig.add_subplot(111)

def animate(i):
    dataLink = ''

    
class SeaOfBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Real Time Test")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (StartPage, BTCe_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""ALPHA Bitcoin trading application,
                                    use at your own risk. There is no promise
                                    of warranty.""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree", 
                            command=lambda:controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree", 
                            command=quit)
        button2.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back To Home", 
                            command=lambda:controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page2", 
                            command=lambda:controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back To Home", 
                            command=lambda:controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="PageOne", 
                            command=lambda:controller.show_frame(PageOne))
        button2.pack()

class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back To Home", 
                            command=lambda:controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, expand = True)

app = SeaOfBTCapp()
ani = animation.FuncAnimation(f, animate, frames=[None], interval=1000)
app.mainloop()

# ani = animation.FuncAnimation(f, animate, frames=[None], interval=1000)
# plt.show()

""" break here"""

# import tkinter as tk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation

# def plot_graph():
#     # Create a Matplotlib Figure
#     fig = Figure(figsize=(5, 4), dpi=100)
#     ax = fig.add_subplot(111)
#     ax.plot([1, 2, 3, 4], [10, 15, 7, 3])

#     # Embed the Figure in a tkinter Canvas
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.draw()
#     canvas.get_tk_widget().pack()

# root = tk.Tk()
# button = tk.Button(root, text="Plot Graph", command=plot_graph)
# button.pack()

# root.mainloop()

""" break here """

# from tkinter import *

# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy as np

# from random import randrange
# from time import time

# clickCounter = 0

# blueCounter = 0
# redCounter = 0

# self = Tk()

# x1 = []
# y1 = []

# x2 = []
# y2 = []

# figure, ax = plt.subplots()

# # Since plotting a single graph
# curve1,  = ax.plot(0, 0, label="Behavior 1")
# curve2, = ax.plot(0, 0, label="Behavior 2")

# # Setting limits for x and y axis
# ax.set_xlim(0, 100)
# ax.set_ylim(0, 5) 

# def graphBlue(i, blueCounter):
#     # clickCounter += 2
#     blueCounter += 1
#     # redCounter = 0

#     x1.append(i)
#     y1.append(blueCounter)

#     curve1.set_xdata(x1)
#     curve1.set_ydata(y1)

#     return curve1,

# start_time = time()

# btnB = Button(self, width='14', height='6', bg='blue', command=lambda:graphBlue(time() - start_time, blueCounter))
# btnR = Button(self, width='14', height='6', bg='red')

# btnB.place(x='75', y='30')
# btnR.place(x='200', y='30')
 
# # def animation_function(i):
# #     x1.append(i * 15)
# #     y1.append(i)
 
# #     curve1.set_xdata(x1)
# #     curve1.set_ydata(y1)

# #     x2.append(i * 5)
# #     y2.append(i * 2)
# #     curve2.set_xdata(x2)
# #     curve2.set_ydata(y1)

# #     return curve1, curve2
 
# animation = FuncAnimation(figure,
#                           func = lambda:graphBlue(blueCounter),
#                           frames = np.arange(0, 10, 0.1),
#                           interval = 10)
# figure.legend()
# plt.show()

# self.mainloop()

''' break here'''

# from matplotlib import pyplot as plt
 
# x = []
# y = []
 
# for i in range(100):
#     x.append(i)
#     y.append(i)
 
#     # Mention x and y limits to define their range
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
     
#     # Plotting graph
#     plt.plot(x, y, color = 'green')
#     plt.pause(0.01)
 
# plt.show()


# import tkinter as tk
# import time
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# root = tk.Tk()
# root.title("Button Click Tracker")

# canvas = tk.Canvas(root, width=400, height=400)
# canvas.pack()

# dot = canvas.create_oval(190, 190, 210, 210, fill="blue")

# def move_dot(direction):
#     if direction == "up":
#         canvas.move(dot, 0, -10)
#     elif direction == "down":
#         canvas.move(dot, 0, 10)
#     elif direction == "left":
#         canvas.move(dot, -10, 0)
#     elif direction == "right":
#         canvas.move(dot, 10, 0)

# up_button = tk.Button(root, text="Up", command=lambda: move_dot("up"))
# down_button = tk.Button(root, text="Down", command=lambda: move_dot("down"))
# left_button = tk.Button(root, text="Left", command=lambda: move_dot("left"))
# right_button = tk.Button(root, text="Right", command=lambda: move_dot("right"))

# up_button.pack()
# down_button.pack()
# left_button.pack()
# right_button.pack()

# button_clicks = {"Up": 0, "Down": 0, "Left": 0, "Right": 0}
# timestamps = []

# def update_clicks(button):
#     button_clicks[button] += 1
#     timestamps.append(time.time())

# def plot_data():
#     # plt.clf()
#     plt.bar(button_clicks.keys(), button_clicks.values())
#     plt.xlabel("Button")
#     plt.ylabel("Click Count")
#     plt.title("Button Click Count")
#     plt.show()

# def animate():
#     current_time = time.time()
#     while timestamps and current_time - timestamps[0] > 0.5:
#         timestamps.pop(0)
#         for button, count in button_clicks.items():
#             print(f"{button}: {count}")
#         plot_data()

# fig = plt.figure()
# ani = FuncAnimation(plt.gcf(), animate, frames=[None], interval=500)
# plt.show()

# root.mainloop()

# import matplotlib.pyplot as plt
# from matplotlib.animation import TimedAnimation

# class MyTimedAnimation(TimedAnimation):
#     def __init__(self, fig, animate_func, start_time, end_time, interval=100, blit=True):
#         self.start_time = start_time
#         self.end_time = end_time
#         super(MyTimedAnimation, self).__init__(fig, interval=interval, blit=blit)
#         self._setup(fig, animate_func)

# def animate(frame):
#     # Calculate the position of the sinusoidal wave
#     time_elapsed = frame * 0.1  # Adjust the speed of the animation
#     x = time_elapsed
#     y = 5 * (1 + 0.5 * (1 + frame % 20)) * (1 + 0.2 * (1 + frame % 5)) * (1 + 0.1 * (1 + frame % 2)) * (1 + 0.05 * (1 + frame % 5)) * (1 + 0.02 * (1 + frame % 10)) * (1 + 0.01 * (1 + frame % 20)) * (1 + 0.01 * (1 + frame % 40))
    
#     # Clear the plot and plot the sinusoidal wave
#     plt.clf()
#     plt.plot(x, y, 'ro')  # 'ro' means red color, round marker
#     plt.xlim(0, 10)
#     plt.ylim(0, 50)
#     plt.xlabel('Time')
#     plt.ylabel('Amplitude')
#     plt.title('Moving Sinusoidal Wave')

# fig = plt.figure()
# ani = MyTimedAnimation(fig, animate, start_time=0, end_time=10, interval=200)  # Adjust interval as needed
# plt.show()