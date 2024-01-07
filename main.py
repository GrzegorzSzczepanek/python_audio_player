from PyQt5.QtWidgets import QApplication
from gui_elements import MainWindow, SongButton, MusicPlayer
from file_functions import open_file, open_directory, check_playlists_path


def main():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
