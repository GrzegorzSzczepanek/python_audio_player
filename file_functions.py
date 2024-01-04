from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy

def open_file(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    fileName, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)
