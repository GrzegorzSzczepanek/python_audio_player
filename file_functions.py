from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QVBoxLayout,
                             QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy)
import os


def start_music_player(parent, file_name, music_player, playlist=None):
    parent.replace_widgets_to_player(playlist)
    player = music_player
    player.set_path(file_name)
    parent.layout().addWidget(player)


def find_all_songs():
    file_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk('/home/grzesiek/Music') for f in filenames if f.endswith(('.mp3', '.wav', '.flac'))]
    return file_paths


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


def add_playlist(self, new_playlist_path):
    playlists_path = os.path.expanduser("~/.local/share/PyPlayer/")
    playlists_file = "playlists.txt"
    playlists_path = os.path.join(playlists_path, playlists_file)

    with open(playlists_path, "r") as file:
        if new_playlist_path not in file.read():
            with open(playlists_path, "a") as append_file:
                append_file.write(f"{new_playlist_path}\n")

    self.remove_widgets()
    self.show_playlists()


def create_playlist(playlist_name):
    playlist_path = os.path.expanduser("~/.local/share/PyPlayer/")
    # Create created_playlists directory if it doesn't exist
    created_playlists_path = os.path.join(playlist_path, "created_playlists")
    if not os.path.exists(created_playlists_path):
        os.makedirs(created_playlists_path)

    # Create the file with the provided playlist name
    playlist_file_path = os.path.join(created_playlists_path, f"{playlist_name}.txt")
    with open(playlist_file_path, 'w') as playlist_file:
        playlist_file.write("")


def add_song_to_playlist(playlist_name: str, path_to_song: str):
    playlist_path = os.path.expanduser("~/.local/share/PyPlayer/created_playlists/")
    playlist_path = os.path.join(playlist_path, playlist_name)

    with open(playlist_path, "r") as file:
        if playlist_path not in file.read():
            with open(playlist_path, "a") as append_file:
                append_file.write(f"{path_to_song}\n")


def get_playlist_songs(name):
    playlist_path = os.path.expanduser("~/.local/share/PyPlayer/")
    playlist_path = os.path.join(playlist_path, name)
    print(playlist_path)

    if not os.path.exists(playlist_path):
        print(f"Playlist '{name}' not found at '{playlist_path}'.")
        return None

    all_files = os.listdir(playlist_path)
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac']
    audio_files = [file for file in all_files if any(file.lower().endswith(ext) for ext in audio_extensions)]

    return audio_files


def remove_playlist(playlist_to_delete):
    playlists_path = os.path.expanduser("~/.local/share/PyPlayer/")
    playlists_file = "playlists.txt"
    playlists_path = os.path.join(playlists_path, playlists_file)

    try:
        with open(playlists_path, 'r') as file:
            playlists = file.readlines()

        # remove the specified playlist path
        playlists = [playlist.strip() for playlist in playlists if playlist.strip() != playlist_to_delete]

        with open(playlists_path, 'w') as file:
            file.write('\n'.join(playlists))

        print(f"Playlist path '{playlist_to_delete}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting playlist path: {str(e)}")
