import json
import os

# Creates a dictionary of pairs that map 4 hex nibbles (2 bytes) to a single unicode character
def create_encode_dict(random=False, filename='hex_to_unicode'):
    if random == False:  # default mappings
        # Create the directory if it doesn't exist
        output_dir = os.path.join("mappings", "default")
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Create a dictionary to hold the mappings
        hex_to_unicode = {}

        # Generate mappings for 0000 to FFFF
        for i in range(0x10000):  # 0x10000 is 65536 in decimal, covering 0000 to FFFF
            hex_key = f"{i:04X}"  # Format as 4-digit hex
            if 0xD800 <= i+ 0x0020 <= 0xDFFF:
                continue  # Skip surrogate characters

            # Map hex bytes to Unicode characters starting from U+0020, but hex '0000' starts at ' '
            unicode_char = chr(i + 0x0020)  # Map and 0000 to U+0020

            hex_to_unicode[hex_key] = unicode_char

        # Save the dictionary to a text file
        with open(os.path.join(output_dir, f'{filename}.json'), 'w', encoding='utf-8') as f:
            json.dump(hex_to_unicode, f, ensure_ascii=False, indent=4)
        print(f"Mapping saved to '{filename}.json'")

        # Also create the corresponding decode dictionary
        create_decode_dict()
    #else: # If we are creating random mappings.

def create_decode_dict(filepath=os.path.join("mappings", "default", 'hex_to_unicode.json')):
    # Read the JSON file with the appropriate encoding
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Swap keys and values
    swapped_data = {key: value for value, key in data.items()}

    if os.path.splitext(os.path.basename(filepath))[0] == 'hex_to_unicode':
        decode_table_filename = os.path.join("mappings", "default", 'unicode_to_hex.json')
    else:
        decode_table_filename = os.path.join("mappings", f'DECODE_{os.path.splitext(os.path.basename(filepath))[0]}.json')
    
    # Write the swapped data to a new JSON file with UTF-8 encoding
    with open(decode_table_filename, 'w', encoding='utf-8') as file:
        json.dump(swapped_data, file, indent=4, ensure_ascii=False)

    print(f"Decode table successfully created at {decode_table_filename}")
