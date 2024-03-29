from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class SongButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None, styles=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.button = QPushButton(text)
        self.button.clicked.connect(self.on_button_clicked)
        if styles:
            self.button.setStyleSheet(styles)
        else:
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid black;
                    border-radius: 10px;
                    width: 100%;
                    padding: 10px;
                    margin: 20px;
                }
            """)

        self.layout.addWidget(self.button)

        self.setMinimumWidth(self.button.sizeHint().width() + 20)
        self.setMinimumHeight(self.button.sizeHint().height() + 20)

    def on_button_clicked(self):
        self.clicked.emit()
