from file_functions import (open_file, open_directory, check_playlists_path,
                            add_playlist, get_playlist_songs, start_music_player,
                            create_playlist, find_all_songs)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QMainWindow, QInputDialog, QPushButton
from PyQt5.QtCore import Qt
from audio_player import AudioPlayer
from customizable_button import SongButton
from file_functions import remove_playlist


def PlaylistWidget(QWidget):
    def __init__(self, text="Placeholder Text", parent=None, styles=None):
        super(PlaylistWidget, self).__init__(parent)


class MainWindow(QMainWindow):
    def __init__(self, widgets=None):
        super().__init__()

        self.is_music_folder = False  # Variable used for routing when listening to all of the songs in music folder
        self.setWindowTitle("Python Music Player")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.setBaseSize(400, 700)

        self.music_player = AudioPlayer()

        self.make_widgets()

    def remove_widgets(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def reset_player(self):
        self.main_layout.removeWidget(self.music_player)
        self.music_player.setParent(None)
        self.music_player = None
        self.music_player = AudioPlayer()

    def replace_player_to_widgets(self):
        self.remove_widgets()
        self.reset_player()
        self.make_widgets()

    def song_back_button(self, playlist):
        if self.is_music_folder:
            self.reset_player()
            self.main_layout.removeWidget(self.music_player)
            self.display_all_songs(find_all_songs())
        else:
            self.reset_player()
            self.main_layout.removeWidget(self.music_player)
            self.display_playlist_songs(playlist)

    def replace_widgets_to_player(self, playlist=None):
        self.remove_widgets()
        self.main_layout = QVBoxLayout(self.central_widget)

        self.back_to_menu_button = QPushButton("Go Back")

        if playlist:
            self.back_to_menu_button.clicked.connect(lambda x=playlist: self.song_back_button(x))
        else:
            self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())

        self.main_layout.addWidget(self.back_to_menu_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.music_player, alignment=Qt.AlignCenter)

        self.adjustSize()

    def make_widgets(self):
        self.remove_widgets()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #333;
            }
            QScrollBar:vertical {
                border: none;
                background: #555;
                width: 15px;
                margin: 15px 0 15px 0;
            }
            QScrollBar::handle:vertical {
                background: #777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(playlist_widget)
        playlist_layout.setAlignment(Qt.AlignCenter)  # Center the layout

        self.song_widget = QPushButton("Your playlists")
        self.song_widget.clicked.connect(lambda: self.show_playlists())
        playlist_layout.addWidget(self.song_widget)

        self.file_dialog1 = QPushButton("Play a song")
        self.file_dialog1.clicked.connect(lambda: open_file(self.file_dialog1, self, self.music_player))
        playlist_layout.addWidget(self.file_dialog1)

        self.file_dialog2 = QPushButton("See all songs in Music folder")
        self.file_dialog2.clicked.connect(lambda: self.display_all_songs(all_songs=find_all_songs()))
        playlist_layout.addWidget(self.file_dialog2)

        scroll_area.setWidget(playlist_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
        self.adjustSize()  # Ensure the window resizes to fit the new layout

    def replace_songs_to_playlists(self):
        self.remove_widgets()
        self.reset_player()
        self.show_playlists()
        self.adjustSize()

    def song_to_playlist_after_removing(self, path: str):
        self.remove_widgets()
        remove_playlist(path)
        self.reset_player()
        self.show_playlists()
        self.adjustSize()

    def display_playlist_songs(self, playlists_path: str, all_songs: list = None):
        self.is_music_folder = False

        songs = get_playlist_songs(playlists_path) if not all_songs else all_songs
        self.remove_widgets()

        scroll_area = QScrollArea()

        song_widget = QWidget()
        song_layout = QVBoxLayout(song_widget)
        song_layout.setAlignment(Qt.AlignCenter)  # Center the layout

        self.back_to_playlist_button = QPushButton("Go Back")
        self.back_to_playlist_button.clicked.connect(lambda: self.replace_songs_to_playlists())
        song_layout.addWidget(self.back_to_playlist_button)

        if not all_songs:
            self.remove_playlist_button = QPushButton("Remove this playlist")
            self.remove_playlist_button.clicked.connect(lambda: self.song_to_playlist_after_removing(playlists_path))
            song_layout.addWidget(self.remove_playlist_button)

        for song in songs:
            full_song_path = f"{playlists_path}/{song}"
            song_button = QPushButton(song)
            song_button.clicked.connect(lambda checked, path=full_song_path: start_music_player(
                self, path, self.music_player, playlists_path))
            song_layout.addWidget(song_button)

        scroll_area.setWidget(song_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
        self.adjustSize()  # Ensure the window resizes to fit the new layout

    def display_all_songs(self, all_songs: list):
        self.remove_widgets()

        scroll_area = QScrollArea()

        song_widget = QWidget()
        song_layout = QVBoxLayout(song_widget)
        song_layout.setAlignment(Qt.AlignCenter)  # Center the layout

        self.back_button = QPushButton("Go Back")
        self.back_button.clicked.connect(lambda: self.make_widgets())
        song_layout.addWidget(self.back_button)

        self.is_music_folder = True

        for song in all_songs:
            song_button = QPushButton(song.split("/")[-1])
            song_button.clicked.connect(lambda checked, song=song: start_music_player(
                self, song, self.music_player, all_songs))
            song_layout.addWidget(song_button)

        scroll_area.setWidget(song_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
        self.adjustSize()  # Ensure the window resizes to fit the new layout

    def name_the_playlist(self):
        text, ok = QInputDialog.getText(self, 'New Playlist', 'Enter playlist name:')
        if ok:
            playlist_name = text
            create_playlist(playlist_name)
        print(playlist_name)
        # return playlist_name

    def show_playlists(self):
        self.remove_widgets()
        playlists_names = check_playlists_path()
        # created_playlists_path = check_created_playlists_path()

        scroll_area = QScrollArea()

        playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(playlist_widget)
        playlist_layout.setAlignment(Qt.AlignCenter)  # Center the layout

        self.add_playlist_button = QPushButton("Add existing playlist")
        self.add_playlist_button.clicked.connect(lambda: add_playlist(self, open_directory(self)))
        playlist_layout.addWidget(self.add_playlist_button)

        self.back_to_menu_button = QPushButton("Go Back")
        self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        playlist_layout.addWidget(self.back_to_menu_button)

        self.create_playlist_button = QPushButton("Create new playlist")
        self.create_playlist_button.clicked.connect(lambda: self.name_the_playlist())
        playlist_layout.addWidget(self.create_playlist_button)

        if playlists_names:
            for playlists_name in playlists_names:
                playlist_button = QPushButton(playlists_name.split("/")[-1])
                playlist_button.clicked.connect(
                    lambda checked, playlist=playlists_name: self.display_playlist_songs(playlist))
                playlist_layout.addWidget(playlist_button)

        scroll_area.setWidget(playlist_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
        self.adjustSize()  # Ensure the window resizes to fit the new layout
