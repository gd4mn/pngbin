DEBUG_FILL_STYLE = ""
from qdbg import DEBUG, DEBUG_FILL_STYLE, LOG_LEVEL, console

import sys
import os
import argparse
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QKeyEvent, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

DEBUG_FILL_STYLE = "background-color: rgba(255, 0, 255, 0.2);"


class D4mnPushButtton(QPushButton):
    button_stylesheet = """
        background-color: #f0f0f0;
        border: 1px solid black; 
        border-radius: 4px;
        font-size: 16px;
        font-weight: bold;
        padding: 4px;
        """
    number_stylesheet = """
        background-color: #66CCFF;
        border: 1px solid black;
        border-radius: 4px;
        font-size: 16px;
        """
    text_stylesheet = """
        border: none;
        font-size: 18px;
        """
    def __init__(self, number: int, text: str):
        super().__init__()
        self.num = number
        self.setStyleSheet(self.button_stylesheet)
        self.setFixedHeight(32)

        button_layout = QHBoxLayout(self)
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(2)

        number_frame = QLabel(str(number))
        number_frame.setStyleSheet(self.number_stylesheet)
        number_frame.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        number_frame.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        number_frame.setFixedWidth(self.fontMetrics().boundingRect("999").width())
        button_layout.addWidget(number_frame)

        text_frame = QLabel(text)
        text_frame.setStyleSheet(self.text_stylesheet)
        text_frame.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        text_frame.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        button_layout.addWidget(text_frame)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setLayout(button_layout)
        self.setEnabled(True)
    
    def keyPressEvent(self, event: QKeyEvent):
       console.info(f"Key pressed: {event.key()}")
       if event.key() == self.num + Qt.Key.Key_0:
           console.info(f"Button {self.num} pressed")
           self.click()

    def mousePressEvent(self, event):
        console.info(f"Mouse pressed: {event.button()}")


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

    def keyPressEvent(self, event: QKeyEvent):
        console.info(f"Key pressed: {event.key()}")


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
