import cantools
import struct

# Load your DBC file (replace 'your_dbc_file.dbc' with actual DBC file path)
dbc_file_path = 'toyota_rav4_prime.dbc'
db = cantools.database.load_file(dbc_file_path, strict=False)

# Function to generate raw CAN data from signals
def generate_raw_can_data(message_name, signal_data):
    # Get message by name
    message = db.get_message_by_name(message_name)
    
    # Encode signal data
    raw_data = message.encode(signal_data)
    
    # Pack raw data into binary format
    return raw_data

# Example usage - replace 'MessageName' and signals with actual DBC details
message_name = 'ExampleMessage'
signal_data = {
    'ExampleSignal1': 100,  # Replace with actual signal name and value
    'ExampleSignal2': 50,
}

# Generate raw CAN data
raw_can_data = generate_raw_can_data(message_name, signal_data)

# Convert raw CAN data to binary string for testing
binary_data = struct.pack(f'{len(raw_can_data)}B', *raw_can_data)
print(f"Raw CAN data in binary: {binary_data}")
