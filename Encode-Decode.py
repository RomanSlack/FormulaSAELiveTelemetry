import cantools
from pprint import pprint
import can

# Load the DBC file
db = cantools.database.load_file('motohawk.dbc')

# Retrieve the CAN message by frame ID
example_message = db.get_message_by_frame_id(496)  # Alternatively, use db.get_message_by_name("ExampleMessage")

# Print the type and signal structure of the message
print(type(example_message))
pprint(example_message.signals)

# Create an arbitrary CAN message with specified signal values
data = example_message.encode({'Temperature': 250, 'AverageRadius': 4, 'Enable': 1})
print("Encoded Data:", data)

# Create a CAN message object
message = can.Message(arbitration_id=example_message.frame_id, data=data)
print("Message Data:", message.data)

# Decode the CAN message using the database
decoded_data = db.decode_message(message.arbitration_id, message.data)
print("Decoded Data:", decoded_data)

# Write the CAN data to a binary file
with open('test.bin', "wb") as f:
    f.write(message.data)

# Read the raw CAN data from the binary file and decode it
with open('test.bin', "rb") as f:
    m = f.read()
    
decoded_from_file = db.decode_message(message.arbitration_id, m)
print("Decoded Data from File:", decoded_from_file)

# Output the CAN message ID and data
print("Message Arbitration ID:", message.arbitration_id)
print("Message Data in Bytes:", message.data)

# TODO: Convert bytearray to an array of hexadecimal values
# Example: message.data equivalent => [0xd0, 0xc8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
hex_data = [hex(byte) for byte in message.data]
print("Hexadecimal Data:", hex_data)
