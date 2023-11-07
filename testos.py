import tkinter as tk
from tkinter import Label, Entry, Button, Canvas, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class DiskSchedulerApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Disk Scheduler Simulation")
        
        self.algorithm = "FCFS"
        self.request_queue = []
        self.disk_head = [50, 0]  # Starting position of disk head (x, y)
        self.initial_position = [50, 0]  # Initial position of Read-Write head (x, y)

        self.blink_color = 'blue'  # Color to use when blinking
        self.normal_color = 'green'  # Normal color of the disk head

        self.create_widgets()

    def create_widgets(self):
        # Buttons to select algorithm
        self.fcfs_button = Button(self.master, text="FCFS", command=self.select_fcfs)
        self.scan_button = Button(self.master, text="SCAN", command=self.select_scan)

        self.fcfs_button.pack()
        self.scan_button.pack()

        # Input field for request queue
        self.input_label = Label(self.master, text="Enter Request Queue (comma-separated):")
        self.input_field = Entry(self.master)

        self.input_label.pack()
        self.input_field.pack()

        # Input field for initial position
        self.init_label = Label(self.master, text="Enter Initial Position of Read-Write head (x, y):")
        self.init_field = Entry(self.master)

        self.init_label.pack()
        self.init_field.pack()

        # Canvas for graph
        self.figure, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.ax.axis('on')  # Make axis visible
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Button to start simulation
        self.start_button = Button(self.master, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

    def select_fcfs(self):
        self.algorithm = "FCFS"

    def select_scan(self):
        self.algorithm = "SCAN"

    def draw_disk_head(self, color='red'):
        self.ax.clear()
        self.ax.plot(self.disk_head[0], self.disk_head[1], 'o', color=color)  # Draw current position
        self.ax.set_xlim(-10, 110)
        self.ax.set_ylim(-10, 10)
        self.ax.axis('on')  # Make sure axis is visible
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.canvas.draw()

    def start_simulation(self):
        self.disk_head = list(map(int, self.init_field.get().split(',')))  # Set initial position
        self.request_queue = list(map(int, self.input_field.get().split(',')))

        if not self.request_queue or len(self.disk_head) != 2:
            messagebox.showerror("Error", "Please enter a valid request queue and initial position.")
            return

        if self.algorithm == "FCFS":
            self.fcfs_algorithm()
        elif self.algorithm == "SCAN":
            self.scan_algorithm()

    def fcfs_algorithm(self):
        for track in self.request_queue:
            self.move_disk_head([track, 0])

    def scan_algorithm(self):
        self.request_queue.sort()

        # Head moves from left to right first
        for track in self.request_queue:
            if track >= self.disk_head[0]:
                self.move_disk_head([track, 0])

        # Then head moves from right to left
        for track in reversed(self.request_queue):
            if track < self.disk_head[0]:
                self.move_disk_head([track, 0])

    def move_disk_head(self, target_track):
        while self.disk_head != target_track:
            time.sleep(0.1)  # Add a short delay for animation effect

            for i in range(2):
                if self.disk_head[i] < target_track[i]:
                    self.disk_head[i] += 1
                elif self.disk_head[i] > target_track[i]:
                    self.disk_head[i] -= 1

            if self.disk_head in self.request_queue:  # Check if disk head lands on a request
                self.blink_disk_head()  # Blink the disk head
            else:
                self.draw_disk_head()

            self.master.update_idletasks()

    def blink_disk_head(self):
        for _ in range(6):  # Blink three times
            self.draw_disk_head(color=self.blink_color)
            self.master.update_idletasks()
            time.sleep(0.2)
            self.draw_disk_head(color=self.normal_color)
            self.master.update_idletasks()
            time.sleep(0.2)

def main():
    root = tk.Tk()
    app = DiskSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
