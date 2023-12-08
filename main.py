from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys

from ui import UI

def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()