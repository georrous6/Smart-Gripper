# Gripper Control GUI

A lightweight GUI application for controlling an Arduino-based gripper via serial communication.

## Features

* Connects to Arduino through a serial port
* Intuitive buttons for basic control
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

1. Ensure the Gripper is connected to your computer.
2. Launch the GUI application:

```bash
python GripperControlGUI.py
```

3. Select the appropriate COM port from the dropdown menu.
4. Click **Connect** to establish a connection.
5. Use the control buttons:

   * **Secure Grip** – Starts to close the gripper until it grabs something (sends command `1`)
   * **Release Grip** – Starts to open the gripper (sends command `2`)
   * **Emergency Stop** – Immediately halts all movement (sends command `0`)
6. One of the ***Secure Grip*** and ***Release Grip*** are pressed:

   * If we press the other button it deselects the one that was pressed and selects the other one.
   * If we press again the same button it stops the action (sends command `0`).


## Troubleshooting

If you're unable to connect to the Arduino:

1. Confirm the Gripper is properly connected and that it has code which was already flashed to run.
2. Verify that the correct COM port is selected.
3. Ensure no other program is using the serial port (e.g., Arduino IDE).
4. Check that the baud rate (115200) matches the value in your Arduino sketch.
5. Press reset :)


## Vision

The current hardware does not support internet/bluetooth connectivity. If it did, this same interface and functionality could be adapted into a web-based application. This would allow users to control the gripper directly from a smartphone, enabling a more engaging and interactive experience-completely wireless and without needing a computer as an intermediary.

The GUI could directly use an AI object classifier and, though the camera, set the hyper-parameters of the code we flash based on the object (heavy/light, soft-hard).
