from file_functions import open_file, open_directory, check_playlists_path, add_playlist, get_playlist_songs, start_music_player
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy, QCheckBox, QScrollArea
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal


class MusicPlayer(QWidget):
    def __init__(self, max_width, max_height):
        super().__init__()

        self.setMaximumHeight(max_height)
        self.setMaximumWidth(max_width)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVideoOutput(QVideoWidget())

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)

        self.time_label = QLabel()
        self.song_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.song_label)
        layout.addWidget(self.playButton)
        layout.addWidget(self.slider)
        layout.addWidget(self.time_label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateSlider)

        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

    def setUrl(self, url):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.mediaPlayer.mediaStatusChanged.connect(self.onMediaStatusChanged)
        self.play()

        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)

        song_name = url.split("/")[-1]
        self.song_label.setText(song_name)

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.slider.setMaximum(self.mediaPlayer.duration() // 1000)
            self.slider.setPageStep(1)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            self.timer.start()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText('Pause')
        else:
            self.playButton.setText('Play')

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position * 1000)

    def updateSlider(self):
        position = self.mediaPlayer.position()
        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)  # Update maximum dynamically
        self.slider.setValue(position // 1000)
        self.time_label.setText(
            f"{position // 60000}:{'0' if (position // 1000) % 60 < 10 else ''}{(position // 1000) % 60}")


class SongButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None, styles=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.button = QPushButton(text)
        self.button.clicked.connect(self.on_button_clicked)
        if styles:
            self.button.setStyleSheet(styles)
        else:
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid black;
                    border-radius: 10px;
                    width: 100%;
                    padding: 10px;
                    margin: 20px;
                }
            """)

        self.layout.addWidget(self.button)

        # Set minimum width and height based on the button's size hint
        self.setMinimumWidth(self.button.sizeHint().width() + 20)
        self.setMinimumHeight(self.button.sizeHint().height() + 20)

    def on_button_clicked(self):
        self.clicked.emit()


def PlaylistWidget(QWidget):
    def __init__(self, text="Placeholder Text", parent=None, styles=None):
        super().__init__(parent)


class MainWindow(QMainWindow):

    def __init__(self, widgets=None):
        super().__init__()

        self.setWindowTitle("Python Music Player")
        self.width, self.height = 500, 500
        self.resize(self.width, self.height)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # self.scroll_area = QScrollArea(self)
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setCentralWidget(self.scroll_area)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.max_width = int(self.width)
        self.max_height = int(self.height * 0.22)
        self.music_player = MusicPlayer(self.max_width, self.max_height)

        self.make_widgets()

    def remove_widgets(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

    def replace_player_to_widgets(self):
        self.remove_widgets()

        self.main_layout.removeWidget(self.music_player)
        self.music_player.setParent(None)
        self.music_player = None
        self.make_widgets()

    def replace_widgets_to_player(self):
        self.remove_widgets()

        self.main_layout.addWidget(self.music_player)
        self.back_to_menu_button = SongButton("Go Back", parent=self)
        self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        self.main_layout.addWidget(self.back_to_menu_button)

    def make_widgets(self):
        self.song_widget = SongButton("Your playlists", parent=self)
        self.song_widget.clicked.connect(lambda: self.show_playlists())

        self.file_dialog = SongButton("Play a song", parent=self)
        self.music_player = MusicPlayer(max_width=self.max_width, max_height=self.max_height)
        self.file_dialog.clicked.connect(lambda: open_file(self.file_dialog, self, self.music_player))

        self.main_layout.addWidget(self.song_widget)
        self.main_layout.addWidget(self.file_dialog)

    def replace_songs_to_playlists(self):
        self.remove_widgets()
        self.show_playlists()

    def display_playlist_songs(self, playlists_name):
        self.back_to_playlist_button = SongButton("Go Back", parent=self)
        self.back_to_playlist_button.clicked.connect(lambda: self.replace_songs_to_playlists())

        songs = get_playlist_songs(playlists_name)
        self.remove_widgets()
        for song in songs:
            full_song_path = f"{playlists_name}/{song}"
            song_button = SongButton(song, parent=self)
            song_button.clicked.connect(lambda: start_music_player(self, full_song_path, self.music_player))
            self.main_layout.addWidget(song_button)

    def show_playlists(self):
        self.remove_widgets()
        playlists_names = check_playlists_path()

        self.add_playlist_button = SongButton("Add new playlist", parent=self)
        self.add_playlist_button.clicked.connect(lambda: add_playlist(open_directory(self)))
        self.main_layout.addWidget(self.add_playlist_button)

        self.back_to_menu_button = SongButton("Go Back", parent=self)
        self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        self.main_layout.addWidget(self.back_to_menu_button)

        if playlists_names:
            for playlists_name in playlists_names:
                playlist_button = SongButton(playlists_name, parent=self)
                playlist_button.clicked.connect(lambda: self.display_playlist_songs(playlists_name))
                self.main_layout.addWidget(playlist_button)
