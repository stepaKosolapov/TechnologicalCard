import sys
from PyQt5.QtWidgets import QApplication
import config
import mainwindow
import editwindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    config.mainFont = 'Century Gothic'
    editWindow = editwindow.EditWindow()
    mainWindow = mainwindow.MainWindow()
    sys.exit(app.exec_())
