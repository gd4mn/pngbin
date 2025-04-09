from debugging import console, DEBUG as DEBUG, LOG_LEVEL as LOG_LEVEL
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from PySide6 import QtCore
from rich.traceback import install

DEBUG_FILL_STYLE = "background-color: rgba(255, 0, 255, 0.2);"
EMPTY_FILL_STYLE = """
    background-color: rgb(255, 0, 255); 
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: bold;
"""


class EmptyFrame(QWidget):
    def __init__(self, message: str = "", width: int = 0, height: int = 0):
        super().__init__()

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        empty_layout = QVBoxLayout()
        self.setLayout(empty_layout)

        empty_message = QLabel(message)
        empty_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_message.setStyleSheet(EMPTY_FILL_STYLE)
        empty_layout.addWidget(empty_message)

        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.Well_1 = QLabel("Well 1")
        self.Well_2 = QLabel("Well 2")

        self.addPermanentWidget(self.Well_1)
        self.addPermanentWidget(self.Well_2)
    
    def set_message(self, message: str):
        self.showMessage(message)
    
    def set_well_1(self, message: str):
        self.Well_1.setText(message)

    def set_well_2(self, message: str):
        self.Well_2.setText(message)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workbench")
        self.setMinimumSize(800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # setup the screen layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        main_layout.addWidget(EmptyFrame("Canvas Area"))
        main_layout.addWidget(EmptyFrame("Work Area", width=256))

        # setup the status bar
        status_bar = D4mnStatusBar()
        self.setStatusBar(status_bar)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    console.info("Starting application ...")
    app.exec()
    console.info("Exiting application ...")

    sys.exit(0)


if __name__ == "__main__":
    main()
