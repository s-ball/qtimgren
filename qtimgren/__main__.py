from PyQt5.QtWidgets import QApplication
from .main_window import MainWindow
import sys


def run():
    app = QApplication(sys.argv)
    app.setOrganizationName('SBA')
    app.setApplicationName('QtImgren')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
