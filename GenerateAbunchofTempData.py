import cantools
import can
import random

# Load the DBC file
db = cantools.database.load_file('motohawk.dbc')

# Retrieve the CAN message by frame ID
example_message = db.get_message_by_frame_id(496)  # Alternatively, use db.get_message_by_name("ExampleMessage")

# Define a temperature range within the original bounds (229.52 to 270.47)
temperature_values = [229.52 + i * 2 for i in range(20) if 229.52 + i * 2 <= 270.47]

# Shuffle the list to randomize the order
random.shuffle(temperature_values)

# File to store the generated hex data
output_file = 'can_hex_messages.txt'

# Open the file for writing
with open(output_file, "w") as f:
    # Loop over the range of temperatures
    for temp in temperature_values:
        # Create CAN message data with specified temperature
        data = example_message.encode({'Temperature': temp, 'AverageRadius': 4, 'Enable': 1})
        
        # Convert data to hexadecimal format
        hex_data = [hex(byte) for byte in data]
        
        # Write the hexadecimal string to file
        hex_string = ", ".join(hex_data)
        f.write(f"[{hex_string}]\n")
        
        # Print to console for verification
        print(f"Temperature {temp}K: [{hex_string}]")

print(f"\nHexadecimal CAN messages saved to {output_file}.")
