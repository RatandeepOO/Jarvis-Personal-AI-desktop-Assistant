import pyautogui
import time
import subprocess, os
import tkinter as tk
from tkinter import messagebox

def send_desktop_message(recipient_name, message):
    try:
        # Open WhatsApp Desktop (adjust the path based on your system)
        os.startfile("C:\\Users\\arora\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
        time.sleep(5)  # Wait for the app to open
        
        # Focus on the search bar and type the recipient's name
        pyautogui.hotkey('ctrl', 'f')  # Shortcut to open search
        time.sleep(1)
        pyautogui.typewrite(recipient_name, interval=0.1)
        time.sleep(2)
        
        # Press Enter to select the chat
        pyautogui.press('down')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        # Type the message
        pyautogui.typewrite(message, interval=0.1)
        time.sleep(1)
        
        # Send the message
        pyautogui.press('enter')
        messagebox.showinfo("Success", f"Message sent successfully to {recipient_name}!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("WhatsApp Message Sender")

# Set the window size
root.geometry("400x250")

# Add a label and entry for the recipient's name
label_name = tk.Label(root, text="Recipient's Name:")
label_name.pack(pady=10)

entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

# Add a label and entry for the message
label_message = tk.Label(root, text="Message:")
label_message.pack(pady=10)

entry_message = tk.Entry(root, width=30)
entry_message.pack(pady=5)

# Function to handle button click
def on_send_click():
    recipient_name = entry_name.get()
    message = entry_message.get()
    if recipient_name and message:
        send_desktop_message(recipient_name, message)
    else:
        messagebox.showwarning("Input Error", "Please fill in both fields.")

# Add a send button
send_button = tk.Button(root, text="Send Message", command=on_send_click)
send_button.pack(pady=20)

# Run the main loop
root.mainloop()
