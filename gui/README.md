# Gripper Control GUI (outdated)

A lightweight GUI application for controlling an Arduino-based gripper via serial communication.

## Features

* Connects to Arduino through a serial port
* Intuitive buttons and configuration options for basic control
* Real-time status updates
* Automatic detection of available serial ports

## Requirements

* Python 3.6 or newer
* `pyserial` library
* `tkinter` (typically included with Python)

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure the Arduino is connected to your computer.
2. Launch the GUI application:

```bash
python modern_gui.py
```

3. Select the appropriate COM port from the dropdown menu.
4. Click **Connect** to establish a connection.
5. Use the control buttons:

   * **Close Gripper** – Closes the gripper (sends command `1`)
   * **Open Gripper** – Opens the gripper (sends command `2`)
   * **Smart Grab** – Activates adaptive gripping with PID fine-tuning
   * **Emergency Stop** – Immediately halts all movement (sends command `0`)
6. Adjust settings for **Smart Grab**:

   * **Weight** – Weight of the object in grams
   * **Hardness** – A scale indicating how soft or hard the object is

   These parameters are used to calculate and apply the optimal gripping force.


## Troubleshooting

If you're unable to connect to the Arduino:

1. Confirm the Arduino is properly connected.
2. Verify that the correct COM port is selected.
3. Ensure no other program is using the serial port.
4. Check that the baud rate (115200) matches the value in your Arduino sketch.


## Vision

The current hardware does not support internet connectivity. If it did, this same interface and functionality could be adapted into a web-based application. This would allow users to control the gripper directly from a smartphone, enabling a more engaging and interactive experience—completely wireless and without needing a computer as an intermediary.
