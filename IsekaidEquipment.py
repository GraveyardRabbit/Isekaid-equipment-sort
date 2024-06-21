import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from collections import Counter
import os

# Define color variables
BACKGROUND_COLOR = "#21232a"
BUTTON_COLOR = "#7b8a93"
PROCESS_BUTTON_COLOR = "#7b8a93"
TEXT_COLOR = "white"

# Define the process_stats function
def process_stats(stats):
    if not isinstance(stats, str):
        return "N/A"  # Handle missing or non-string values
    
    stats_list = stats.split(', ')
    counter = Counter(stats_list)
    
    # Check if all counts are the same
    counts = list(counter.values())
    if len(set(counts)) == 1 and len(counter) == 1:
        most_common_stat = list(counter.keys())[0].split(':')[0]
        return f"pure {most_common_stat}"
    
    # Check if all stat names are different
    if len(counter) == len(stats_list):
        all_counts_sorted = sorted(counts, reverse=True)
        return f"{'/'.join(map(str, all_counts_sorted))} mixed"
    
    # Find the highest count
    highest_count = max(counter.values())
    
    # Find all stats with the highest count
    most_common_stats = [stat.split(':')[0] for stat, count in counter.items() if count == highest_count]
    
    # Extract all counts, including the highest ones
    all_counts = [count for stat, count in counter.items()]
    all_counts_sorted = sorted(all_counts, reverse=True)

    # Convert "attack" to "strength" if needed
    most_common_stats = [stat if stat != "attack" else "strength" for stat in most_common_stats]
    
    # Join the counts with '/' and append the most common stats
    result = f"{'/'.join(map(str, all_counts_sorted))} {', '.join(most_common_stats)}"
    
    return result

# Helper function to read and rename DataFrame columns
def read_and_rename_csv(file_path):
    df = pd.read_csv(file_path, index_col=[0, 1])
    df_reset = df.reset_index()

    # Rename columns
    df_renamed_all = df_reset.rename(columns={
        'level_0': 'userid',
        'level_1': 'name',
        'userid': 'rarity',
        'name': 'rank',            
        'rarity': 'stats',
        'rank': 'id',
        'stats': 'attack_power',
        'id': 'level',
        'attack_power': 'favorite',
        'level': 'enchanted',
        'favorite': 'seed'
    })

    # Apply the function to the stats column
    df_renamed_all['processed stats'] = df_renamed_all['stats'].apply(process_stats)
    return df_renamed_all

# Define the function to process the DataFrame and save it to a new file
def process_and_save():
    file_path = selected_file_path.get()
    output_folder = selected_output_folder_path.get()
    
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected")
        return
    
    try:
        df_renamed_all = read_and_rename_csv(file_path)

        # Save the updated DataFrame back to a CSV with the result in a new column
        output_file = os.path.join(output_folder, 'equipment stats full.csv')
        df_renamed_all.to_csv(output_file, index=False)

        # Display success message
        messagebox.showinfo("Success", f"New full CSV file has been saved to {output_file}")

    except Exception as e:
        # Display error message
        messagebox.showerror("Error", str(e))

# Define the function to process the DataFrame and save a simplified version to a new file
def process_simple():
    file_path = selected_file_path.get()
    output_folder = selected_output_folder_path.get()
    
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected")
        return
    
    try:
        df_renamed_all = read_and_rename_csv(file_path)

        # Select the relevant columns
        df_simple = df_renamed_all[['rarity', 'rank', 'name', 'stats', 'processed stats', 'id']]

        # Save the updated DataFrame back to a CSV with the result in a new column
        output_file = os.path.join(output_folder, 'equipment stats minimal.csv')
        df_simple.to_csv(output_file, index=False)

        # Display success message
        messagebox.showinfo("Success", f"New minimal CSV file has been saved to {output_file}")

    except Exception as e:
        # Display error message
        messagebox.showerror("Error", str(e))

# Define the function to open the file dialog and select a file
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if file_path:
        selected_file_path.set(file_path)
        file_label.config(text=file_path)
        update_process_button_state()

# Define the function to open the directory dialog and select an output folder
def select_output_folder():
    folder_path = filedialog.askdirectory(
        title="Select an Output Folder"
    )
    if folder_path:
        selected_output_folder_path.set(folder_path)
        output_folder_label.config(text=folder_path)
        update_process_button_state()

# Define the function to update the state of the process buttons
def update_process_button_state():
    if selected_file_path.get() and selected_output_folder_path.get():
        process_button.config(state=tk.NORMAL)
        process_simple_button.config(state=tk.NORMAL)
    else:
        process_button.config(state=tk.DISABLED)
        process_simple_button.config(state=tk.DISABLED)

# Create the main application window
root = tk.Tk()

# Set the title of the window
root.title("Isekaid Equipment Line Sorter")

# Set the size of the window
root.geometry("400x180")

# Set background color for the window
root.configure(bg=BACKGROUND_COLOR)  # Light gray background

# Create a StringVar to store the selected file path
selected_file_path = tk.StringVar()

# Create a StringVar to store the selected output folder path
selected_output_folder_path = tk.StringVar()

# Create a button to select the file
select_button = tk.Button(root, text="Select Your CSV File", command=select_file, bg=BUTTON_COLOR, fg=TEXT_COLOR)
select_button.pack(pady=5)

# Create a label to display the selected file path
file_label = tk.Label(root, textvariable=selected_file_path, wraplength=350, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
file_label.pack(pady=5)

# Create a button to select the output folder
select_output_folder_button = tk.Button(root, text="Select Your Output Folder", command=select_output_folder, bg=BUTTON_COLOR, fg=TEXT_COLOR)
select_output_folder_button.pack(pady=5)

# Create a label to display the selected output folder path
output_folder_label = tk.Label(root, textvariable=selected_output_folder_path, wraplength=350, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
output_folder_label.pack(pady=5)

# Create a frame to hold the process buttons
process_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
process_frame.pack(pady=10)

# Create a button that says "Process Full" and calls the process_and_save function when clicked
process_button = tk.Button(process_frame, text="Export all stats", command=process_and_save, state=tk.DISABLED, bg=PROCESS_BUTTON_COLOR, fg=TEXT_COLOR)
process_button.pack(side=tk.LEFT, padx=5)

# Create a button that says "Process Simple" and calls the process_simple function when clicked
process_simple_button = tk.Button(process_frame, text="Export stats minimal", command=process_simple, state=tk.DISABLED, bg=PROCESS_BUTTON_COLOR, fg=TEXT_COLOR)
process_simple_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()