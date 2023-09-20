import os
import tkinter as tk
from tkinter import filedialog
import shutil
from tkinter import ttk
import threading
import datetime

# Set an absolute path for the log file
log_file_path = os.path.join(os.path.expanduser("~"), "move_log.txt")

def log_message(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] {message}\n"

    # Append the log message to the log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)

def move_with_progress(sources, destination, progress_bar, status_label, move_button):
    successful_moves = []
    errors = []

    try:
        total_folders = len(sources)
        progress_step = 100 / total_folders

        for idx, source in enumerate(sources):
            if os.path.isdir(source):
                try:
                    # Copy the source directory to the destination
                    shutil.copytree(source, os.path.join(destination, os.path.basename(source)))

                    # Remove the source directory
                    shutil.rmtree(source)

                    successful_moves.append(source)
                except Exception as e:
                    errors.append(f"Failed to move '{source}' to '{destination}': {str(e)}")
            else:
                errors.append(f"'{source}' is not a directory and was not moved.")

            # Update progress bar
            progress_bar["value"] = (idx + 1) * progress_step

            # Update status label on the main thread
            root.after(10, status_label.config, {"text": f"Moving... {idx + 1}/{total_folders} folders"})

        # Log successful moves
        if successful_moves:
            log_message(f"Successfully moved the following folders to '{destination}':")
            for source in successful_moves:
                log_message(f"- {source}")

        # Log errors
        if errors:
            log_message("Errors encountered during the move:")
            for error in errors:
                log_message(error)

        # Update status label on the main thread
        root.after(10, status_label.config, {"text": "Move completed."})
        progress_bar.stop()

        # Enable the move button on the main thread
        root.after(10, move_button.config, {"state": tk.NORMAL})
    except Exception as e:
        log_message(f"Move failed: {str(e)}")

def browse_source_directory():
    source_directory = filedialog.askdirectory()
    source_listbox.insert(tk.END, source_directory)

def browse_destination_directory():
    destination_directory = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_directory)

def move_button_clicked():
    sources = source_listbox.get(0, tk.END)
    destination = destination_entry.get()
    if sources and destination:
        move_button.config(state=tk.DISABLED)
        browse_source_button.config(state=tk.DISABLED)
        browse_destination_button.config(state=tk.DISABLED)
        status_label.config(text="Moving...")

        progress_bar = ttk.Progressbar(frame, length=200, mode='determinate')
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Use a separate thread for the move operation to avoid freezing the GUI
        move_thread = threading.Thread(target=move_with_progress, args=(sources, destination, progress_bar, status_label, move_button))
        move_thread.start()
    else:
        status_label.config(text="Please specify source and destination directories!")

def reset_button_clicked():
    source_listbox.delete(0, tk.END)
    destination_entry.delete(0, tk.END)
    status_label.config(text="")
    move_button.config(state=tk.NORMAL)
    browse_source_button.config(state=tk.NORMAL)
    browse_destination_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Folder Move GUI")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

source_label = tk.Label(frame, text="Source Directories:")
source_label.pack()

source_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
source_listbox.pack()

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
