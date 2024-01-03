from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow


class MainWidnow(QMainWindow):
    def __init__(self, central_widget=None):
        super().__init__()

        self.setWindowTitle("Python Music Player")
        self.resize(500, 500)
        self.resize(300, 300)
        button = QPushButton("Test BTn")

        if central_widget:
            self.setCentralWidget(central_widget)
        else:
            self.setCentralWidget(button)


class FileDialog(QWidget):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__(parent)

        self.button = QPushButton("Open File Dialog")
        self.button.clicked.connect(self.open_file)

        layout = QVBoxLayout()
        layout.addWidget(self.button)

        self.le = QLabel("File Path")
        self.setLayout(layout)
        self.setWindowTitle("File Dialog Demo")

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.le.setText(fileName)
