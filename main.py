from PyQt5.QtWidgets import QApplication
from window import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()


