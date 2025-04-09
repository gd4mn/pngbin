import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

DEBUG = False
if ("-d" in sys.argv) or ("--debug" in sys.argv):
    DEBUG = True

DEBUG_FILL_STYLE = "background-color: rgba(253, 61, 81, 0.2);"


class D4mnInfoBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(256)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnCanvasArea(QWidget):
    def __init__(self):
        super().__init__()
        
        self.canvas_layout = QVBoxLayout()
        
        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(32)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnAboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About D4mn")
        self.setFixedSize(640, 480)

        about_layout = QVBoxLayout()
        about_widget = QLabel("D4mn is a simple PNG editor.")
        about_layout.addWidget(about_widget)
        self.setLayout(about_layout)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class D4mnLogoWidget(QWidget):
    def __init__(self):
        super().__init__()

        logo_image = QImage(" ./rsc/logo.png")
        pixmap = QPixmap.fromImage(logo_image)

        self.setPixmap(pixmap)
        self.setFixedHeight(128)
        self.setScaledContents(True)

        logo_layout = QVBoxLayout()
        logo_layout.addWidget(self)
        self.setLayout(logo_layout)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.about_dialog = D4mnAboutWindow(self)
            self.about_dialog.exec()


class D4mnPushButtton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(128, 128)

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNGbin")
        self.setMinimumSize(1024, 768)

        # setup the screen layout
        window_layout = QHBoxLayout()

        # setup the main area
        main_layout = QVBoxLayout()
        main_layout.addWidget(D4mnCanvasArea())

        # add the fill style for debugging
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
