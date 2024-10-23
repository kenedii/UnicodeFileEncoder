import json
import os

def get_filename(filepath=""):
    filename = os.path.splitext(os.path.basename(filepath))[0] # Get the file name without file extension
    file_extension = os.path.splitext(filepath)[1] # Get the file extension

    return filename, file_extension

def encode_file(filepath, mapping):
    filename, file_extension = get_filename(filepath) # Retrieve the file name + extension

    # Load the hex to unicode mappings from the JSON file
    with open(f'{mapping}', 'r', encoding='utf-8') as f:
        hex_to_unicode = json.load(f)

    with open(f'{filepath}', 'rb') as f: # Open the file to be encoded
        data = f.read()

    encoded_output = []
    for i in range(0, len(data), 2):
        # Get the next 4 bytes (or less if at the end of the file)
        byte_sequence = data[i:i+2]
        hex_sequence = byte_sequence.hex().upper()  # Convert to hex string
        
        # Find the corresponding unicode character, or use a placeholder if not found
        unicode_char = hex_to_unicode.get(hex_sequence, '?')  # Use '?' if no mapping exists
        
        encoded_output.append(unicode_char)

    # Join the encoded characters into a single string
    encoded_string = ''.join(encoded_output)

    # Write the encoded string to the output file
    with open(f'{filename}_ENCODED{file_extension}', 'w', encoding='utf-8') as f:
        f.write(encoded_string)

    print(f"Encoded output saved to '{filename}_ENCODED{file_extension}'")


# Function to decode a file using the mappings
def decode_file(filepath, mapping):
    filename, file_extension = get_filename(filepath) # Retrieve the file name + extension

    # Load the unicode to hex mappings from the JSON file
    with open(f'{mapping}', 'r', encoding='utf-8') as f:
        unicode_to_hex = json.load(f)

    with open(filepath, 'r', encoding='utf-8') as f:
        encoded_data = f.read()

    decoded_output = bytearray()
    for char in encoded_data:
        hex_sequence = unicode_to_hex.get(char, None)  # Get hex mapping
        if hex_sequence is not None:
            # Convert hex string back to bytes
            decoded_output.extend(bytes.fromhex(hex_sequence))  # Ensure hex is converted back to bytes
        else:
            # If no mapping exists, add a placeholder 
            decoded_output.extend(b'\x00')  # Placeholder for unknown characters
    
    if filename.endswith("_ENCODED"):
        decoded_filename = filename.split("_ENCODED")[0]
    else:
        decoded_filename = filename

    # Write the decoded bytes to the output file
    with open(f'{decoded_filename}{file_extension}', 'wb') as f:
        f.write(decoded_output)

    print(f"Decoded output saved to '{decoded_filename}'")


#input_file_path = 'encoded_output1.txt'  #  input binary file path
#output_file_path = 'encoded_output.txt'  #  output filename
#encode_file(input_file_path, output_file_path)


"""
encoded_file_path = 'encoded_output.txt'  # File to decode
decoded_file_path = 'testcsv.csv'  # Desired output file name for decoded data
decode_file(encoded_file_path, decoded_file_path)
"""