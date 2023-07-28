# touchscreen.py

# graphics library
from tkinter import *

# data visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# create root window
root = Tk()

# root window title and dimension
# note: this will be the title for the complex version of the game.
# root.title("The Hardest Easy Game")

# for the easy version
root.title("The Easy Game")

# set geometry (widthxheight)
root.geometry('700x400')

# for hard mode
# subtitle = Label(root, text = "Click the buttons to get the dot to the right side of the screen. Have fun! >:)")

# for easy mode
subtitle = Label(root, text = "Click the buttons to get the dot to the right side of the screen. Have fun! :)")
subtitle.place(anchor='nw')

# create canvas for dot
canvas_width = 600
canvas_height = 250
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='white')
# canvas.grid(root, )
# canvas.pack()
canvas.place(x='50', y='100')

# initial position of dot
dot_radius = 20
dot_x = 300
dot_y = 200
# dot_y = canvas_height // 2

# create dot
dot = canvas.create_oval(dot_x - dot_radius, dot_y - dot_radius,
                         dot_x + dot_radius, dot_y + dot_radius,
                         outline='red', fill='red')

# function to move dot left
def move_left():
    canvas.move(dot, -10, 0)

# function to move dot right
def move_right():
    canvas.move(dot, 10, 0)

# function to move dot up
def move_up():
    canvas.move(dot, 0, -10)

def move_down():
    canvas.move(dot, 0, 10)

# create buttons for moving the circle
btn_left = Button(root, width='7', height='3', bg='blue', command=move_left)
btn_right = Button(root, width='7', height='3', bg='red', command=move_right)

# place the buttons on the screen
btn_left.place(x='75', y='30')
btn_right.place(x='150', y='30')

root.mainloop()