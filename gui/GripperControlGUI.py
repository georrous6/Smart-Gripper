import customtkinter as ctk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import threading
import time
import subprocess
import os

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GripperControlGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Smart Gripper Control")
        self.window.geometry("600x550")

        self.serial_port = None
        self.is_connected = False
        self.active_button = None

        self.setup_gui()

    def setup_gui(self):
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

        # Title Frame
        title_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(
            title_frame,
            text="Smart Gripper Control",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack()

        # Connection Frame
        conn_frame = ctk.CTkFrame(self.window)
        conn_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        port_label = ctk.CTkLabel(conn_frame, text="Select Port:")
        port_label.pack(side="left", padx=10)

        self.port_var = ctk.StringVar()
        self.port_combo = ctk.CTkOptionMenu(
            conn_frame, variable=self.port_var, values=["No ports available"], width=150
        )
        self.port_combo.pack(side="left", padx=10)

        refresh_btn = ctk.CTkButton(
            conn_frame, text="🔄 Refresh", width=100, command=self.refresh_ports
        )
        refresh_btn.pack(side="left", padx=5)

        self.connect_btn = ctk.CTkButton(
            conn_frame, text="🔌 Connect", width=100, command=self.toggle_connection
        )
        self.connect_btn.pack(side="left", padx=5)

        # Control Frame
        control_frame = ctk.CTkFrame(self.window)
        control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            control_frame,
            text="Gripper Controls",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=10)

        self.grip_btn = ctk.CTkButton(
            control_frame,
            text="🔒 Secure Grip",
            font=ctk.CTkFont(size=16),
            height=60,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=lambda: self.handle_button_press("grip", "1"),
        )
        self.grip_btn.pack(fill="x", padx=20, pady=10)

        self.release_btn = ctk.CTkButton(
            control_frame,
            text="🔓 Release Grip",
            font=ctk.CTkFont(size=16),
            height=60,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=lambda: self.handle_button_press("release", "2"),
        )
        self.release_btn.pack(fill="x", padx=20, pady=10)

        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⚠ EMERGENCY STOP",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#FFA500",
            hover_color="#FF8C00",
            command=self.emergency_stop,
        )
        self.stop_btn.pack(fill="x", padx=20, pady=10)

        # Settings Frame
        settings_frame = ctk.CTkFrame(self.window)
        settings_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        slider_frame = ctk.CTkFrame(settings_frame)
        slider_frame.pack(fill="x", padx=10, pady=10)

        # Weight Slider
        weight_frame = ctk.CTkFrame(slider_frame, fg_color="transparent")
        weight_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(weight_frame, text="Weight (0–500g)").pack()
        self.weight_slider = ctk.CTkSlider(
            weight_frame, from_=0, to=500, number_of_steps=100, orientation="horizontal"
        )
        self.weight_slider.set(250)
        self.weight_slider.pack()

        # Hardness Slider
        hardness_frame = ctk.CTkFrame(slider_frame, fg_color="transparent")
        hardness_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(hardness_frame, text="Hardness (0.0–1.0)").pack()
        self.hardness_slider = ctk.CTkSlider(
            hardness_frame, from_=0, to=1, number_of_steps=100, orientation="horizontal"
        )
        self.hardness_slider.set(0.5)
        self.hardness_slider.pack()

        # Image Button
        image_btn = ctk.CTkButton(
            slider_frame, text="📷 Take Image", width=120, command=self.run_main_py
        )
        image_btn.pack(side="left", padx=(10, 0))

        # Status & Theme
        bottom_frame = ctk.CTkFrame(self.window)
        bottom_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.status_label = ctk.CTkLabel(
            bottom_frame, text="Status: Not Connected", font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        self.theme_switch = ctk.CTkSwitch(
            bottom_frame, text="Dark Mode", command=self.toggle_theme, onvalue="dark", offvalue="light"
        )
        self.theme_switch.pack(side="right", padx=10, pady=5)
        self.theme_switch.select()

        self.refresh_ports()

    def toggle_theme(self):
        ctk.set_appearance_mode(self.theme_switch.get())

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if not ports:
            ports = ["No ports available"]
        self.port_combo.configure(values=ports)
        self.port_combo.set(ports[0])

    def check_port_available(self, port):
        try:
            test_serial = serial.Serial(port, 115200, timeout=1)
            test_serial.close()
            return True
        except Exception:
            return False

    def toggle_connection(self):
        if not self.is_connected:
            try:
                port = self.port_var.get()
                if port == "No ports available":
                    raise Exception("No valid port selected")

                if not self.check_port_available(port):
                    try:
                        temp_serial = serial.Serial(port)
                        temp_serial.close()
                    except:
                        pass
                    time.sleep(1)
                    if not self.check_port_available(port):
                        raise Exception(
                            f"Port {port} is in use by another program."
                        )

                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.is_connected = True
                self.connect_btn.configure(
                    text="🔌 Disconnect", fg_color="#FF5757", hover_color="#FF3333"
                )
                self.status_label.configure(
                    text=f"Status: Connected to {port}", text_color="#4CAF50"
                )
                self.port_combo.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))
        else:
            if self.serial_port:
                self.serial_port.close()
            self.is_connected = False
            self.connect_btn.configure(text="🔌 Connect", fg_color="#3B8ED0")
            self.status_label.configure(
                text="Status: Disconnected", text_color="gray"
            )
            self.port_combo.configure(state="normal")

    def handle_button_press(self, button_name, command):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect to a port first")
            return

        if self.active_button == button_name:
            self.active_button = None
            self.send_command("0")
            self.reset_button_colors()
            self.status_label.configure(text="Status: Stopped")
        else:
            if self.active_button:
                self.send_command("0")
                time.sleep(0.1)
            self.active_button = button_name
            self.send_command(command)
            self.reset_button_colors()

            if button_name == "grip":
                self.grip_btn.configure(fg_color="#FF5757", hover_color="#FF3333")
                self.status_label.configure(text="Status: Securing grip...")
            else:
                self.release_btn.configure(fg_color="#FF5757", hover_color="#FF3333")
                self.status_label.configure(text="Status: Releasing grip...")

    def reset_button_colors(self):
        self.grip_btn.configure(fg_color="#4CAF50", hover_color="#388E3C")
        self.release_btn.configure(fg_color="#4CAF50", hover_color="#388E3C")

    def emergency_stop(self):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect to a port first")
            return

        self.active_button = None
        self.reset_button_colors()
        self.send_command("0")
        self.status_label.configure(text="Status: EMERGENCY STOP", text_color="#FF5757")

    def send_command(self, cmd):
        if not self.is_connected:
            return
        try:
            formatted_cmd = f"T{cmd}\n"
            self.serial_port.write(formatted_cmd.encode())
            self.serial_port.flush()
        except Exception as e:
            messagebox.showerror("Communication Error", str(e))
            self.toggle_connection()

    def run_main_py(self):
        try:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "object_classification", "main.py"))
            subprocess.Popen(["python", script_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run main.py:\n{e}")

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.window.destroy()


if __name__ == "__main__":
    app = GripperControlGUI()
    app.run()
