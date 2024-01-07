from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy
import os


def start_music_player(parent, file_name, music_player):
    parent.replace_widgets_to_player()
    player = music_player
    player.setUrl(file_name)
    parent.layout().addWidget(player)
    print(file_name)


def open_file(self, parent, music_player):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "Audio Files (*.wav *.mp3 *.flac *.ogg)", options=options)
    if file_name:
        start_music_player(parent, file_name, music_player)


def open_directory(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    directory = QFileDialog.getExistingDirectory(
        self, "Open Folder", "", options=options)
    if directory:
        return directory


def check_playlists_path():
    playlists_path = os.path.expanduser("~/.local/share/PyPlayer/")
    os.makedirs(playlists_path, exist_ok=True)
    playlists_file = "playlists.txt"
    playlists_path = os.path.join(playlists_path, playlists_file)

    if os.path.isfile(playlists_path):

        with open(playlists_path, "r") as file:
            playlists = list(map(lambda x: x.replace("\n", ""), file.readlines()))
        return playlists
    else:
        with open(playlists_path, 'w') as file:
            pass
        return None


def add_playlist(new_playlist_path):
    playlists_path = os.path.expanduser("~/.local/share/PyPlayer/")
    playlists_file = "playlists.txt"
    playlists_path = os.path.join(playlists_path, playlists_file)

    with open(playlists_path, "r") as file:
        if new_playlist_path not in file.read():
            with open(playlists_path, "a") as append_file:
                append_file.write(f"{new_playlist_path}\n")


def get_playlist_songs(name):
    playlist_path = os.path.expanduser("~/.local/share/PyPlayer/")
    playlist_path = os.path.join(playlist_path, name)

    if not os.path.exists(playlist_path):
        print(f"Playlist '{name}' not found at '{playlist_path}'.")
        return None

    all_files = os.listdir(playlist_path)
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac']
    audio_files = [file for file in all_files if any(file.lower().endswith(ext) for ext in audio_extensions)]

    return audio_files
