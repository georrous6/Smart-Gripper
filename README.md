# Smart-Gripper

**Smart Gripper** is a robotics project developed for the EESTech Challenge Final Round 2025, where it proudly secured **3rd place**. The system utilizes an Infineon motor controller (IFX007T Shield 2Go), an angle sensor (TLE5012B E1000), and a 3D magnetic sensor to provide intelligent, material-aware gripping functionality.

---

## 🚀 How It Works

The Smart Gripper controls the force applied to objects using a **PID controller** with parameters:

- `kp = 1`
- `ki = 0`
- `kd = 0`

### Core Mechanism:

1. A **BLDC motor** drives the gripper to close.
2. Two 3D magnetic sensors at the gripper’s edges detect magnetic field changes when pressure is applied.
3. The **magnitude of the magnetic field** is proportional to the force on the object.
4. The magnetic field serves as **feedback** for the PID controller.
5. The **target force** is dynamically set based on the material identified by the onboard camera.

### Supported Materials & Thresholds:

| Material | Threshold (Magnetic Field Magnitude) |
|----------|--------------------------------------|
| Balloon  | 0.8                                  |
| Wood     | 3.0                                  |
| Iron     | 10.0                                 |

---

### Project Structure Overview

- `src/`
Contains the core implementation code that is deployed to and executed on the Gripper.

- `camera/`
Contains the source code of the camera for material classification.

- `test/`
Contains a simple code for testing communication of the gui with the arduino via serial port.

- `docs/`
Contains the topic and challenge introduction slides


---

## 🛠 Prerequisites

- **Python 3.6+**
- **Arduino IDE**

---

## 🔧 Setup Instructions

### 1. Install XMC for Arduino

Follow the instructions from the official [XMC for Arduino documentation](https://xmc-arduino.readthedocs.io/en/latest/installation-instructions.html) and make sure to use the **alternative installation link** provided [here](https://github.com/LinjingZhang/XMC-for-Arduino/releases/download/V3.5.3-beta/package_infineon_index.json).


### 2. Install Required Arduino Libraries

Search and install the following libraries using the Arduino Library Manager:

- **XENSIV™ Angle Sensor TLx5012B**  
  *(Used for reading motor position via diametrically magnetized magnets)*  
  [Sensor Info](https://www.infineon.com/cms/de/product/sensor/magnetic-sensors/magnetic-position-sensors/angle-sensors/tle5012b-e1000/)

- **XENSIV™ 3D Magnetic Sensor TLx493D**  
  *(Used to measure magnetic field changes in X, Y, and Z directions)*  
  [Sensor Info](https://www.infineon.com/cms/en/product/sensor/magnetic-sensors/magnetic-position-sensors/3d-magnetics/tle493d-a2b6/)

- **Simple FOC Library**  
  *(For Field Oriented Control of BLDC motors)*  
  [Library Docs](https://docs.simplefoc.com)

---

## 🧰 Installation

```bash
git clone git@github.com:georrous6/Smart-Gripper.git
cd Smart-Gripper
pip install -r requirements.txt
```

## ⚙️ Running the Project

### 1. Flash Gripper Firmware
- Open `src/torque_control/` in Arduino IDE 
- Select the board (*XMC4700 Relax Kit*) 
- Select the correct serial port
- Upload the sketch.

### 2. Flash Test Code (Optional)
- Open `test/` in Arduino IDE 
- Select the board (*XMC1100 XMC2Go*) 
- Select the correct serial port
- Upload the sketch.

### 3. Run the GUI Application

1. Launch the GUI application:
```bash
python main.py
```
2. Select the appropriate COM port from the dropdown menu.
3. Click **Connect** to establish a connection.
4. Use the camera to determine the type of object to grab.
5. Use the control buttons:

   - **Secure Grip** – Grabs an object (command `1`)
   - **Release Grip** – Opens the gripper (command `2`)
   - **Emergency Stop** – Immediately halts all movement (command `0`)
6. Manually adjust the pressure applied to the grabbed object using the slider.

#### Button behaviour:
- Pressing the opposite button switches the action.
- Pressing the same button again will stop the action (command: `0`).

## Troubleshooting

If you're unable to connect to the Arduino:

1. Confirm the Gripper is properly connected and that it has code which was already flashed to run.
2. Verify that the correct COM port is selected.
3. Ensure no other program is using the serial port (e.g., Arduino IDE).
4. Check that the baud rate (115200) matches the value in your Arduino sketch.
5. Press reset :)
    
