from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy


def open_file(self, parent, music_player):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
    if file_name:
        parent.replace_widgets_to_player()
        player = music_player
        player.setUrl(file_name)
        parent.layout().addWidget(player)
        print(file_name)
