from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVideoOutput(QVideoWidget())

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.playButton)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

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
        self.label.setText(
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
                    padding: 10px;
                    margin: 0px;
                    margin-bottom:100px;
                }
            """)

        self.layout.addWidget(self.button)

        # Set minimum width and height based on the button's size hint
        self.setMinimumWidth(self.button.sizeHint().width() + 20)
        self.setMinimumHeight(self.button.sizeHint().height() + 20)

        # Set size policy if needed
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def on_button_clicked(self):
        self.clicked.emit()


class MainWindow(QMainWindow):
    def __init__(self, central_widget=None, parent=None):
        super().__init__()

        self.setWindowTitle("Python Music Player")
        self.resize(500, 500)
        self.resize(300, 300)
        button = QPushButton("Test BTn")

        # if central_widget:
        #     self.setCentralWidget(central_widget)
        # else:
        #     self.setCentralWidget(button)


# class FileDialog(QWidget):
#     def __init__(self, parent=None):
#         super(FileDialog, self).__init__(parent)
#
#         self.button = QPushButton("Play a song")
#         self.button.clicked.connect(self.open_file)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.button)
#
#         self.le = QLabel("Song Path")
#         self.setLayout(layout)
#         self.setWindowTitle("Song Picker")
#
#     def open_file(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly
#         fileName, _ = QFileDialog.getOpenFileName(
#             self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
#         if fileName:
#             self.le.setText(fileName)
