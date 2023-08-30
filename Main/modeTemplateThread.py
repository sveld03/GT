# Base class for all game modes

# Screen and utilities
from infrastructure import *

# from abc import ABC, abstractmethod

# Game mode A: simplest version, blue button moves dot right
class ModeTemplate:
    def __init__(self, screen, timer):
        
        self.screen = screen
        self.run = True
        
        # Get access to buttons on screen
        self.btnB = self.screen.btnB
        self.btnR = self.screen.btnR
        self.btnG = self.screen.btnG
        self.btnY = self.screen.btnY

        self.mode_char = self.screen.mode_char
        self.player_name = self.screen.nameNtr.get()
        self.trial_number = self.screen.trialNtr.get()

        # Get access to movement functions
        self.move_left = self.screen.move_left
        self.move_up = self.screen.move_up
        self.move_down = self.screen.move_down

        # Game stopwatch
        self.timer = timer

        # # Connect to database
        # self.freqprof = freqprof
        # self.Cursor = cursor

        self.button_clicks = {"blue": 0, "red": 0, "green": 0, "yellow": 0}
        # self.timestamps = []

        self.processing_thread = None
        self.processing_interval = 0.1  # seconds

        # self.data_queue = queue.Queue()
        self.x_data = []
        self.y1_data = []
        self.y2_data = []
        self.y3_data = []
        self.y4_data = []

        # self.animation_running = False

    def start(self):
        # Assign movement functions to buttons
        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

        self.fig, self.ax = plt.subplots()
        self.line1, = self.ax.plot(self.x_data, self.y1_data, 'b', linestyle='solid', label="Behavior 1")
        self.line2, = self.ax.plot(self.x_data, self.y2_data, 'r', linestyle='solid', label="Behavior 2")
        self.line3, = self.ax.plot(self.x_data, self.y3_data, 'g', linestyle='solid', label="Behavior 3")
        self.line4, = self.ax.plot(self.x_data, self.y4_data, linestyle='solid', label="Behavior 4")

        self.update_data()
        self.animate()

    def update_clicks(self, button):
        self.button_clicks[button] = 1
        # self.timestamps.append(time())

    def process_data(self):
        # if self.animation_running == False:
        #     self.animate()
        #     self.animation_running = True

        # database connection
        self.freqprof = sqlite3.connect('freqprof.db')
        self.Cursor = self.freqprof.cursor()

        self.Cursor.execute("SELECT id FROM FreqProf ORDER BY id DESC LIMIT 1")
        self.last_id = self.Cursor.fetchone()

        while True:
            start_time = time()

            self.record_data()

            elapsed_time = time() - start_time

            if elapsed_time < self.processing_interval:
                sleep(self.processing_interval - elapsed_time)

    def update_data(self):
        if self.processing_thread is None:
            self.processing_thread = threading.Thread(target=self.process_data)
            self.processing_thread.start()

        self.screen.after(int(self.processing_interval * 1000), self.update_data)

    def record_data(self):
        print("hello")
        click = False
        if self.button_clicks['blue'] == 1 and self.run == True:
            record_blue(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
        if self.button_clicks['red'] == 1 and self.run == True:
            record_red(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
        if self.button_clicks['green'] == 1 and self.run == True:
            record_green(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
        if self.button_clicks['yellow'] == 1 and self.run == True:
            record_yellow(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
        if click == False and self.run == True:
            record_none(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)

        for button in self.button_clicks:
            self.button_clicks[button] = 0

    # def handle_data(self, event):
    #     self.record_data()
    #     self.update_plot()

    def update_plot(self, frame):

        # Fetch new data from the database
        # self.Cursor.execute("SELECT time, B1, B2, B3, B4 FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? AND time > ?", 
        #                     (self.screen.nameNtr.get(), self.screen.mode_char, self.screen.trialNtr.get(), frame * 0.1))
        self.Cursor.execute("SELECT time, B1, B2, B3, B4 FROM FreqProf WHERE name = ? AND mode = ? AND trial = ? AND time > ?", 
                            (self.player_name, self.mode_char, self.trial_number, frame * 0.1))
        new_data = self.Cursor.fetchall()

        for row in new_data:
            print(row)

        # if new_data[0][0] != self.last_id + 1:
        #     sys.exit("Error: sample is not continuous, may be a combination of multiple trials")

        # for n in range(len(new_data) - 1):
        #     if new_data[n][0] + 1 != new_data[n + 1][0]:
        #         sys.exit("Error: sample is not continuous, may be a combination of multiple trials")

        # Update the plot data
        for row in new_data:
            self.x_data.append(row[0])
            self.y1_data.append(row[1])
            self.y2_data.append(row[2])
            self.y3_data.append(row[3])
            self.y4_data.append(row[4])

        # Update the line plot
        self.line1.set_data(self.x_data, self.y1_data)
        self.line2.set_data(self.x_data, self.y2_data)
        self.line3.set_data(self.x_data, self.y3_data)
        self.line4.set_data(self.x_data, self.y4_data)

    def animate(self):

        # Create an animation that updates the plot every 0.1 seconds
        self.ani = FuncAnimation(self.fig, self.update_plot, frames=itertools.count(), repeat=False, save_count=MAX_FRAMES)

        # Display the plot
        plt.legend()
        plt.show()

    # Button assignment functions; same for all game modes

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def assign_btnG(self):
        self.btnG.config(command=self.move_green)

    def assign_btnY(self):
        self.btnY.config(command=self.move_yellow)

    # Move right function that sets run = False
    def move_right(self):
        run = self.screen.move_right(self.ani, self.run)
        self.run = run

    # Button movement functions: different across game modes

    # Move dot right, then record blue button click
    def move_blue(self):
        self.update_clicks("blue")

    # Move dot left, then record red button click
    def move_red(self):
        self.update_clicks("red")
    
    # Move dot up, then record green button click
    def move_green(self):
        self.update_clicks("green")

    # Move dot down, then record yellow button click
    def move_yellow(self):
        self.update_clicks("yellow")