from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_elements import FileDialog, MainWidnow

# songs save path: HOME/.local/share


def main():
    app = QApplication([])

    main_window = MainWidnow()
    main_window.show()

    app.exec_()


if __name__ == '__main__':
    main()
