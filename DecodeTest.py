import cantools

# Load the DBC file
db = cantools.database.load_file('motohawk.dbc')
example_message = db.get_message_by_frame_id(496)  # Retrieve message for decoding

# Define raw hexadecimal arrays for testing
hex_data_1 = [0xd0, 0xc8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Encoded for Temperature 266
hex_data_2 = [0xd1, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Encoded for Temperature 230

# Function to convert hex array to byte array and decode it
def decode_temperature(hex_data):
    # Convert hex array to bytearray
    data = bytearray(hex_data)
    
    # Decode the CAN data using cantools
    decoded_data = db.decode_message(example_message.frame_id, data)
    
    # Extract and print temperature
    temperature = decoded_data.get('Temperature', 'N/A')
    print(f"Decoded Temperature: {temperature}°C")
    return temperature

# Decode both temperature values
print("Decoding hex_data_1:")
temperature1 = decode_temperature(hex_data_1)

print("Decoding hex_data_2:")
temperature2 = decode_temperature(hex_data_2)
