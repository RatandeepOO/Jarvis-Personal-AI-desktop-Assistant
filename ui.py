import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle("Personal Assistant")
        self.setGeometry(200, 200, 800, 600)  # x, y, width, height

        # Initialize UI
        self.initUI()

        # Set up a timer to change outline color every 300 milliseconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_outline_color)
        self.timer.start(18)  # 300 milliseconds for a slower transition

        # Initialize rainbow colors
        self.rainbow_colors = [
            QColor(255, 0, 0),    # Red
            QColor(255, 127, 0),  # Orange
            QColor(255, 255, 0),  # Yellow
            QColor(0, 255, 0),    # Green
            QColor(0, 0, 255),    # Blue
            QColor(75, 0, 130),   # Indigo
            QColor(148, 0, 211)    # Violet
        ]
        self.current_color_index = 0  # To cycle through the rainbow colors

        # For smoother transition
        self.next_color_index = 1
        self.transition_steps = 100  # Number of steps in color transition
        self.current_step = 0  # Current step of transition

    def initUI(self):
        # Set a sci-fi gradient background color
        gradient = QPalette()
        gradient.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(gradient)

        # Create a label for "Jarvis"
        self.label = QLabel("Jarvis", self)

        # Set the font to Algerian with a larger size
        font = QFont("Algerian", 70)  # Increased font size

        # Apply the font
        self.label.setFont(font)

        # Set the text color to vibrant cyan
        self.label.setStyleSheet("color: cyan; background-color: transparent;")

        # Create a blurred outline using QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setOffset(0, 0)  # No offset, centered shadow
        self.shadow_effect.setBlurRadius(30)  # Increased blur radius for a more pronounced effect
        self.label.setGraphicsEffect(self.shadow_effect)

        # Align the text to the top-center
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Create a central widget for the layout
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(container)

    def change_outline_color(self):
        # Calculate the next color to transition to
        start_color = self.rainbow_colors[self.current_color_index]
        end_color = self.rainbow_colors[self.next_color_index]

        # Interpolate between start and end color
        r = int(start_color.red() + (end_color.red() - start_color.red()) * (self.current_step / self.transition_steps))
        g = int(start_color.green() + (end_color.green() - start_color.green()) * (self.current_step / self.transition_steps))
        b = int(start_color.blue() + (end_color.blue() - start_color.blue()) * (self.current_step / self.transition_steps))

        # Set the shadow color to the interpolated color
        self.shadow_effect.setColor(QColor(r, g, b))

        # Update the current step
        self.current_step += 1

        # Check if we have reached the end of the transition
        if self.current_step >= self.transition_steps:
            # Move to the next color
            self.current_color_index = self.next_color_index
            self.next_color_index = (self.next_color_index + 1) % len(self.rainbow_colors)
            self.current_step = 0  # Reset step for next transition

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
