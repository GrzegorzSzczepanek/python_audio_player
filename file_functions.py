from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy
import os


def open_file(self, parent, music_player):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "Audio Files (*.wav *.mp3 *.flac)", options=options)
    if file_name:
        parent.replace_widgets_to_player()
        player = music_player
        player.setUrl(file_name)
        parent.layout().addWidget(player)
        print(file_name)


def open_directory(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    directory = QFileDialog.getExistingDirectory(
        self, "Open Folder", "", options=options)
    if directory:
        print(directory)


def check_playlists_path():
    playlists_path = os.path.expanduser("~/.local/share/PyPlayer/Playlists")

    if os.path.isdir(playlists_path):
        playlists = os.listdir(playlists_path)
        # for item in contents:
        #     print(item)
        return playlists
    else:
        os.makedirs(playlists_path, exist_ok=True)
        return
