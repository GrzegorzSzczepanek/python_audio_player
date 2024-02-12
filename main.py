from PyQt5.QtWidgets import QApplication
from window import MainWindow
from file_functions import remove_playlist


def main():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
