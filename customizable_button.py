from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class SongButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text="", styles=None):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.button = QPushButton(text)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.setDefault(True)

        if styles:
            self.button.setStyleSheet(styles)
        else:
            self.button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.6, y2:0, stop:0 #4d94ff, stop:1 #0066cc);
                    border: 2px solid #0056b3;
                    border-radius: 15px;
                    color: white;
                    padding: 12px 20px;
                    margin: 20px;
                    max-width: 300px;
                }
                QPushButton:hover {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.6, y2:0, stop:0 #007bff, stop:1 #0056b3);
                }
            """)

        self.layout.addWidget(self.button)

        self.setMinimumWidth(self.button.sizeHint().width() + 40)
        self.setMinimumHeight(self.button.sizeHint().height() + 40)

    def on_button_clicked(self):
        self.clicked.emit()
