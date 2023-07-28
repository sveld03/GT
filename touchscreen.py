# touchscreen.py

# graphics library
from tkinter import *

# data visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# create root window
root = Tk()

# for the easy version
root.title("The Hard Easy Game")

# set geometry (widthxheight)
root.geometry('700x400')

# instructions
subtitle = Label(root, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
subtitle.place(anchor='nw')

def modeNull():
    # create buttons for moving the circle
    btn1 = Button(root, width='7', height='3', bg='blue')
    btn2 = Button(root, width='7', height='3', bg='red')
    btn3 = Button(root, width='7', height='3', bg='green')
    btn4 = Button(root, width='7', height='3', bg='yellow')

    # place the buttons on the screen
    btn1.place(x='75', y='30')
    btn2.place(x='150', y='30')
    btn3.place(x='225', y='30')
    btn4.place(x='300', y='30')

def modeA():
    print("Mode A")

def modeB():
    # btn1.config(command=move_left)
    # btn2.config(command=move_right)
    # btn3.config(command=move_up)
    # btn4.config(command=move_down)

    def move_left():
        if canvas.coords(dot)[0] > 0:
            canvas.move(dot, -10, 0)

    def move_right():
        if canvas.coords(dot)[2] < 600:
            canvas.move(dot, 10, 0)
            check_completion(btn1, btn2, btn3, btn4)

    def move_up():
        if canvas.coords(dot)[1] > 0:
            canvas.move(dot, 0, -10)

    def move_down():
        if canvas.coords(dot)[3] > 0:
            canvas.move(dot, 0, 10)

    btn1 = Button(root, width='7', height='3', bg='blue', command=move_left)
    btn2 = Button(root, width='7', height='3', bg='red', command=move_right)
    btn3 = Button(root, width='7', height='3', bg='green', command=move_up)
    btn4 = Button(root, width='7', height='3', bg='yellow', command=move_down)

    # place the buttons on the screen
    btn1.place(x='75', y='30')
    btn2.place(x='150', y='30')
    btn3.place(x='225', y='30')
    btn4.place(x='300', y='30')
    
    def check_completion(btn1, btn2, btn3, btn4):
        if canvas.coords(dot)[2] >= 550:
            btn1.config(state=DISABLED)
            btn2.config(state=DISABLED)
            btn3.config(state=DISABLED)
            btn4.config(state=DISABLED)
            congrats = Label(root, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')
            congrats.place(x=300, y=375)

def modeC():
    print("Mode C")

def modeD():
    print("Mode D")

def modeE():
    print("Mode E")

# game mode selection menu
modeMenu = Menu(root)
gameModes = Menu(modeMenu)
modeMenu.add_cascade(label='Select Game Mode', menu=gameModes)
gameModes.add_command(label='A', command = modeA)
gameModes.add_command(label='B', command = modeB)
gameModes.add_command(label='C', command = modeC)
gameModes.add_command(label='D', command = modeD)
gameModes.add_command(label='E', command = modeE)
# modeMenu.place(anchor='ne')
# modeMenu.add_cascade(label='Menu', menu=modeMenu)
root.config(menu=modeMenu)

# create canvas for dot
canvas_width = 600
canvas_height = 250
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='white')
# canvas.grid(root, )
# canvas.pack()
canvas.place(x='50', y='100')

# initial position of dot
dot_radius = 20
dot_x = 50
dot_y = 120
# dot_y = canvas_height // 2

# create dot
dot = canvas.create_oval(dot_x - dot_radius, dot_y - dot_radius,
                         dot_x + dot_radius, dot_y + dot_radius,
                         outline='red', fill='red')

# def check_completion(btn1, btn2, btn3, btn4):
#     if canvas.coords(dot)[2] >= 550:
#         btn1.config(state=DISABLED)
#         btn2.config(state=DISABLED)
#         btn3.config(state=DISABLED)
#         btn4.config(state=DISABLED)
#         congrats = Label(root, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')
#         congrats.place(x=300, y=375)

# def move_left():
#     if canvas.coords(dot)[0] > 0:
#         canvas.move(dot, -10, 0)

# def move_right():
#     if canvas.coords(dot)[2] < 600:
#         canvas.move(dot, 10, 0)
#         check_completion(btn1, btn2, btn3, btn4)

# def move_up():
#     if canvas.coords(dot)[1] > 0:
#         canvas.move(dot, 0, -10)

# def move_down():
#     if canvas.coords(dot)[3] > 0:
#         canvas.move(dot, 0, 10)

# create buttons for moving the circle
btn1 = Button(root, width='7', height='3', bg='blue', state=DISABLED)
btn2 = Button(root, width='7', height='3', bg='red', state=DISABLED)
btn3 = Button(root, width='7', height='3', bg='green', state=DISABLED)
btn4 = Button(root, width='7', height='3', bg='yellow', state=DISABLED)

# place the buttons on the screen
btn1.place(x='75', y='30')
btn2.place(x='150', y='30')
btn3.place(x='225', y='30')
btn4.place(x='300', y='30')

root.mainloop()