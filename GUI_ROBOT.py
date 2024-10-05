import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import time
import serial

class RobotController:
    def __init__(self, port='COM3', baudrate=9600):
        # Initialize the serial connection to the robot
        try:
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for the connection to establish
        except serial.SerialException as e:
            print(f"Error connecting to robot: {e}")
            self.serial_connection = None
    
    def move_to_position(self, position):
        if self.serial_connection:
            command = f"MOVE {position}\n"  # Example command format
            self.serial_connection.write(command.encode())
            print(f"Sent command: {command.strip()}")
            response = self.serial_connection.readline().decode().strip()
            print(f"Robot response: {response}")
    
    def perform_action_at_position(self, position, action):
        if self.serial_connection:
            command = f"ACT {position} {action}\n"  # Example command format
            self.serial_connection.write(command.encode())
            print(f"Sent command: {command.strip()}")
            response = self.serial_connection.readline().decode().strip()
            print(f"Robot response: {response}")
    
    def close_connection(self):
        if self.serial_connection:
            self.serial_connection.close()

class CellCulturePlate:
    def __init__(self, master, robot):
        self.master = master
        self.master.title("Cell Culture Plate")
        
        # Set the path for saving/loading configurations
        self.config_path = r"C:\Users\tkate\Desktop\STEMAI\codes"
        self.robot = robot
        
        self.cells = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create header buttons with enhanced styling
        header_frame = tk.Frame(self.master, pady=10, bg="#f0f0f0")
        header_frame.pack(fill=tk.X)
        
        button_style = {"padx": 10, "pady": 5, "bg": "#4CAF50", "fg": "white", "font": ("Helvetica", 12, "bold")}
        
        save_button = tk.Button(header_frame, text="Save", command=self.save_config, **button_style)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = tk.Button(header_frame, text="Load", command=self.load_config, **button_style)
        load_button.pack(side=tk.LEFT, padx=5)
        
        export_button = tk.Button(header_frame, text="Export", command=self.export_config, **button_style)
        export_button.pack(side=tk.LEFT, padx=5)

        send_button = tk.Button(header_frame, text="Send to Robot", command=self.send_to_robot, **button_style)
        send_button.pack(side=tk.LEFT, padx=5)
        
        # Create the grid of cells with row and column labels
        grid_frame = tk.Frame(self.master, padx=20, pady=10, bg="#f0f0f0")
        grid_frame.pack()
        
        # Add column labels
        for col in range(12):
            tk.Label(grid_frame, text=str(col+1), width=4, height=2, bg="#f0f0f0", font=("Helvetica", 12, "bold")).grid(row=0, column=col+1)
        
        # Add row labels and cells
        for row in range(8):
            tk.Label(grid_frame, text=chr(65+row), width=4, height=2, bg="#f0f0f0", font=("Helvetica", 12, "bold")).grid(row=row+1, column=0)
            for col in range(12):
                cell_id = f"{chr(65+row)}{col+1}"
                cell = tk.Button(grid_frame, width=4, height=2, bg="gray", activebackground="lightgray", command=lambda cell_id=cell_id: self.toggle_cell(cell_id))
                cell.grid(row=row+1, column=col+1, padx=2, pady=2)
                self.cells[cell_id] = cell
        
        # Create footer summary with enhanced styling
        footer_frame = tk.Frame(self.master, pady=10, bg="#f0f0f0")
        footer_frame.pack(fill=tk.X)
        
        self.summary_label = tk.Label(footer_frame, text="Summary: Yes: 0   No: 96", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
        self.summary_label.pack()

    def toggle_cell(self, cell_id):
        cell = self.cells[cell_id]
        current_color = cell.cget("bg")
        new_color = "green" if current_color == "gray" else "gray"
        cell.config(bg=new_color)
        self.update_summary()
        
    def update_summary(self):
        yes_count = sum(1 for cell in self.cells.values() if cell.cget("bg") == "green")
        no_count = len(self.cells) - yes_count
        self.summary_label.config(text=f"Summary: Yes: {yes_count}   No: {no_count}")

    def send_to_robot(self):
        for cell_id, cell in self.cells.items():
            action = "Yes" if cell.cget("bg") == "green" else "No"
            self.robot.perform_action_at_position(cell_id, action)
        messagebox.showinfo("Send to Robot", "Commands sent to robot successfully.")
        
    def save_config(self):
        if not self.config_path:
            messagebox.showerror("Save Configuration", "Please set the path directory first.")
            return
        
        config = {cell_id: cell.cget("bg") for cell_id, cell in self.cells.items()}
        with open(os.path.join(self.config_path, "cell_config.json"), "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Save Configuration", "Configuration saved successfully!")
        
    def load_config(self):
        file_path = filedialog.askopenfilename(title="Select Configuration File", filetypes=[("JSON files", "*.json")])
        
        if not file_path:
            messagebox.showerror("Load Configuration", "No file selected.")
            return
        
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            for cell_id, color in config.items():
                self.cells[cell_id].config(bg=color)
            self.update_summary()
            messagebox.showinfo("Load Configuration", "Configuration loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Load Configuration", "No saved configuration found.")
        except json.JSONDecodeError:
            messagebox.showerror("Load Configuration", "Invalid configuration file.")
            
    def export_config(self):
        if not self.config_path:
            messagebox.showerror("Export Configuration", "Please set the path directory first.")
            return
        
        try:
            with open(os.path.join(self.config_path, "cell_config.json"), "r") as f:
                config = json.load(f)
            with open(os.path.join(self.config_path, "cell_config.csv"), "w") as f:
                for cell_id, color in config.items():
                    f.write(f"{cell_id},{color}\n")
            messagebox.showinfo("Export Configuration", "Configuration exported successfully as CSV!")
        except FileNotFoundError:
            messagebox.showerror("Export Configuration", "No saved configuration found.")

if __name__ == "__main__":
    root = tk.Tk()
    robot = RobotController()
    app = CellCulturePlate(master=root, robot=robot)
    root.mainloop()
    robot.close_connection()
