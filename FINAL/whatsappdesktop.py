import pyautogui
import time
import subprocess

def send_desktop_message(recipient_name, message):
    try:
        # Open WhatsApp Desktop (adjust the path based on your system)
        subprocess.Popen(["C:\\Users\\<YourUsername>\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])
        time.sleep(5)  # Wait for the app to open
        
        # Focus on the search bar and type the recipient's name
        pyautogui.hotkey('ctrl', 'f')  # Shortcut to open search
        time.sleep(1)
        pyautogui.typewrite(recipient_name, interval=0.1)
        time.sleep(2)
        
        # Press Enter to select the chat
        pyautogui.press('enter')
        time.sleep(2)
        
        # Type the message
        pyautogui.typewrite(message, interval=0.1)
        time.sleep(1)
        
        # Send the message
        pyautogui.press('enter')
        print(f"Message sent successfully to {recipient_name}!")
    except Exception as e:
        print(f"An error occurred: {e}")

# User input
name = input("Enter the recipient's name as saved in WhatsApp: ")
message = input("Enter the message to send: ")

# Send the message
send_desktop_message(name, message)
