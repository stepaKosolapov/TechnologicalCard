import sys

from PyQt5.QtWidgets import QApplication

import config
import controller
import selectwindow
import dishwindow
import mainwindow
import editwindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller.load()
    config.mainFont = 'Century Gothic'
    selectWindow = selectwindow.SelectWindow()
    editWindow = editwindow.EditWindow()
    mainWindow = mainwindow.MainWindow()
    dishWindow = dishwindow.DishWindow()
    selectWindow.show()
    sys.exit(app.exec_())
