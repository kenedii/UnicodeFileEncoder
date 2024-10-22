import json

def create_encode_dict(random=False, filename='hex_to_unicode'):
    if random==False:
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
        with open('{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(hex_to_unicode, f, ensure_ascii=False, indent=4)
        print("Mapping saved to 'hex_to_unicode.json'")

