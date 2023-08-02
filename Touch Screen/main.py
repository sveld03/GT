from utilities import *

from modeA import ModeA

class Game(Tk):
    def __init__(self):
        super().__init__()

        # for the easy version
        self.title("The Hard Easy Game")

        # set geometry (widthxheight)
        self.geometry('1360x710')

        self.resizable(width=False, height=False)

        # instructions
        subtitle = Label(self, text = "Choose game mode above, then click the buttons to get the dot to the right side of the screen. Have fun! :)")
        subtitle.place(anchor='nw')

        self.finish = Label(self, text="Finish Line")
        self.finish.place(x=1235, y=125)

        self.congrats = Label(self, text="Congratulations! You completed the game! Exit or try another mode.", bg='green')

        self.canvas = Canvas(self, bg="white", width=1250, height = 500)
        self.canvas.place(x=50, y=150)
        # self.canvas.pack(fill=BOTH, padx=50, pady=150, expand=True)

        # self.canvas.bind("<Configure>", self.on_resize)

        # initial position of dot
        dot_radius = 20
        self.init_x1 = 50 - dot_radius
        self.init_y1 = 250 - dot_radius
        self.init_x2 = 50 + dot_radius
        self.init_y2 = 250 + dot_radius

        # create dot
        self.dot = self.canvas.create_oval(self.init_x1, self.init_y1,
                         self.init_x2, self.init_y2,
                         outline='red', fill='red')
        
        self.line = self.canvas.create_line(1225, 0, 1225, 500)
        
        # self.update_dot_position("<Configure>")
        
        self.game_mode = None

        self.create_buttons()
        self.create_menu()

        # self.bind("<Configure>", self.on_resize)

    # def on_resize(self, event):
    #         # self.canvas_width = event.width
    #         # self.canvas_height = event.height
    #         # self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
    #         self.update_dot_position

    # def update_dot_position(self, event):
    #     canvas_width = event.width
    #     canvas_height = event.height

    #     center_x = canvas_width // 2
    #     center_y = canvas_height // 2

    #     self.canvas.coords(self.dot, center_x - 10, center_y - 10, 
    #                         center_x + 10, center_y + 10)
    
    # Mode A: simplest version, blue button moves dot right
    def modeA(self):
        self.game_mode = ModeA()
        self.game_mode.mainloop()
        # self.game_mode = "A"
        # self.congrats.place_forget()

    # # Mode B: a specific sequence of 4 button presses moves dot right
    # def modeB(self):
    #     self.game_mode = modeB()
    #     # self.congrats.place_forget()

    # # Mode C: double-click green for 1st half, red-yellow for 2nd half
    # def modeC(self):
    #     self.game_mode = modeC()
    #     # self.congrats.place_forget()

    # def mode1(self):
    #     self.game_mode = mode1()
    #     # self.congrats.place_forget()
    
    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        game_menu = Menu(menubar, tearoff=0)
        game_menu.add_command(label='A', command=self.modeA)
        # game_menu.add_command(label='B', command=self.modeB)
        # game_menu.add_command(label='C', command=self.modeC)
        # game_menu.add_command(label='1', command=self.mode1)

        menubar.add_cascade(label="Game Modes", menu=game_menu)
    
    def create_buttons(self):
        self.btnB = Button(self, width='14', height='6', bg='blue', command=self.game_mode.move_blue)
        self.btnR = Button(self, width='14', height='6', bg='red', command=self.game_mode.move_red)
        self.btnG = Button(self, width='14', height='6', bg='green', command=self.game_mode.move_green)
        self.btnY = Button(self, width='14', height='6', bg='yellow', command=self.game_mode.move_yellow)

        self.btnB.place(x='75', y='30')
        self.btnR.place(x='200', y='30')
        self.btnG.place(x='325', y='30')
        self.btnY.place(x='450', y='30')

    def check_completion(self):
        if self.canvas.coords(self.dot)[2] >= 1225:
            self.game_mode = None
            self.congrats.place(x=50, y=675)

            x1, y1, x2, y2 = self.canvas.coords(self.dot)
            dx = self.init_x1 - x1
            dy = self.init_y1 - y1
            self.canvas.move(self.dot, dx, dy)

    def move_left(self):
        if self.canvas.coords(self.dot)[0] > 0:
            self.canvas.move(self.dot, -20, 0)

    def move_right(self):
        if self.canvas.coords(self.dot)[2] < 1250:
            self.canvas.move(self.dot, 20, 0)
            self.check_completion()

    def move_up(self):
        if self.canvas.coords(self.dot)[1] > 0:
            self.canvas.move(self.dot, 0, -20)

    def move_down(self):
        if self.canvas.coords(self.dot)[3] < 500:
            self.canvas.move(self.dot, 0, 20)
