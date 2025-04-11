import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)

from qdbg import console  # Assuming DEBUG, DEBUG_FILL_STYLE, LOG_LEVEL are not used


class NumberedButton(QPushButton):  # More descriptive name
    """A push button with a leading number."""

    _BUTTON_STYLESHEET = """
        background-color: #f0f0f0;
        border: 1px solid black;
        border-radius: 4px;
        font-size: 16px;
        font-weight: bold;
        padding: 4px;
        """

    _NUMBER_STYLESHEET = """
        background-color: #66CCFF;
        border: 1px solid black;
        border-radius: 4px;
        font-size: 16px;
        """

    _TEXT_STYLESHEET = """
        border: none;
        font-size: 18px;
        """

    def __init__(self, number: int, text: str, parent=None):  # Add parent parameter
        super().__init__(parent)
        self.num = number

        self.setStyleSheet(self._BUTTON_STYLESHEET)
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        number_label = QLabel(str(number), self)  # Set parent for child widgets
        number_label.setStyleSheet(self._NUMBER_STYLESHEET)
        number_label.setAlignment(Qt.AlignCenter)
        number_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        number_label.setFixedWidth(self.fontMetrics().boundingRect("999").width())
        layout.addWidget(number_label)

        text_label = QLabel(text, self)  # Set parent for child widgets
        text_label.setStyleSheet(self._TEXT_STYLESHEET)
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        text_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layout.addWidget(text_label)

    def keyPressEvent(self, event: QKeyEvent):
        console.info(f"Key pressed: {event.key()}")
        if event.key() == self.num + Qt.Key_0:
            console.info(f"Button {self.num} pressed")
            self.click()

    def mousePressEvent(self, event):
        console.info(f"Mouse pressed: {event.button()}")


class MainWindow(QMainWindow):
    def __init__(self, parent=None):  # Add parent parameter
        super().__init__(parent)
        self.setWindowTitle("Workbench")
        self.setMinimumSize(256, 256)

        central_widget = QWidget(self)  # Set parent for central widget
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)  # Set parent for layout
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        button = NumberedButton(1, "Untitled button", central_widget)  # Use NumberedButton, set parent
        layout.addWidget(button)

    def keyPressEvent(self, event: QKeyEvent):
        console.info(f"Key pressed: {event.key()}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    console.info("Starting application ...")
    ret = app.exec()
    console.info("Exiting application ...")

    sys.exit(ret)  # Exit with the return code from app.exec()


if __name__ == "__main__":
    main()