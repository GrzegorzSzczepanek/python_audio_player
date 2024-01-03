from PyQt5.QtWidgets import QApplication
from gui_elements import MainWindow, SongWidget
from file_functions import open_file
# songs save path: HOME/.local/share


def main():
    app = QApplication([])

    main_window = MainWindow()

    song_widget = SongWidget("got it on me", main_window)
    song_widget.clicked.connect(lambda: print("dupa"))
    file_dialog = SongWidget("Pick a song", main_window, """
                QLabel {
                    border: 1px solid black;
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 100px;
                }
            """)
    file_dialog.clicked.connect(lambda: open_file(file_dialog))

    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
