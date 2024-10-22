import json

# Read the JSON file with the appropriate encoding
try:
    with open('hex_to_unicode.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit()

# Swap keys and values
swapped_data = {key: value for value, key in data.items()}

# Write the swapped data to a new JSON file with UTF-8 encoding
with open('unicode_to_hex.json', 'w', encoding='utf-8') as file:
    json.dump(swapped_data, file, indent=4, ensure_ascii=False)

print("Swapping complete! Check 'unicode_to_hex.json' for the result.")
