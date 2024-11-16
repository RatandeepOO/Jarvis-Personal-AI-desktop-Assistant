import tkinter as tk
from tkinter import messagebox
import random

# List of fake hacking commands
commands = [
    "Connecting to the mainframe...",
    "Bypassing firewall...",
    "Decrypting password...",
    "Accessing database...",
    "Downloading files...",
    "Uploading malware...",
    "Scanning for vulnerabilities...",
    "Establishing backdoor access...",
    "Executing payload...",
    "Access granted.",
    "You have been hacked!"
]

# Function to create a black screen
def show_black_screen():
    black_screen = tk.Toplevel()
    black_screen.attributes('-fullscreen', True)
    black_screen.configure(bg='black')
    black_screen.after(10000, black_screen.destroy)  # Close after 10 seconds

# Function to simulate hacking commands
def simulate_hacking(index=0):
    if index < len(commands):
        command = commands[index]
        console.insert(tk.END, command + "\n")
        console.yview(tk.END)  # Scroll to the end
        app.after(1000, simulate_hacking, index + 1)  # Call again after 1 second
    else:
        # Final message
        console.insert(tk.END, "\nSYSTEM ALERT: Your computer has been compromised!\n")
        console.insert(tk.END, "Press CTRL+C to stop all operations!\n")
        # Show pop-up message
        messagebox.showinfo("ALERT", "Your data has been released publicly!")
        show_black_screen()  # Show black screen after pop-up
        app.quit()  # Close the app after showing the black screen

# Function to generate random binary numbers
def binary_effect():
    # Generate a random binary string
    binary_line = ''.join(random.choice(['0', '1']) for _ in range(100))  # 100 characters wide
    
    # Add the binary line to the console
    console.insert(tk.END, binary_line + "\n")
    console.yview(tk.END)  # Scroll to the end

    # Schedule next binary update in 100ms
    app.after(100, binary_effect)

# Function for flash effect
def flash():
    app.configure(bg='white')  # Change background to white
    app.after(100, lambda: app.configure(bg='black'))  # Change back to black after 100ms

# Bind the escape key to the flash function
app = tk.Tk()
app.title("Hacking Simulation")

# Set to full screen
app.attributes('-fullscreen', True)

# Create a text widget for the console
console = tk.Text(app, bg='black', fg='green', font=("Courier New", 12), wrap=tk.NONE)
console.pack(expand=True, fill=tk.BOTH)

# Bind the Esc key to the flash function
app.bind('<Escape>', lambda event: flash())

# Start the binary effect
binary_effect()

# Start the simulation of hacking commands after a short delay
app.after(1000, simulate_hacking)

# Run the application
app.mainloop()
