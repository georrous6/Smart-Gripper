import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# === Serial config ===
SERIAL_PORT = 'COM3'  # Change this to your port (e.g., 'COM4' or '/dev/ttyUSB0')
BAUD_RATE = 115200

# === Data storage ===
MAX_POINTS = 200
data_x = deque(maxlen=MAX_POINTS)
data_y = deque(maxlen=MAX_POINTS)
data_z = deque(maxlen=MAX_POINTS)

# === Open serial port ===
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Connected to", SERIAL_PORT)

# === Plot setup ===
fig, ax = plt.subplots()
line_x, = ax.plot([], [], label='X')
line_y, = ax.plot([], [], label='Y')
line_z, = ax.plot([], [], label='Z')

ax.set_ylim(-100, 100)  # Adjust based on your sensor's range
ax.set_xlim(0, MAX_POINTS)
ax.set_title('Live Magnetic Field Data')
ax.set_xlabel('Sample')
ax.set_ylabel('Field Value')
ax.grid(True)
ax.legend()

# === Update function ===
def update(frame):
    while ser.in_waiting:
        try:
            line = ser.readline().decode().strip()
            values = list(map(float, line.split(',')))
            if len(values) == 3:
                data_x.append(values[0])
                data_y.append(values[1])
                data_z.append(values[2])
        except:
            pass

    line_x.set_data(range(len(data_x)), data_x)
    line_y.set_data(range(len(data_y)), data_y)
    line_z.set_data(range(len(data_z)), data_z)
    return line_x, line_y, line_z

# === Save plot as PDF on close ===
def on_close(event):
    print("Saving final plot to 'magnetic_field_plot.pdf'...")
    fig2, ax2 = plt.subplots()
    ax2.plot(data_x, label='X')
    ax2.plot(data_y, label='Y')
    ax2.plot(data_z, label='Z')
    ax2.set_title("Final Magnetic Field Data")
    ax2.set_xlabel("Sample")
    ax2.set_ylabel("Field Value")
    ax2.grid(True)
    ax2.legend()
    fig2.savefig("control_data.pdf")
    print("Plot saved.")
    ser.close()

fig.canvas.mpl_connect('close_event', on_close)

# === Run animation ===
ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
