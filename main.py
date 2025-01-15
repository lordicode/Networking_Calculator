import sys

import regex
from PyQt5 import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel, QLineEdit, QMessageBox)


# noinspection PyUnresolvedReferences
class IPCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Networking Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Adding icon to make the app look more professional
        self.setWindowIcon(QIcon('algebra_icon.png'))

        # This centers the background image
        background = QPixmap('background_texture.jpg')

        # Dividing by 2 gives us the center point of both width and height
        x = (background.width() - self.width()) // 2
        y = (background.height() - self.height()) // 2
        centered_background = background.copy(x, y, self.width(), self.height())

        # Setting up the background
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(centered_background))
        self.setPalette(palette)

        # Create main widget and layout
        main_widget = QWidget()
        main_widget.setStyleSheet("background: rgba(255, 255, 255, 200);")
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tab 1: IP Calculator
        ip_tab = QWidget()
        ip_layout = QVBoxLayout(ip_tab)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP Address (e.g., 192.168.1.0)")
        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Enter Subnet Mask (e.g., 255.255.255.0 or /24)")

        ip_layout.addWidget(QLabel("IP Address:"))
        ip_layout.addWidget(self.ip_input)
        ip_tab.setStyleSheet("background: rgba(255, 255, 255, 200);")
        ip_layout.addWidget(QLabel("Subnet Mask:"))
        ip_layout.addWidget(self.mask_input)

        # Tab 2: Binary Conversion
        binary_tab = QWidget()
        binary_layout = QVBoxLayout(binary_tab)

        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText(
            "Enter binary IP (e.g., 11000000.10101000.00000001.00000000). 32 bits long")
        self.decimal_input = QLineEdit()
        self.decimal_input.setPlaceholderText("Enter decimal IP (e.g., 192.168.1.0)")

        binary_layout.addWidget(QLabel("Binary IP:"))
        binary_layout.addWidget(self.binary_input)
        binary_layout.addWidget(QLabel("Decimal IP:"))
        binary_layout.addWidget(self.decimal_input)
        binary_tab.setStyleSheet("background: rgba(255, 255, 255, 200);")

        # Tab 3: Device Calculator
        device_tab = QWidget()
        device_layout = QVBoxLayout(device_tab)

        self.devices_input = QLineEdit()
        self.devices_input.setPlaceholderText("Enter number of hosts needed")
        device_layout.addWidget(QLabel("Number of hosts:"))
        device_layout.addWidget(self.devices_input)
        device_tab.setStyleSheet("background: rgba(255, 255, 255, 200);")

        # Device calculator button
        device_buttons = QHBoxLayout()
        self.calculate_subnet_btn = QPushButton("Calculate Required Subnet")
        device_buttons.addWidget(self.calculate_subnet_btn)
        device_layout.addLayout(device_buttons)

        # Add tabs
        tabs.addTab(ip_tab, "IP Calculator")
        tabs.addTab(binary_tab, "Binary Conversion")
        tabs.addTab(device_tab, "Hosts to Network Calculator")

        # Buttons for each tab
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
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # Connect signals
        self.calculate_btn.clicked.connect(self.calculate)
        self.to_decimal_btn.clicked.connect(self.binary_to_decimal)
        self.to_binary_btn.clicked.connect(self.decimal_to_binary)
        self.calculate_subnet_btn.clicked.connect(self.calculate_from_devices)
        self.ip_input.textChanged.connect(self.on_ip_input_changed)

    def is_valid_ipv4(self, address):
        """
        Validates the IP address as all other calculations do not matter if the value entered is not allowed.
        An IPv4 address is valid if:
        1. It contains exactly 4 parts separated by dots
        2. Each part is a number between 0 and 255
        3. No empty parts or non-numeric values are allowed
        """
        try:
            parts = address.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except:
            return False

    def is_valid_binary_ipv4(self, address):
        """
        Validates the IP address in binary notation as all other calculations do not matter if the value entered is not allowed.
        An IPv4 address is valid in binary if:
        1. It contains exactly 4 parts separated by dots
        2. Each part is in a set of 01
        3. No empty parts, no symbols outside 01,non-numeric values are allowed
        """
        try:
            parts = address.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                binary_digit = str(part)
                if not set(binary_digit).issubset({'0', '1'}) or len(part) != 8:
                    return False
            return True
        except:
            return False


    def binary_to_decimal(self):
        """
        Convert a dotted-binary IPv4 string with 32 bits
        back into dotted-decimal form (192.168.1.10).

        Logic:
        1. Split the binary address into four 8-bit parts by '.'
        2. Convert each 8-bit part to an integer (base 2)
        3. Convert each integer to a decimal string
        4. Join the four decimal octets with '.'
        """
        binary_ip = self.binary_input.text()
        if self.is_valid_binary_ipv4(binary_ip):
            # Split into four parts, each part is an 8-bit binary number
            parts = binary_ip.split(".")
            decimal_parts = []

            # Convert each part from binary to decimal
            for part in parts:
                number = int(part, 2)  # base 2 means interpret as binary
                decimal_parts.append(str(number))

            # Join the decimal octets to form a dotted-decimal IP
            result = ".".join(decimal_parts)
            self.result_display.setText(result)
        else:
            self.result_display.setText("Invalid binary notation!")


    def decimal_to_binary(self):
        """
        Convert a dotted-decimal IPv4 address ('192.168.1.10')
        into a dotted-binary string.
        Logic:
        1. Split the IP into four octets by '.'
        2. Convert each octet to an integer
        3. Convert the integer to an 8-bit binary string with leading zeros if needed
        4. Join the four binary octets with '.'
        """

        ip_decimal = self.decimal_input.text()
        if self.is_valid_ipv4(ip_decimal):

            # Split the IP address into four octets)
            parts = ip_decimal.split(".")
            binary_parts = []
            # For each octet, convert to int, then to binary, remove '0b', and pad to 8 bits
            for part in parts:
                number = int(part)
                binary_string = bin(number)
                binary_string = binary_string[
                                2:]  # this returns string with 0b at the start, so we proceed to remove the first 2 symbols
                # Pad to 8 bits with leading zeroes
                binary_string = binary_string.zfill(8)
                binary_parts.append(binary_string)
            # Join the four binary octets with dots
            result = ".".join(binary_parts)
            self.result_display.setText(result)
        else:
            self.result_display.setText("Invalid decimal notation!")

    def calculate(self):
        """
        Calculate and display the Network Address, First Usable IP Address,
        Last Usable IP Address, and Broadcast Address based on the input IP
        address and subnet mask.
        """
        ip_v4 = self.ip_input.text().strip()
        subnet_mask = self.mask_input.text().strip()

        # Validate the IPv4 address
        if not self.is_valid_ipv4(ip_v4):
            self.result_display.setText("Invalid IPv4 address!")
            return

        # Validate the subnet mask format (must start with '/')
        if not subnet_mask.startswith('/'):
            self.result_display.setText("Subnet mask must be in CIDR notation (e.g., /24)!")
            return

    def smallest_power_of_2(self, n):
        """
        Serves as a simple iterative way to get the closest higher power of 2 (finds the subnet)
        """
        exponent = 0
        power = 1
        while power < n:
            power *= 2
            exponent += 1
        return power, exponent

    def calculate_from_devices(self):
        """
        Subnet / can be found by finding the lowest power of 2 that can accommodate the entered number of devices
        and subtracting the found power from 32
        """
        # Get the entered number of hosts
        entered_number = int(self.devices_input.text())
        potential_hosts, exponent = self.smallest_power_of_2(entered_number)
        cidr = 32 - exponent
        result = f"The subnet needed is /{cidr}. It can accommodate up to {potential_hosts} potential hosts."
        self.result_display.setText(str(result))

    def on_ip_input_changed(self):
        """
        Serves as a simple visual mechanism, adds a visual flare.
        If the IP address is valid, the background turns light green.
        If invalid, the background turns light red.
        """
        text = self.ip_input.text().strip()
        if self.is_valid_ipv4(text):
            self.ip_input.setStyleSheet("background-color: #b3ffb3;")  # light green
        else:
            self.ip_input.setStyleSheet("background-color: #ffb3b3;")  # light red


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPCalculator()
    window.show()
    sys.exit(app.exec_())
