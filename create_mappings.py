import json
import os

# Creates a dictionary of pairs that map 4 hex nibbles (2 bytes) to a single unicode character
def create_encode_dict(random=False, filename='hex_to_unicode'):
    if random==False: #default mappings
        # Create a dictionary to hold the mappings
        hex_to_unicode = {}

        # Generate mappings for 0000 to FFFF
        for i in range(0x10000):  # 0x10000 is 65536 in decimal, covering 0000 to FFFF
            hex_key = f"{i:04X}"  # Format as 4-digit hex
            if 0xD800 <= i <= 0xDFFF:
                continue  # Skip surrogate characters

            # Map hex bytes to Unicode characters starting from U+0020
            unicode_char = chr(i + 0x0020) if i < 0x0020 else chr(i)  # Shift for 0000 to 001F

            hex_to_unicode[hex_key] = unicode_char

        # Save the dictionary to a text file
        with open(os.path.join("mappings/default",f'{filename}.json'), 'w', encoding='utf-8') as f:
            json.dump(hex_to_unicode, f, ensure_ascii=False, indent=4)
        print(f"Mapping saved to '{filename}.json'")
        create_decode_dict()
    #else: # If we are creating random mappings.

def create_decode_dict(filepath=os.path.join("mappings/default",f'hex_to_unicode.json')):
    # Read the JSON file with the appropriate encoding
    try:
        with open(f'{filepath}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

    # Swap keys and values
    swapped_data = {key: value for value, key in data.items()}

    if os.path.splitext(os.path.basename(filepath))[0] == 'hex_to_unicode':
        decode_table_filename = os.path.join("mappings/default", 'unicode_to_hex.json')
    else:
        decode_table_filename = os.path.join("mappings", f'DECODE_{os.path.splitext(os.path.basename(filepath))[0]}.json')
    # Write the swapped data to a new JSON file with UTF-8 encoding
    with open(f'{decode_table_filename}.json', 'w', encoding='utf-8') as file:
        json.dump(swapped_data, file, indent=4, ensure_ascii=False)

    print(f"{os.path.splitext(os.path.basename(filepath))[0]} Decode table successfully created under {decode_table_filename}.json")