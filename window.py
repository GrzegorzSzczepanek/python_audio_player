from file_functions import (open_file, open_directory, check_playlists_path,
                            add_playlist, get_playlist_songs, start_music_player,
                            create_playlist, find_all_songs)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QMainWindow, QInputDialog
from audio_player import AudioPlayer
from customizable_button import SongButton
from file_functions import remove_playlist


def PlaylistWidget(QWidget):
    def __init__(self, text="Placeholder Text", parent=None, styles=None):
        super().__init__(parent)


class MainWindow(QMainWindow):

    def __init__(self, widgets=None):
        super().__init__()

        self.setWindowTitle("Python Music Player")
        self.width, self.height = 500, 500

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.max_width = int(self.width)
        self.max_height = int(self.height * 0.4)
        self.music_player = AudioPlayer(self.max_width, self.max_height)

        self.make_widgets()

    def remove_widgets(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

    def reset_player(self):
        self.main_layout.removeWidget(self.music_player)
        self.music_player.setParent(None)
        self.music_player = None
        self.music_player = AudioPlayer(self.max_width, self.max_height)

    def replace_player_to_widgets(self):
        self.remove_widgets()
        self.reset_player()
        self.make_widgets()

    def song_back_button(self, playlist):
        self.reset_player()
        self.main_layout.removeWidget(self.music_player)
        self.display_playlist_songs(playlist)

    def replace_widgets_to_player(self, playlist=None):
        self.remove_widgets()

        self.main_layout.addWidget(self.music_player)
        self.back_to_menu_button = SongButton("Go Back", parent=self)
        if playlist:
            self.back_to_menu_button.clicked.connect(lambda x=playlist: self.song_back_button(x))
        else:
            self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        self.main_layout.addWidget(self.back_to_menu_button)

    def make_widgets(self):
        scroll_area = QScrollArea()

        playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(playlist_widget)

        self.song_widget = SongButton("Your playlists", parent=self)
        self.song_widget.clicked.connect(lambda: self.show_playlists())
        playlist_layout.addWidget(self.song_widget)

        self.file_dialog = SongButton("Play a song", parent=self)
        self.file_dialog.clicked.connect(lambda: open_file(self.file_dialog, self, self.music_player))
        playlist_layout.addWidget(self.file_dialog)

        self.file_dialog = SongButton("See all songs in Music folder", parent=self)
        self.file_dialog.clicked.connect(lambda: self.display_all_songs(all_songs=find_all_songs()))
        playlist_layout.addWidget(self.file_dialog)

        scroll_area.setWidget(playlist_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)

    def replace_songs_to_playlists(self):
        self.remove_widgets()
        self.reset_player()
        self.show_playlists()

    def song_to_playlist_after_removing(self, path: str):
        self.remove_widgets()
        remove_playlist(path)
        self.reset_player()
        self.show_playlists()

    def display_playlist_songs(self, playlists_path: str, all_songs: list = None):
        songs = get_playlist_songs(playlists_path) if not all_songs else all_songs
        self.remove_widgets()

        scroll_area = QScrollArea()

        song_widget = QWidget()
        song_layout = QVBoxLayout(song_widget)

        self.back_to_playlist_button = SongButton("Go Back", parent=self)
        self.back_to_playlist_button.clicked.connect(lambda: self.replace_songs_to_playlists())
        song_layout.addWidget(self.back_to_playlist_button)

        if not all_songs:
            self.remove_playlist_button = SongButton("Remove this playlist", parent=self)
            self.remove_playlist_button.clicked.connect(lambda: self.song_to_playlist_after_removing(playlists_path))
            song_layout.addWidget(self.remove_playlist_button)

        for song in songs:
            full_song_path = f"{playlists_path}/{song}"
            song_button = SongButton(song, parent=self)
            song_button.clicked.connect(lambda path=full_song_path: start_music_player(self,
                                                                                       path,
                                                                                       self.music_player,
                                                                                       playlists_path))
            song_layout.addWidget(song_button)

        scroll_area.setWidget(song_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)

    def display_all_songs(self, all_songs: list):
        self.remove_widgets()

        scroll_area = QScrollArea()

        song_widget = QWidget()
        song_layout = QVBoxLayout(song_widget)

        self.back_button = SongButton("Go Back", parent=self)
        self.back_button.clicked.connect(lambda: self.make_widgets())
        song_layout.addWidget(self.back_button)

        for song in all_songs:
            song_button = SongButton(song, parent=self)
            song_button.clicked.connect(lambda: start_music_player(self,
                                                                   song,
                                                                   self.music_player,
                                                                   all_songs))
            song_layout.addWidget(song_button)

        scroll_area.setWidget(song_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)

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

        self.add_playlist_button = SongButton("Add existing playlist", parent=self)
        self.add_playlist_button.clicked.connect(lambda: add_playlist(self, open_directory(self)))
        playlist_layout.addWidget(self.add_playlist_button)

        self.back_to_menu_button = SongButton("Go Back", parent=self)
        self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        playlist_layout.addWidget(self.back_to_menu_button)

        self.create_playlist_button = SongButton("Create new playlist", parent=self)
        self.create_playlist_button.clicked.connect(lambda: self.name_the_playlist())
        playlist_layout.addWidget(self.create_playlist_button)

        if playlists_names:
            for playlists_name in playlists_names:
                playlist_button = SongButton(playlists_name.split("/")[-1], parent=self)
                playlist_button.clicked.connect(lambda playlist=playlists_name: self.display_playlist_songs(playlist))
                playlist_layout.addWidget(playlist_button)

        scroll_area.setWidget(playlist_widget)
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
