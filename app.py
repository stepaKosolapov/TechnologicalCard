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
    controller.save()
    controller.load()
    config.mainFont = 'Century Gothic'
    config.colors[0] = '#9ACD32'
    config.colors[1] = '#DCDCDC'
    config.colors[2] = '#FFA07A'
    config.colors[3] = '#FFDAB9'
    selectWindow = selectwindow.SelectWindow()
    editWindow = editwindow.EditWindow()
    mainWindow = mainwindow.MainWindow()
    dishWindow = dishwindow.DishWindow()
    selectWindow.show()
    sys.exit(app.exec_())
