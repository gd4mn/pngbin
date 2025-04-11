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

DEFAULT_FRAME_SPACING = 8


class ImageItem:
    def __init__(self, path: str):
        self.name = os.path.basename(path)
        self.dir = os.path.dirname(path)

    def put(self, new_dir: str):
        self.dir = new_dir

    def move(self):
        pass

    def delete(self):
        pass

    def __repr__(self):
        return f"ImageItem(name={self.name}, dir={self.dir})"

    def __str__(self):
        return f"ImageItem({self.dir + self.name})"


# global variables
source_dir = ""
gallery_dir = ""
image_list: list[ImageItem] = []


class D4mnPushButton(QPushButton):
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


class D4mnStatusBar(QWidget):
    stylesheet = (
        "background-color: #999999; border-top: 2px solid #000000; font-size: 11px;"
    )
    well_frame_width = 256

    def __init__(self):
        super().__init__()

        self.setStyleSheet(self.stylesheet)
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)
        self.setFixedHeight(24)

        bar_layout = QHBoxLayout()
        bar_layout.setContentsMargins(4, 0, 4, 0)
        bar_layout.setSpacing(DEFAULT_FRAME_SPACING)
        self.setLayout(bar_layout)

        # add the message
        self.message_label = QLabel("Messages")
        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        bar_layout.addWidget(self.message_label)

        # add the wells
        well_widget = QWidget()
        well_widget.setFixedWidth(self.well_frame_width)
        if DEBUG:
            well_widget.setStyleSheet(DEBUG_FILL_STYLE)

        well_layout = QHBoxLayout(well_widget)
        well_layout.setContentsMargins(0, 0, 0, 0)
        well_layout.setSpacing(DEFAULT_FRAME_SPACING)

        self.well_1 = QLabel("Well 1")
        if DEBUG:
            self.well_1.setStyleSheet(DEBUG_FILL_STYLE)

        self.well_2 = QLabel("Well 2")
        if DEBUG:
            self.well_2.setStyleSheet(DEBUG_FILL_STYLE)

        well_layout.addWidget(self.well_1)
        well_layout.addWidget(self.well_2)

        bar_layout.addWidget(well_widget)

    def set_message(self, message: str):
        self.message_label.setText(message)

    def set_well_1(self, message: str):
        self.well_1.setText(message)

    def set_well_2(self, message: str):
        self.well_2.setText(message)


class D4mnEmptyFrame(QWidget):
    stylesheet = (
        "background-color: #99FF33; color: white; font-size: 16px; font-weight=bold;"
    )

    def __init__(self, message: str = "", width: int = 0, height: int = 0):
        super().__init__()

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.setStyleSheet(self.stylesheet)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(DEFAULT_FRAME_SPACING)
        self.setLayout(frame_layout)

        # add the message
        self.frame_message = message
        if self.frame_message:
            self.frame_label = QLabel()
            self.frame_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            )
            if DEBUG:
                self.frame_label.setStyleSheet(DEBUG_FILL_STYLE)

            frame_layout.addWidget(self.frame_label)

            self.resizeEvent(None)

    def resizeEvent(self, event):
        if self.frame_message:
            # get the frame geometry
            width, height = (
                self.frame_label.size().width(),
                self.frame_label.size().height(),
            )
            self.frame_label.setText(f"{self.frame_message}\n{width}x{height}")


class D4mnImageFrame(QWidget):
    def __init__(self, image: QImage, width: int = 0, height: int = 0):
        super().__init__()

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)

        pixmap = QPixmap.fromImage(image)
        frame_label = QLabel()
        frame_label.setScaledContents(True)
        frame_label.setPixmap(pixmap)
        frame_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        frame_layout.addWidget(frame_label)
        self.setLayout(frame_layout)


class D4mnControlFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(256)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(DEFAULT_FRAME_SPACING)
        self.setLayout(frame_layout)

        logo_widget = D4mnImageFrame(QImage("./rsc/logo.png"), height=128)
        folder_widget = D4mnEmptyFrame("Folder", height=320)
        meta_widget = D4mnEmptyFrame("Metadata")

        frame_layout.addWidget(logo_widget)
        frame_layout.addWidget(folder_widget)
        frame_layout.addWidget(meta_widget)


class MainWindow(QMainWindow):
    def __init__(self, source_dir: str, gallery_dir: str):
        super().__init__()
        self.setWindowTitle("PNGbin")
        self.setMinimumSize(1024, 768)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # setup the screen layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(4, 4, 4, 0)
        main_layout.setSpacing(DEFAULT_FRAME_SPACING)

        main_layout.addWidget(D4mnEmptyFrame("Canvas"))
        main_layout.addWidget(D4mnControlFrame())

        # setup the status bar
        status_bar = D4mnStatusBar()

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(DEFAULT_FRAME_SPACING)

        window_layout.addLayout(main_layout)
        window_layout.addWidget(status_bar)

        central_widget.setLayout(window_layout)


def dir_path(path):
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory")


def main():
    parser = argparse.ArgumentParser(description="PNGbin - Image Gallery Manager")
    parser.add_argument(
        "source_dir", type=dir_path, help="Directory containing source images"
    )
    parser.add_argument(
        "gallery_dir", type=dir_path, help="Directory for the gallery output"
    )

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args.source_dir, args.gallery_dir)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
