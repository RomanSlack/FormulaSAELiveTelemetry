import serial
import time


# Set up the serial connection (replace 'COM3' with your CP210x port)
ser = serial.Serial('COM8', 115200, timeout=1)  # Set your COM port and baud rate
time.sleep(2)  # Wait for connection to establish


print("Connected to RYLR998. Waiting for data...")


try:
   while True:
       # Check if data is available
       if ser.in_waiting > 0:
           # Read the incoming data from the RYLR998
           received_data = ser.readline().decode('utf-8').strip()


           # Print the received data to the console
           print(f"Received: {received_data}")


           # Optionally, you could process the data here (e.g., parse or store it)


except KeyboardInterrupt:
   # Close the serial connection on exit
   ser.close()
   print("Connection closed.")