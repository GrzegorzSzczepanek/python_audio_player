from file_functions import open_file
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy, QCheckBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumHeight(200)

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
                    margin: 20px;
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

    def __init__(self, widgets=None):
        super().__init__()

        self.setWindowTitle("Python Music Player")
        self.setGeometry(100, 100, 500, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.music_player = MusicPlayer()
        self.make_widgets()

    def replace_player_to_widgets(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        self.main_layout.removeWidget(self.music_player)
        self.music_player.setParent(None)
        self.music_player = None
        self.make_widgets()

    def replace_widgets_to_player(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

        self.main_layout.addWidget(self.music_player)
        self.back_to_menu_button = SongButton("Go Back", parent=self)
        self.back_to_menu_button.clicked.connect(lambda: self.replace_player_to_widgets())
        self.main_layout.addWidget(self.back_to_menu_button)

    def make_widgets(self):
        self.song_widget = SongButton("your songs", parent=self)
        self.song_widget.clicked.connect(lambda: self.replace_widgets())

        self.file_dialog = SongButton("Pick a song", parent=self, styles="""
                    QPushButton {
                        border: 1px solid black;
                        border-radius: 10px;
                        padding: 10px;
                        margin-top: 40px;
                        width: 100%;
                    }
                """)
        self.music_player = MusicPlayer()
        self.file_dialog.clicked.connect(lambda: open_file(self.file_dialog, self, self.music_player))

        self.main_layout.addWidget(self.song_widget)
        self.main_layout.addWidget(self.file_dialog)
