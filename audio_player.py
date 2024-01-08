from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy, QCheckBox, QScrollArea
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class AudioPlayer(QWidget):
    def __init__(self, max_width, max_height):
        super().__init__()

        self.setMaximumHeight(max_height)
        self.setMaximumWidth(max_width)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVideoOutput(QVideoWidget())

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

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
        self.timer.timeout.connect(self.update_slider)

        self.mediaPlayer.stateChanged.connect(self.media_state_changed)

    def set_path(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.mediaStatusChanged.connect(self.on_media_status_changed)
        self.play()

        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)

        song_name = path.split("/")[-1]
        self.song_label.setText(song_name)

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

    def update_slider(self):
        position = self.mediaPlayer.position()
        self.slider.setMaximum(self.mediaPlayer.duration() // 1000)  # Update maximum dynamically
        self.slider.setValue(position // 1000)
        self.time_label.setText(
            f"{position // 60000}:{'0' if (position // 1000) % 60 < 10 else ''}{(position // 1000) % 60}")
