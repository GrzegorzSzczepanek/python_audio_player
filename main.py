from PyQt5.QtWidgets import QApplication
from gui_elements import MainWindow, SongButton, MusicPlayer
from file_functions import open_file
# songs save path: HOME/.local/share


def main():
    app = QApplication([])

    main_window = MainWindow()
    song_widget = SongButton("your songs", main_window)
    song_widget.clicked.connect(lambda: print("xd"))
    file_dialog = SongButton("Pick a song", main_window, """
                QPushButton {
                    border: 1px solid black;
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 40px;
                }
            """)
    file_dialog.clicked.connect(lambda: open_file(file_dialog, main_window))
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
