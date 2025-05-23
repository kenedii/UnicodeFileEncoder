import customtkinter as ctk
from tkinter import filedialog
import create_mappings
import encode_file
import os

# Check if the default mappings exist and create them if not
if not os.path.exists("mappings\\default\\hex_to_unicode.json"): 
    create_mappings.create_encode_dict()  # Create encode + decode mapping dicts

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Initialize the Tkinter root
root = ctk.CTk()
root.title("Unicode Encoder/Decoder")
root.geometry("800x600")

# Functions to handle file selection and updating UI
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select File")
    file_entry.configure(state='normal')
    file_entry.delete(0, ctk.END)
    file_entry.insert(0, file_path)
    file_entry.configure(state='disabled')

def select_map_file():
    global map_file_path
    map_file_path = filedialog.askopenfilename(title="Select Map File")
    map_file_entry.configure(state='normal')
    map_file_entry.delete(0, ctk.END)
    map_file_entry.insert(0, map_file_path)
    map_file_entry.configure(state='disabled')

def update_ui():
    if var_encode.get() == 1:
        map_label.configure(text="Encode Map File:")
        action_button.configure(text="Encode")
    else:
        map_label.configure(text="Decode Map File:")
        action_button.configure(text="Decode")

def toggle_default_map():
    global map_file_path
    if use_default_var.get() == 1:  # Checkbox is checked
        map_file_entry.configure(state='disabled')
        map_file_button.configure(state='disabled')
        if var_encode.get() == 1:
            map_file_path = os.path.join("mappings", "default", "hex_to_unicode.json")  # Use default mapping
        else:
            map_file_path = os.path.join("mappings", "default", "unicode_to_hex.json")  # Use default mapping
    else:
        map_file_entry.configure(state='normal')
        map_file_button.configure(state='normal')

def encode_decode_file():
    if var_encode.get() == 1:  # Encode
        print(f'{file_path} {map_file_path}')
        encode_file.encode_file(file_path, map_file_path)
    else:  # Decode
        print(f'{file_path} {map_file_path}')
        encode_file.decode_file(file_path, map_file_path)

# Title label
title_label = ctk.CTkLabel(root, text="Unicode File Encoder/Decoder", font=("Arial", 20))
title_label.pack(pady=20)

# File selection
file_label = ctk.CTkLabel(root, text="Select file:")
file_label.pack(pady=10)

file_frame = ctk.CTkFrame(root)
file_frame.pack(pady=5)

file_entry = ctk.CTkEntry(file_frame, width=400)
file_entry.pack(side='left', padx=10)

file_button = ctk.CTkButton(file_frame, text="Browse", command=select_file)
file_button.pack(side='left')

# Encode/Decode checkboxes
var_encode = ctk.IntVar(value=1)  # Default to encode

encode_checkbox = ctk.CTkRadioButton(root, text="Encode", variable=var_encode, value=1, command=update_ui)
encode_checkbox.pack()

decode_checkbox = ctk.CTkRadioButton(root, text="Decode", variable=var_encode, value=0, command=update_ui)
decode_checkbox.pack()

# Encode/Decode map file
map_label = ctk.CTkLabel(root, text="Encode Map File:")
map_label.pack(pady=10)

map_file_frame = ctk.CTkFrame(root)
map_file_frame.pack(pady=5)

map_file_entry = ctk.CTkEntry(map_file_frame, width=400)
map_file_entry.pack(side='left', padx=10)

map_file_button = ctk.CTkButton(map_file_frame, text="Browse", command=select_map_file)
map_file_button.pack(side='left')

# Use Default checkbox
use_default_var = ctk.IntVar(value=0)  # Default is unchecked
use_default_checkbox = ctk.CTkCheckBox(root, text="Use Default", variable=use_default_var, command=toggle_default_map)
use_default_checkbox.pack(pady=10)

# Frame for # of Loops and action button
loops_frame = ctk.CTkFrame(root)
loops_frame.pack(pady=10)

# "# of Loops" text to the left of the dropdown menu
loops_label = ctk.CTkLabel(loops_frame, text="# of Loops:")
loops_label.pack(side='left', padx=10)

loop_values = [str(i) for i in range(1, 11)]
loops_dropdown = ctk.CTkComboBox(loops_frame, values=loop_values)
loops_dropdown.set("1")
loops_dropdown.pack(side='left', padx=10)

# Encode/Decode action button
action_button = ctk.CTkButton(root, text="Encode", command=encode_decode_file)  # Encode/Decode logic
action_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
