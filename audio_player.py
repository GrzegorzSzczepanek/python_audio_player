from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy, QCheckBox, QScrollArea
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from file_functions import get_playlist_songs


class AudioPlayer(QWidget):
    def __init__(self, max_width, max_height):
        super().__init__()

        self.setMaximumHeight(max_height)
        self.setMaximumWidth(max_width)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVideoOutput(QVideoWidget())

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)

        self.next_button = QPushButton("next")
        self.previous_button = QPushButton("previous")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        self.time_label = QLabel()
        self.song_label = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.song_label)
        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.previous_button)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.time_label)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_slider)

        self.mediaPlayer.stateChanged.connect(self.media_state_changed)

    def play_song(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.mediaStatusChanged.connect(self.on_media_status_changed)
        self.play()
        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)

        song_name = path.split("/")[-1]
        self.song_label.setText(song_name)

    def reset_buttons(self):
        self.layout.removeWidget(self.previous_button)
        self.previous_button.setParent(None)
        self.previous_button = None
        self.previous_button = QPushButton("Previous")

        self.layout.removeWidget(self.next_button)
        self.next_button.setParent(None)
        self.next_button = None
        self.next_button = QPushButton("Next")

        self.layout.addWidget(self.previous_button)
        self.layout.addWidget(self.next_button)

    def init_buttons(self, path):
        self.next_button.clicked.connect(lambda x=path: self.next_song(x))
        self.previous_button.clicked.connect(lambda x=path: self.previous_song(x))

    def set_path(self, path):
        self.play_song(path)

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.slider.setMaximum(self.mediaPlayer.duration() // 1000)
            self.slider.setPageStep(1)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            self.timer.start()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText('Pause')
        else:
            self.playButton.setText('Play')

    def set_position(self, position):
        self.mediaPlayer.setPosition(position * 1000)

    def next_song(self, path, custom_playlist=None):
        self.current_song_path = path
        playlist_path = "/".join(path.split("/")[0:-1])
        current_song = path.split("/")[-1]
        playlist_songs = get_playlist_songs(playlist_path)

        try:
            current_song_index = playlist_songs.index(current_song)
            next_song_index = current_song_index + 1
            if next_song_index == len(playlist_songs):
                next_song_index = 0  # current song was last one in playlist
                next_song = playlist_songs[next_song_index]
            else:
                next_song_index = current_song_index + 1
                next_song = playlist_songs[next_song_index]

            next_song_path = f"{playlist_path}/{next_song}"
            self.set_path(next_song_path)

        except Exception as e:
            print(f"\n\neeror: {str(e)}")

    def previous_song(self, path, custom_playlist=None):
        self.current_song_path = path
        playlist_path = "/".join(path.split("/")[0:-1])
        current_song = path.split("/")[-1]
        playlist_songs = get_playlist_songs(playlist_path)

        try:
            current_song_index = playlist_songs.index(current_song)
            next_song_index = current_song_index + 1
            if next_song_index == 0:
                next_song_index = len(playlist_songs) - 1  # current song was first in playlist
                next_song = playlist_songs[next_song_index]
            else:
                next_song_index = current_song_index - 1
                next_song = playlist_songs[next_song_index]

            next_song_path = f"{playlist_path}/{next_song}"
            self.set_path(next_song_path)

        except Exception as e:
            print(f"\n\neeror: {str(e)}")

    def update_slider(self):
        position = self.mediaPlayer.position()
        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)  # Update maximum dynamically
        self.slider.setValue(position // 1000)
        self.time_label.setText(
            f"{position // 60000}:{'0' if (position // 1000) % 60 < 10 else ''}{(position // 1000) % 60}")
