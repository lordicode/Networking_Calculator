import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel, QLineEdit)



class IPCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Address Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Adding icon to make the app look more professional
        self.setWindowIcon(QIcon('algebra_icon.png'))

        # This centers the background image - learned this from my UI design course
        background = QPixmap('background_texture.jpg')

        # Dividing by 2 gives us the center point of both width and height, which is the center of the generated window
        x = (background.width() - self.width()) // 2
        y = (background.height() - self.height()) // 2
        centered_background = background.copy(x, y, self.width(), self.height())

        # Setting up the background
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(centered_background))
        self.setPalette(palette)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs. Task calls for multiple functionalities.
        # To not overcrowd the UI we will be using tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tab 1: IP Calculator
        ip_tab = QWidget()
        ip_layout = QVBoxLayout(ip_tab)

        # IP and Mask inputs
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP Address (e.g., 192.168.1.0)")
        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Enter Subnet Mask (e.g., 255.255.255.0 or /24)")

        ip_layout.addWidget(QLabel("IP Address:"))
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(QLabel("Subnet Mask:"))
        ip_layout.addWidget(self.mask_input)

        # Tab 2: Binary Conversion
        binary_tab = QWidget()
        binary_layout = QVBoxLayout(binary_tab)

        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText("Enter binary IP (e.g., 11000000.10101000.00000001.00000000)")
        self.decimal_input = QLineEdit()
        self.decimal_input.setPlaceholderText("Enter decimal IP (e.g., 192.168.1.0)")

        binary_layout.addWidget(QLabel("Binary IP:"))
        binary_layout.addWidget(self.binary_input)
        binary_layout.addWidget(QLabel("Decimal IP:"))
        binary_layout.addWidget(self.decimal_input)

        # Tab 3: Device Calculator
        device_tab = QWidget()
        device_layout = QVBoxLayout(device_tab)

        self.devices_input = QLineEdit()
        self.devices_input.setPlaceholderText("Enter number of hosts needed")
        device_layout.addWidget(QLabel("Number of hosts:"))
        device_layout.addWidget(self.devices_input)

        # Add tabs
        tabs.addTab(ip_tab, "IP Calculator")
        tabs.addTab(binary_tab, "Binary Conversion")
        tabs.addTab(device_tab, "Hosts to Network Calculator")

        # Buttons for each tab
        # IP Calculator buttons
        ip_buttons = QHBoxLayout()
        self.calculate_btn = QPushButton("Calculate")
        ip_buttons.addWidget(self.calculate_btn)
        ip_layout.addLayout(ip_buttons)

        # Binary conversion buttons
        binary_buttons = QHBoxLayout()
        self.to_decimal_btn = QPushButton("Binary to Decimal")
        self.to_binary_btn = QPushButton("Decimal to Binary")
        binary_buttons.addWidget(self.to_decimal_btn)
        binary_buttons.addWidget(self.to_binary_btn)
        binary_layout.addLayout(binary_buttons)

        # Result display
        self.result_display = QTextEdit()
        # This will only display text, so we set it to be read only
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # Connect signals. This allows the buttons to call certain functions
        self.calculate_btn.clicked.connect(self.calculate)
        self.to_decimal_btn.clicked.connect(self.binary_to_decimal)
        self.to_binary_btn.clicked.connect(self.decimal_to_binary)
        self.ip_input.textChanged.connect(self.validate_ip)

    def validate_ip(self):
        return
    def binary_to_decimal(self):
        return

    def decimal_to_binary(self):
        return

    def calculate(self):
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPCalculator()
    window.show()
    sys.exit(app.exec_())