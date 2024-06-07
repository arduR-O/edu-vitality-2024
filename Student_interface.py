import tkinter as tk
from tkinter import scrolledtext

# Function to send a message
def send_message():
    message = entry.get()
    if message:
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {message}\n")
        chat_box.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

# Main application window
root = tk.Tk()
root.title("Chat Application")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = "1000"

# Set the window size to fit the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Configure the grid layout
live_stream = root.columnconfigure(0, weight=30)  
chat_window = root.columnconfigure(1, weight=1)  
root.rowconfigure(0, weight=1)

# Frame for chat box and entry
frame = tk.Frame(root)
frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# ScrolledText widget for chat box
chat_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Entry widget for message input
entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
entry.bind("<Return>", lambda event: send_message())

# Send button
send_button = tk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

# Run the application
root.mainloop()
