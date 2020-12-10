import sys
from PyQt5.QtWidgets import QApplication
import mainwindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow.mainFont = 'Century Gothic'
    mainWindow = mainwindow.MainWindow()
    sys.exit(app.exec_())
