from debugging import console, DEBUG as DEBUG, LOG_LEVEL as LOG_LEVEL
import sys
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
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
        empty_message.setStyleSheet(DEBUG_FILL_STYLE)
        empty_layout.addWidget(empty_message)

        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnPushButtton(QPushButton):
    def __init__(self, key:str = "", text:str = "", path:str = ""):
        super().__init__(text)
        self.path=path
        self.setStyleSheet("border: 0px;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        key_frame = QLabel(key)
        key_frame.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        key_frame.setStyleSheet(EMPTY_FILL_STYLE)
        if DEBUG:
            key_frame.setStyleSheet(DEBUG_FILL_STYLE)
        layout.addWidget(key_frame)

        text_frame = QLabel(text)
        text_frame.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        text_frame.setStyleSheet(EMPTY_FILL_STYLE)
        if DEBUG:
            text_frame.setStyleSheet(DEBUG_FILL_STYLE)

        layout.addWidget(text_frame)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workbench")
        self.setMinimumSize(256, 256)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # setup the screen layout
        window_layout = QVBoxLayout(central_widget)
        window_layout.setContentsMargins(2, 2, 2, 2)
        window_layout.setSpacing(2)

        
        button = D4mnPushButtton("1", "Untitled button")
        window_layout.addWidget(button)


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
