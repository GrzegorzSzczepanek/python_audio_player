import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow
import os
os.environ['QT_QPA_PLATFORM'] = 'wayland'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #333;
        color: #fff;
        font-size: 16px;
    }
    QPushButton {
        background-color: #555;
        border: none;
        color: #fff;
        padding: 5px;
        min-width: 70px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #777;
    }
    QPushButton:pressed {
        background-color: #999;
    }
    QSlider::groove:horizontal {
        height: 8px;
        background: #999;
    }
    QSlider::handle:horizontal {
        width: 18px;
        background: #555;
        margin: -5px 0;
        border-radius: 9px;
    }
    QCheckBox {
        spacing: 5px;
    }
    QCheckBox::indicator {
        width: 13px;
        height: 13px;
    }
""")

    main_window = MainWindow()
    main_window.show()
    app.exec_()
