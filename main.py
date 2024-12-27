import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout)



class IPCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Address Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

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