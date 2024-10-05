# Robot Arm GUI Controller

This Python project is a GUI-based controller for a robotic arm, designed to move the arm to specific positions and perform actions. The graphical user interface (GUI) is built using `tkinter` and provides an interactive way to control a robot using serial communication.

## Features

- **Graphical Interface**: A grid-based UI that represents a cell culture plate.
- **Command Execution**: Sends movement and action commands to a robotic arm over a serial connection.
- **Save/Load Configuration**: Save and load configurations for cell actions, such as marking cells as active/inactive.
- **Export to CSV**: Export the cell configuration to a CSV file.
- **Robot Control**: Send the grid configuration to the robotic arm to perform the associated actions.

## How It Works

- The robot arm is controlled through serial communication, which is initialized by specifying the serial port (`COM3` by default) and baud rate.
- The GUI provides a grid (representing a 96-well cell culture plate), where each cell can be toggled between active (`green`) and inactive (`gray`).
- Commands are sent to the robot based on the active/inactive state of each cell in the grid.
- Users can save/load configurations as JSON and export the grid state as a CSV file.

## Requirements

- Python 3.x
- `tkinter` (for GUI)
- `pyserial` (for serial communication)

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/robot-arm-gui-controller.git
    ```
2. Install the required packages:
    ```bash
    pip install pyserial
    ```
3. Run the program:
    ```bash
    python GUI_ROBOT.py
    ```

## GUI Overview

- **Grid Representation**: The grid represents the cell culture plate. Each cell can be toggled on/off by clicking.
- **Header Buttons**:
  - `Save`: Save the current configuration to a JSON file.
  - `Load`: Load a saved configuration from a JSON file.
  - `Export`: Export the configuration as a CSV file.
  - `Send to Robot`: Send the current configuration to the robotic arm.

## Troubleshooting

- If you encounter a serial port error (`FileNotFoundError`), ensure that the correct serial port is specified in the code (`COM3` or change it to your active port).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

![image](https://github.com/user-attachments/assets/63245aba-d139-417a-9ef5-84051b458006)


