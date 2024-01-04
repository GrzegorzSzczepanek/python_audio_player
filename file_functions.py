from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy
from gui_elements import MusicPlayer


def open_file(self, main_window):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
    if file_name:
        player = MusicPlayer()
        player.setUrl(file_name)
        main_window.setCentralWidget(player)
        print(file_name)
