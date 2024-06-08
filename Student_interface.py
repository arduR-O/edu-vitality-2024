import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage

# Function to send a message
def send_message():
    message = entry.get()
    if message:
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {message}\n")
        chat_box.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

# Function to create a gradient
def create_gradient(canvas, width, height, color1, color2):
    limit = width if width > height else height
    (r1, g1, b1) = canvas.winfo_rgb(color1)
    (r2, g2, b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        canvas.create_line(i, 0, i, height, fill=color)

def close_window():
    root.destroy()

# Main application window
root = tk.Tk()
root.title("Chat Application")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to fit the screen
#root.geometry("1200x800+0+0")
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Configure the grid layout
live_stream = root.columnconfigure(0, weight=20)  
chat_window = root.columnconfigure(1, weight=1)
root.rowconfigure(0,weight=1)


# Create a canvas for the gradient background
gradient_canvas = tk.Canvas(root, width=screen_width, height=screen_height)
gradient_canvas.grid(row=0, column=0, columnspan=2, rowspan=1, sticky='nsew')
create_gradient(gradient_canvas, screen_width, screen_height, '#1A1919', '#5A5656')

#Frame big
frame_big = tk.Frame(root,bg = "lightblue",height = 1090,width=1395)
frame_big.place(x=0,y=0)
frame_big.grid(row=0,column=0)

  
#Frame for teacher's screen
frame_teacher = tk.Frame(root,bg = "white",height=600,width=700)
frame_teacher.grid(row = 0,column=0)
text_label0 = tk.Label(frame_teacher,text="Teacher's screen", font=("Arial", 12), bg="black", fg="white")
text_label0.pack_propagate(0)
text_label0.pack(padx=2,pady=2)


# Load the image file
image = PhotoImage(file=".\\Teacher.png")  

# Create a label with the image
image_label = tk.Label(frame_teacher, image=image)
image_label.pack()



#Frame for questions from teacher
frame_top = tk.Frame(root,bg="lightgrey",height = 500)
frame_top.grid(row = 0,column = 1,padx =10,sticky = 'nsew')

# Add text to the frame
text_label = tk.Label(frame_top, text=" Questions ", font=("Arial", 12), bg="black", fg="white")
text_label.pack(padx=20, pady=20)



# Frame for chat box and entry
frame = tk.Frame(root,bg="#1A1919",height = 500)
frame.grid(row=0, column=1, padx=10, pady=300,sticky = 'nsew')
#frame.place(x=1350,y=400)
# Add text to the frame
text_label1 = tk.Label(frame, text="Chat Window", font=("Arial", 12), bg="black", fg="white")
text_label1.pack(padx=20, pady=20)



# ScrolledText widget for chat box
chat_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20,bg="#1A1919",fg = "#F9F4F4")
chat_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



# Entry widget for message input
entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
entry.bind("<Return>", lambda event: send_message())

# Send button
send_button = tk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

frame_bottom = tk.Frame(root,bg="#1A1919")
frame_bottom.grid(row=0, column=1, padx=10, pady=200)

# Add an exit button
exit_button = tk.Button(frame, text="Leave class",bg = "red",fg = "black", command=close_window)
exit_button.pack(pady = 10)



# Run the application
root.mainloop()
