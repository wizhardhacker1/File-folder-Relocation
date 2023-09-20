import tkinter as tk
from tkinter import filedialog
import shutil
from tkinter import ttk
import os
import threading

def move_with_progress(source, destination, progress_bar):
    try:
        shutil.move(source, destination)
        status_label.config(text="Move completed.")
        progress_bar.stop()
        move_button.config(state=tk.NORMAL)
        browse_source_button.config(state=tk.NORMAL)
        browse_destination_button.config(state=tk.NORMAL)
        source_entry.delete(0, tk.END)
        destination_entry.delete(0, tk.END)
    except Exception as e:
        status_label.config(text=f"Move failed: {str(e)}")

def browse_source_directory():
    source_directory = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_directory)

def browse_destination_directory():
    destination_directory = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_directory)

def move_button_clicked():
    source = source_entry.get()
    destination = destination_entry.get()
    if source and destination:
        move_button.config(state=tk.DISABLED)
        browse_source_button.config(state=tk.DISABLED)
        browse_destination_button.config(state=tk.DISABLED)
        status_label.config(text="Moving... Please wait.")

        progress_bar = ttk.Progressbar(frame, length=200, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Use a separate thread for the move operation to avoid freezing the GUI
        move_thread = threading.Thread(target=move_with_progress, args=(source, destination, progress_bar))
        move_thread.start()
    else:
        status_label.config(text="Please specify both source and destination directories!")

def reset_button_clicked():
    source_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)
    status_label.config(text="")
    move_button.config(state=tk.NORMAL)
    browse_source_button.config(state=tk.NORMAL)
    browse_destination_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Folder Move GUI")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

source_label = tk.Label(frame, text="Source Directory:")
source_label.pack()

source_entry = tk.Entry(frame, width=50)
source_entry.pack()

browse_source_button = tk.Button(frame, text="Browse", command=browse_source_directory)
browse_source_button.pack()

destination_label = tk.Label(frame, text="Destination Directory:")
destination_label.pack()

destination_entry = tk.Entry(frame, width=50)
destination_entry.pack()

browse_destination_button = tk.Button(frame, text="Browse", command=browse_destination_directory)
browse_destination_button.pack()

move_button = tk.Button(frame, text="Move", command=move_button_clicked)
move_button.pack()

reset_button = tk.Button(frame, text="Reset", command=reset_button_clicked)
reset_button.pack()

status_label = tk.Label(frame, text="")
status_label.pack()

root.mainloop()
