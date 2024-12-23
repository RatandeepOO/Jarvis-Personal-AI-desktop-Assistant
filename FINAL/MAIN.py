import sys
import test
import pyttsx3
from PyQt5 import QtCore , QtWidgets , QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QPixmap

# Initialize text-to-speech
assistant = pyttsx3.init('sapi5')
voices = assistant.getProperty('voices')
assistant.setProperty('voice', voices[1].id)
assistant.setProperty('rate', 150)

def speak(audio):
    assistant.say(audio)
    print(f": {audio}")
    assistant.runAndWait()

class GifLoaderWorker(QtCore.QThread):
    gif_path_loaded = QtCore.pyqtSignal(str)  # Signal to emit when a GIF path is loaded

    def __init__(self, gif_paths):
        super().__init__()
        self.gif_paths = gif_paths

    def run(self):
        # Emit paths to load GIFs one by one
        for path in self.gif_paths:
            self.gif_path_loaded.emit(path)
            self.msleep(100)  # Simulate a small delay for better visual understanding

class PersonalAssistantUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Personal Assistant")
        self.setGeometry(100, 100, 800, 600)

        # Remove the maximize option
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        # Set background color
        self.setStyleSheet("background-color: black;")

        # Create a label for "Jarvis"
        self.jarvis_label = QtWidgets.QLabel("Jarvis", self)
        self.jarvis_label.setAlignment(QtCore.Qt.AlignCenter)
        self.jarvis_label.setStyleSheet("color: cyan; font: 72px 'Algerian';")
        self.jarvis_label.setGeometry(0, 50, 800, 100)

        # Create start/stop button
        self.start_stop_button = QtWidgets.QPushButton("Start/Stop", self)
        self.start_stop_button.setGeometry(300, 150, 200, 50)  # Positioned above the background label
        self.start_stop_button.setStyleSheet("font: 20px 'Algerian'; color: white; background-color: green;")
        self.start_stop_button.clicked.connect(self.open_loading_window)

    def open_loading_window(self):
        # Close the main window immediately
        self.close()

        # Open the GIF window
        self.gif_window = GifWindow()
        self.gif_window.show()

        # Speak welcome message
        speak("Welcome to the world of automation")

class GifWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Come to the world of automation")
        self.setGeometry(150, 150, 800, 600)

        # Remove the maximize option
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        # Set background color
        self.setStyleSheet("background-color: black;")

        # Create label for the GIF
        self.gif_label = QtWidgets.QLabel(self)
        self.gif_label.setGeometry(0, 0, 800, 600)
        self.gif_label.setAlignment(QtCore.Qt.AlignCenter)

        # Start the asynchronous GIF loading
        gif_paths = ["GIFs\\Start.gif"]  # Replace with your GIF paths
        self.gif_loader = GifLoaderWorker(gif_paths)
        self.gif_loader.gif_path_loaded.connect(self.load_gif)  # Connect to the signal
        self.gif_loader.start()  # Start the worker thread

        # Automatically close the GIF window after 5 seconds and open the next window
        QtCore.QTimer.singleShot(3000, self.open_next_window)

    def load_gif(self, path):
        # Load and display GIF in the main thread
        movie = QtGui.QMovie(path)
        movie.setSpeed(50)  # Adjust GIF speed if necessary
        self.gif_label.setMovie(movie)
        movie.start()

    def open_next_window(self):
        self.close()  # Close the loading GIF window
        self.new_window = NextWindow()  # Open the new window after the GIF window closes
        self.new_window.show()

class NextWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Your existing initialization code...

        # Create an instance of Assistant
        self.assistant_instance = test.Assistant()

        # Start the assistant
        self.assistant_instance.run_assistant()
        # Set window properties (larger window size)
        self.setWindowTitle("Next Window")
        self.setGeometry(0, 0, 2000, 1288)


        # Set background color
        self.setStyleSheet("background-color: black;")

                # Set a QLabel to hold the GIF
        self.gif_label = QtWidgets.QLabel(self)
        self.gif_label.setGeometry(0, 0, 2000, 1288)  # Set label size to fill the window
        
        # Load the GIF
        self.gif_movie = QtGui.QMovie("GIFs\\06.gif")  # Replace with the actual path to your GIF
        self.gif_label.setMovie(self.gif_movie)

        # Start the GIF
        self.gif_movie.start()

        # Create labels for GIFs
        self.gif_label_left = QtWidgets.QLabel(self)
        self.gif_label_center = QtWidgets.QLabel(self)
        self.gif_label_right = QtWidgets.QLabel(self)

        # Create label to display text in the new window
        self.label = QtWidgets.QLabel("Welcome", self)
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.label.setStyleSheet("color: cyan; font: 78px 'Algerian'; background: transparent;")
        self.label.setGeometry(390, 100, 1200, 100)
        
        
        # Start the asynchronous GIF loading
        gif_paths = ["GIFs\\02.gif", "GIFs\\04.gif", "GIFs\\05.gif"]  # Replace with your GIF paths
        self.gif_loader = GifLoaderWorker(gif_paths)
        self.gif_loader.gif_path_loaded.connect(self.load_gif)  # Connect to the signal
        self.gif_loader.start()  # Start the worker thread

    def load_gif(self, path):
        movie = QtGui.QMovie(path)
        if "02.gif" in path:
            self.gif_label_left.setMovie(movie)
            self.gif_label_left.setGeometry(65, 300, 450, 450)   # Left GIF
        elif "04.gif" in path:
            self.gif_label_center.setMovie(movie)
            self.gif_label_center.setGeometry(700, 125, 750, 900)  # Center GIF
        elif "05.gif" in path:
            self.gif_label_right.setMovie(movie)
            self.gif_label_right.setGeometry(1450, 300, 450, 450)  # Right GIF
        movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PersonalAssistantUI()
    window.show()
    sys.exit(app.exec_())
