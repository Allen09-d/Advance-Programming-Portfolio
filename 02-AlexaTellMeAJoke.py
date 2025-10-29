from tkinter import *
import random

def load_jokes(filename): # Load Jokes from txt file
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def show_setup(): # Display Joke Setup
    global current_joke
    current_joke = random.choice(jokes) # Pick a random joke from list
    
    if '?' in current_joke:
        setup, _ = current_joke.split('?', 1)
        joke_label.config(text=setup + '?', fg="#2E86AB")
    else:
        joke_label.config(text=current_joke, fg="#2E86AB")
    
    punchline_button.config(state='normal', bg="#A23B72", fg="white")
    root.config(bg="#F8F4E3")
    tell_button.config(bg="#F18F01")
    quit_button.config(bg="#C73E1D", fg="white")

def show_punchline(): # Display Punchline
    if '?' in current_joke:
        _, punchline = current_joke.split('?', 1)
        joke_label.config(text=joke_label.cget("text") + "\n\n" + punchline.strip(), fg="#C73E1D")
    punchline_button.config(state='disabled', bg="#CCCCCC")
    root.config(bg="#FFF8E8")

def quit_app(): # Exit Application
    root.destroy()

# Load jokes
jokes = load_jokes('randomJokes.txt')
current_joke = ""

# GUI setup
root = Tk()
root.title("Alexa Joke Teller")
root.geometry("600x400")
root.resizable(True, True)
root.minsize(500, 350)
root.config(bg="#F8F4E3")

# Color scheme
colors = {
    "primary": "#2E86AB",      # Blue for setup
    "secondary": "#A23B72",    # Purple for buttons
    "accent": "#F18F01",       # Orange for tell button
    "danger": "#C73E1D",       # Red for quit button
    "punchline": "#C73E1D",    # Red for punchline
    "bg_light": "#F8F4E3",     # Light beige background
    "bg_lighter": "#FFF8E8"    # Lighter beige for punchline
}

# Configure styles
joke_label = Label(root, text="Alexa Tell Me A Joke!", wraplength=500, font=("Arial", 16, "bold"), justify="center", bg=colors["bg_light"], fg=colors["primary"], pady=20)
joke_label.pack(expand=True, fill="both", padx=20, pady=20)

# Button frame for better layout
button_frame = Frame(root, bg=colors["bg_light"])
button_frame.pack(pady=20)

tell_button = Button(button_frame, text="Tell me a Joke", command=show_setup, font=("Arial", 12, "bold"), bg=colors["accent"], fg="white", padx=20, pady=10, relief="raised", bd=3)
tell_button.pack(pady=10)

punchline_button = Button(button_frame, text="Show Punchline", command=show_punchline, state='disabled', font=("Arial", 12, "bold"), bg="#CCCCCC", fg="white", padx=20, pady=10, relief="raised", bd=3)
punchline_button.pack(pady=10)

quit_button = Button(button_frame, text="Quit", command=quit_app, font=("Arial", 12, "bold"), bg=colors["danger"], fg="white", padx=30, pady=10, relief="raised", bd=3)
quit_button.pack(pady=10)

root.mainloop() # Run main event on loop