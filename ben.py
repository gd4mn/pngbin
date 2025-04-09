from debugging import console, DEBUG as DEBUG, LOG_LEVEL as LOG_LEVEL
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
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


class D4mnStatusWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("border-top: 0px;")

        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)

        # message column
        message_column = QWidget()
        message_column.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        message_layout = QHBoxLayout(message_column)
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(2)

        # message box - flexible width, fixed height
        self.message_box = QLabel("Message")
        if DEBUG:
            self.message_box.setStyleSheet(DEBUG_FILL_STYLE)
        message_layout.addWidget(self.message_box)

        # wells column
        wells_column = QWidget()
        wells_column.setFixedWidth(256)
        wells_column.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        wells_layout = QHBoxLayout(wells_column)
        wells_layout.setContentsMargins(0, 0, 0, 0)
        wells_layout.setSpacing(2)

        # wells box - flexible width, fixed height
        self.well_1_box = QLabel("Well 1")
        if DEBUG:
            self.well_1_box.setStyleSheet(DEBUG_FILL_STYLE)
        wells_layout.addWidget(self.well_1_box)

        self.well_2_box = QLabel("Well 2")
        if DEBUG:
            self.well_2_box.setStyleSheet(DEBUG_FILL_STYLE)
        wells_layout.addWidget(self.well_2_box)

        status_layout.addWidget(message_column)
        status_layout.addWidget(wells_column)

        self.setLayout(status_layout)  # set the layout for the widge

        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

    def set_message(self, message: str):
        self.message_box.setText(message)

    def set_well_1(self, message: str):
        self.well_1_box.setText(message)

    def set_well_2(self, message: str):
        self.well_2_box.setText(message)


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workbench")
        self.setMinimumSize(800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # setup the screen layout
        window_layout = QVBoxLayout(central_widget)
        window_layout.setContentsMargins(0,0,0,0)
        window_layout.setSpacing(0)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        main_layout.addWidget(EmptyFrame("Canvas Area"))
        main_layout.addWidget(EmptyFrame("Work Area", width=256))

        window_layout.addLayout(main_layout)
        #window_layout.addWidget(EmptyFrame("Status Bar", height=32))


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
