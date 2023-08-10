import matplotlib.pyplot as plt
import threading
import time

# Initialize lists to store button press frequencies
colors = ['blue', 'red', 'green', 'yellow']
button_presses = [[] for _ in colors]

# Function to update the plot in real-time
def update_plot():
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()

    lines = [ax.plot([], label=color)[0] for color in colors]
    ax.set_xlim(0, 10)  # Adjust the x-axis limits as needed
    ax.set_ylim(0, 10)  # Adjust the y-axis limits as needed
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Button Press Frequency')
    ax.legend()

    while True:
        for i, line in enumerate(lines):
            line.set_xdata(list(range(len(button_presses[i]))))
            line.set_ydata(button_presses[i])
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.1)  # Pause to update the plot

# Function to simulate button presses and update the lists
def simulate_button_presses():
    while True:
        try:
            button_index = int(input("Enter button index (0-blue, 1-red, 2-green, 3-yellow): "))
            if 0 <= button_index < len(colors):
                button_presses[button_index].append(len(button_presses[button_index]) + 1)
        except ValueError:
            print("Invalid input. Please enter a valid button index.")

# Start the real-time plot update thread
plot_thread = threading.Thread(target=update_plot)
plot_thread.daemon = True  # Allow the thread to exit when the main program exits
plot_thread.start()

# Start the button press simulation thread
simulate_thread = threading.Thread(target=simulate_button_presses)
simulate_thread.daemon = True
simulate_thread.start()

# Keep the main thread running
while True:
    pass
