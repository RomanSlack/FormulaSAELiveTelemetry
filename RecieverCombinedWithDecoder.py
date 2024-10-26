import cantools
import serial
import time
import re
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

# Load the DBC file and set up the CAN message
db = cantools.database.load_file('motohawk.dbc')
example_message = db.get_message_by_frame_id(496)  # Message for temperature decoding

# Initialize serial connection (adjust port as needed)
ser = serial.Serial('COM8', 115200, timeout=1)
time.sleep(2)

# Initialize deque for storing recent temperature values
temperature_data = deque(maxlen=50)  # Store the last 50 temperature readings

# Tkinter setup
root = tk.Tk()
root.title("Real-Time Temperature Monitor")

# Matplotlib Figure setup
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
line, = ax.plot([], [], 'r-')
ax.set_xlim(0, 50)  # Display up to 50 readings
ax.set_ylim(200, 300)  # Set y-axis range for temperature in °C
ax.set_xlabel("Reading #")
ax.set_ylabel("Temperature (°C)")
ax.grid(True)  # Add a grid for clarity

# Canvas setup for integrating Matplotlib with Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

def decode_temperature(hex_data):
    # Convert hex array to bytearray
    data = bytearray(hex_data)
    
    # Decode the CAN data using cantools
    decoded_data = db.decode_message(example_message.frame_id, data)
    
    # Extract temperature value
    temperature = decoded_data.get('Temperature', 'N/A')
    if temperature != 'N/A':
        temperature_data.append(temperature)  # Add new temperature to the deque
        update_graph()
    return temperature

def update_graph():
    # Update the line plot with the latest temperature data
    line.set_data(range(len(temperature_data)), list(temperature_data))
    
    # Adjust x-axis dynamically based on data length
    ax.set_xlim(0, max(50, len(temperature_data)))
    canvas.draw_idle()  # Efficiently update the canvas

def read_serial():
    if ser.in_waiting > 0:
        received_data = ser.readline().decode('utf-8').strip()
        print(f"Received: {received_data}")

        # Extract hex data using regex
        hex_matches = re.findall(r"'0x[0-9a-fA-F]+'", received_data)
        hex_data = [int(hx.strip("'"), 16) for hx in hex_matches]

        # Decode the temperature if valid hex data was found
        if hex_data:
            decode_temperature(hex_data)

    # Schedule the next serial read
    root.after(100, read_serial)

# Start reading serial data
root.after(100, read_serial)
root.mainloop()
