# Base class for all game modes

# Screen and utilities
from infrastructure import *

from params import *

# Game mode A: simplest version, blue button moves dot right
class ModeTemplate:
    def __init__(self, freqprof, cursor, screen, timer, params):
        
        # Store parameter and game info
        self.params = params
        self.screen = screen
        self.run = True

        # Won't start until this is True
        self.button_clicked = False

        # Frequency profile window -- default is 3s
        self.window = self.params.get_window()
        
        # Get access to buttons on screen
        self.btnB = self.screen.btnB
        self.btnR = self.screen.btnR
        self.btnG = self.screen.btnG
        self.btnY = self.screen.btnY

        # Store mode, player, and trial
        self.mode_char = self.screen.mode_char
        self.player_name = self.params.nameNtr.get()
        self.trial_number = self.params.trialNtr.get()

        # Game stopwatch
        self.timer = timer

        # Connect to database
        self.freqprof = freqprof
        self.Cursor = cursor

        # Get the last ID from the database, to make sure our trial is continuous
        self.Cursor.execute("SELECT id FROM FreqProf ORDER BY id DESC LIMIT 1")
        self.last_id = self.Cursor.fetchone()

        # The value for a given key briefly changes to 1 when that button is clicked
        self.button_clicks = {"blue": 0, "red": 0, "green": 0, "yellow": 0}

        # x_data is in seconds, y is button clicks, freq_data is what is graphed on the y-axis of the frequency profile
        self.x_data = []
        self.y_data = [[], [], [], []]
        self.freq_data = [[], [], [], []]

        # For transmitting frequency data -- not in use right now but helpful if we want to implement threading or multiprocessing to boost performance
        self.queue = queue.Queue()

        # Plots for frequency profile, probability profile, and accuracy profile
        self.fig, self.axs = plt.subplots(3, 1, sharex=True, sharey=False)

        # In this file we will be working exclusively with the frequency profile
        self.ax = self.axs[2]
        self.ax.set_ylim(0, 1)

        # Lines to represent frequency of presses for each button, henceforth called behaviors
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid', label="Behavior 1")
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid', label="Behavior 2")
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid', label="Behavior 3")
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid', label="Behavior 4")

        # Assign the buttons to their respective functions
        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

    # When a button is clicked, update the dictionary
    def update_clicks(self, button):
        self.button_clicks[button] = 1

    # For each button, it its value is 1 then add that to the y data
    def record_data(self, frame):
        click = False

        if self.button_clicks["blue"] == 1 and self.run == True:
            record_blue(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number) # Adds to the FreqProf table
            click = True # lets us know to skip the record_none
            self.x_data.append(frame * .1) # equivalent to the timestamp
            self.y_data[0].append(1) # blue is behavior 1
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        if self.button_clicks["red"] == 1 and self.run == True:
            record_red(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(1) # red is behavior 2
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        if self.button_clicks["green"] == 1 and self.run == True:
            record_green(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(1) # green is behavior 3
            self.y_data[3].append(0)

        if self.button_clicks["yellow"] == 1 and self.run == True:
            record_yellow(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(1) # yellow is behavior 4
        
        # If no buttons were clicked in the last .1 second, append a row of all 0s
        if click == False and self.run == True:
            record_none(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        # reset the value of all buttons
        for button in self.button_clicks:
            self.button_clicks[button] = 0

        # stores the number of frames over which we want to average to get our frequency value, based on the frequency profile window
        count = self.window * 10
        if len(self.x_data) < count: 
            count = len(self.x_data)

        new_freq_data = []

        # Calculate our frequency value
        for i in range(4):
            new_freq_data.append(0)
            for j in range(count):
                new_freq_data[i] += self.y_data[i][-j] # add the y-values within the range of the window
            new_freq_data[i] = new_freq_data[i] / (self.window * 10) # divide by the number of frames we added up

        self.queue.put(new_freq_data)
        
        # Append our newest frequency values to the profile
        for i in range(4):
            if len(self.freq_data[i]) >= 2:
                # Average this value with the previous 2 values to smooth out the curve
                self.freq_data[i].append((new_freq_data[i] + self.freq_data[i][-1] + self.freq_data[i][-2])/3)
                # self.freq_data[i].append((new_freq_data[i] + self.freq_data[i][-1])/2) # can also average with only the previous value for less smoothness and more precision
            else:
                self.freq_data[i].append(new_freq_data[i])

        # For the first ten seconds, the lines include all the data
        if frame <= 100:
            self.line1.set_data(self.x_data, self.freq_data[0])
            self.line2.set_data(self.x_data, self.freq_data[1])
            self.line3.set_data(self.x_data, self.freq_data[2])
            self.line4.set_data(self.x_data, self.freq_data[3])

        # After the first ten seconds, the lines include only the last ten seconds of data
        if frame > 100:
            self.line1.set_data(self.x_data[-100:], self.freq_data[0][-100:])
            self.line2.set_data(self.x_data[-100:], self.freq_data[1][-100:])
            self.line3.set_data(self.x_data[-100:], self.freq_data[2][-100:])
            self.line4.set_data(self.x_data[-100:], self.freq_data[3][-100:])

        return self.line1, self.line2, self.line3, self.line4

    # Button assignment functions; same for all game modes

    def assign_btnB(self):
        self.btnB.config(command=self.move_blue)

    def assign_btnR(self):
        self.btnR.config(command=self.move_red)

    def assign_btnG(self):
        self.btnG.config(command=self.move_green)

    def assign_btnY(self):
        self.btnY.config(command=self.move_yellow)

    # Move right function that sets run = False when the finish line has been reached
    def move_right(self, distance=40):
        if self.screen.canvas.coords(self.screen.dot)[2] < 1225:
            self.screen.canvas.move(self.screen.dot, distance, 0)
            return True
        else:
            self.run = False
            self.screen.reset() # reset the screen
            self.screen.congrats.place(x=50, y=625) # congratulate the player
            self.screen.event_generate("<<stopGraph>>") # stop the graph
            return False

    # Moves dot left
    def move_left(self, distance=40):
        if self.screen.canvas.coords(self.screen.dot)[0] > 0:
            self.screen.canvas.move(self.screen.dot, -distance, 0)
            return True
        return False

    # Moves dot up
    def move_up(self, distance=40):
        if self.screen.canvas.coords(self.screen.dot)[1] > 0:
            self.screen.canvas.move(self.screen.dot, 0, -distance)
            return True
        return False

    # Moves dot down
    def move_down(self, distance=40):
        if self.screen.canvas.coords(self.screen.dot)[3] < 450:
            self.screen.canvas.move(self.screen.dot, 0, distance)
            return True
        return False


    # Button movement functions: different across game modes -- for all buttons, if it is the first click then start the timer and graph

    # Move dot right, then record blue button click
    def move_blue(self):
        if self.button_clicked == False:
            self.button_clicked = True
            self.timer.start_time = time()
            self.screen.event_generate("<<buttonClicked>>")
        self.update_clicks("blue")

    # Move dot left, then record red button click
    def move_red(self):
        if self.button_clicked == False:
            self.button_clicked = True
            self.timer.start_time = time()
            self.screen.event_generate("<<buttonClicked>>")
        self.update_clicks("red")
    
    # Move dot up, then record green button click
    def move_green(self):
        if self.button_clicked == False:
            self.button_clicked = True
            self.timer.start_time = time()
            self.screen.event_generate("<<buttonClicked>>")
        self.update_clicks("green")

    # Move dot down, then record yellow button click
    def move_yellow(self):
        if self.button_clicked == False:
            self.button_clicked = True
            self.timer.start_time = time()
            self.screen.event_generate("<<buttonClicked>>")
        self.update_clicks("yellow")