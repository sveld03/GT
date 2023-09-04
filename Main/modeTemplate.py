# Base class for all game modes

# Screen and utilities
from infrastructure import *

from params import *

# Game mode A: simplest version, blue button moves dot right
class ModeTemplate:
    def __init__(self, freqprof, cursor, screen, timer, params):
        
        self.params = params
        self.screen = screen
        self.run = True

        self.window = self.params.get_window()
        
        # Get access to buttons on screen
        self.btnB = self.screen.btnB
        self.btnR = self.screen.btnR
        self.btnG = self.screen.btnG
        self.btnY = self.screen.btnY

        self.mode_char = self.screen.mode_char
        self.player_name = self.params.nameNtr.get()
        self.trial_number = self.params.trialNtr.get()

        # Game stopwatch
        self.timer = timer

        # Connect to database
        self.freqprof = freqprof
        self.Cursor = cursor

        self.Cursor.execute("SELECT id FROM FreqProf ORDER BY id DESC LIMIT 1")
        self.last_id = self.Cursor.fetchone()

        self.button_clicks = {"blue": 0, "red": 0, "green": 0, "yellow": 0}

        self.x_data = []
        self.y_data = [[], [], [], []]
        self.freq_data = [[], [], [], []]

        self.queue = queue.Queue()

        self.fig, self.axs = plt.subplots(3, 1, sharex=True, sharey=False)
        self.ax = self.axs[2]
        self.ax.set_ylim(0, 1)
        self.line1, = self.ax.plot([], [], 'b', linestyle='solid', label="Behavior 1")
        self.line2, = self.ax.plot([], [], 'r', linestyle='solid', label="Behavior 2")
        self.line3, = self.ax.plot([], [], 'g', linestyle='solid', label="Behavior 3")
        self.line4, = self.ax.plot([], [], 'y', linestyle='solid', label="Behavior 4")

        # self.ax.set_ylim(0, 1)
        # self.ax.set_xlim(0, 10)

        self.assign_btnB()
        self.assign_btnR()
        self.assign_btnG()
        self.assign_btnY()

        # self.ax.set_xticks([0, 2, 4, 6, 8, 10], labels=["-10", "-8", "-6", "-4", "-2", "0"])

    def update_clicks(self, button):
        self.button_clicks[button] = 1

    def record_data(self, frame):
        click = False

        if self.button_clicks["blue"] == 1 and self.run == True:
            record_blue(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            # self.x_data.append(truncate_after_first_decimal(self.timer.time_elapsed()))
            self.x_data.append(frame * .1)
            self.y_data[0].append(1)
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        if self.button_clicks["red"] == 1 and self.run == True:
            record_red(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            # self.x_data.append(truncate_after_first_decimal(self.timer.time_elapsed()))
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(1)
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        if self.button_clicks["green"] == 1 and self.run == True:
            record_green(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            # self.x_data.append(truncate_after_first_decimal(self.timer.time_elapsed()))
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(1)
            self.y_data[3].append(0)

        if self.button_clicks["yellow"] == 1 and self.run == True:
            record_yellow(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            click = True
            # self.x_data.append(truncate_after_first_decimal(self.timer.time_elapsed()))
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(1)
        
        if click == False and self.run == True:
            record_none(self.Cursor, self.freqprof, self.timer, self.mode_char, self.player_name, self.trial_number)
            # self.x_data.append(truncate_after_first_decimal(self.timer.time_elapsed()))
            self.x_data.append(frame * .1)
            self.y_data[0].append(0)
            self.y_data[1].append(0)
            self.y_data[2].append(0)
            self.y_data[3].append(0)

        for button in self.button_clicks:
            self.button_clicks[button] = 0

        count = self.window * 10
        if len(self.x_data) < count: 
            count = len(self.x_data)

        new_freq_data = []
        for i in range(4):
            new_freq_data.append(0)
            for j in range(count):
                new_freq_data[i] += self.y_data[i][-j]
            new_freq_data[i] = new_freq_data[i] / (self.window * 10)

        self.queue.put(new_freq_data)
        
        for i in range(4):
            self.freq_data[i].append(new_freq_data[i])

        window_start = 0
        if frame <= 100:
            self.line1.set_data(self.x_data, self.freq_data[0])
            self.line2.set_data(self.x_data, self.freq_data[1])
            self.line3.set_data(self.x_data, self.freq_data[2])
            self.line4.set_data(self.x_data, self.freq_data[3])

        if frame > 100:
            window_start = frame/10 - 10

            self.line1.set_data(self.x_data[-100:], self.freq_data[0][-100:])
            self.line2.set_data(self.x_data[-100:], self.freq_data[1][-100:])
            self.line3.set_data(self.x_data[-100:], self.freq_data[2][-100:])
            self.line4.set_data(self.x_data[-100:], self.freq_data[3][-100:])

        # self.ax.set_xlim(window_start, window_start + 10)
        
        # xticks = [window_start, 2+window_start, 4+window_start, 6+window_start, 8+window_start, 10+window_start]
        # labels = [str(x) for x in xticks]
        # # self.ax.set_xticks(xticks, labels=[str(2+window_start), str(4+window_start), str(6+window_start), str(8+window_start), str(10+window_start)])

        # if window_start % 2 == 0:
        #     self.ax.set_xticks(xticks, labels=labels)

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

    # Move right function that sets run = False
    def move_right(self):
        if self.screen.canvas.coords(self.screen.dot)[2] < 1225:
            self.screen.canvas.move(self.screen.dot, 20, 0)
            return True
        else:
            self.run = False
            self.screen.reset()
            # self.ani.event_source.stop()
            self.screen.congrats.place(x=50, y=625)
            self.screen.event_generate("<<stopGraph>>")
            return False

    # Moves dot left
    def move_left(self):
        if self.screen.canvas.coords(self.screen.dot)[0] > 0:
            self.screen.canvas.move(self.screen.dot, -20, 0)
            return True
        return False

    # Moves dot up
    def move_up(self):
        if self.screen.canvas.coords(self.screen.dot)[1] > 0:
            self.screen.canvas.move(self.screen.dot, 0, -20)
            return True
        return False

    # Moves dot down
    def move_down(self):
        if self.screen.canvas.coords(self.screen.dot)[3] < 450:
            self.screen.canvas.move(self.screen.dot, 0, 20)
            return True
        return False

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