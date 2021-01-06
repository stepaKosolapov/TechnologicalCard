from PyQt5.QtWidgets import (
                                QWidget, QPushButton,
                                QComboBox, QLabel,
                                QLineEdit, QHBoxLayout, QVBoxLayout,
                            )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import mainwindow
import dishwindow
import controller
import config

windowObject = ''

colors = []
mainFont = ''


def _setConfigs():
    """
        Sets the global settings of  selectwindow using the config.py
    """
    global colors, mainFont
    colors = config.colors
    mainFont = config.mainFont


class SelectWindow(QWidget):
    def __init__(self):
        global windowObject
        windowObject = self
        super().__init__()
        _setConfigs()

        self.newDishName = ''
        self.selectedDishName = ''

        self.selectDishBox = QComboBox()
        self.selectDishLabel = QLabel()
        self.nameInput = QLineEdit()
        self.nameLabel = QLabel()
        self.newButton = QPushButton()
        self.editButton = QPushButton()
        self.delButton = QPushButton()

        self.mainHLayout = QHBoxLayout()

        self.selectDishVLayout = QVBoxLayout()
        self.buttonsVLayout = QVBoxLayout()
        self.selectButtonsHLayout = QHBoxLayout()

        self.layoutWidgets()
        self.initWidgets()

    def closeEvent(self, QCloseEvent):
        controller.save()
        self.close()

    def showEvent(self, QShowEvent):
        self.show()
        self.nameInput.setText('')
        controller.resetDishParameters()
        self.updateSelectDishBox()

    def selectingDishChanged(self):
        """
            Called when the dishBox changed
            Updates the selectedDishName parameter using the dishBox
        Uses:
            object dishBox
        Changes:
            parameter selectedDishName
        """
        self.selectedDishName = self.selectDishBox.currentText()

    def inputNameChanged(self):
        """
            Called when the nameInput changes
            Updates the newDishName parameter using the nameInput
        Uses:
            object nameInput
        Changes:
            parameter newDishName
        """
        name = self.nameInput.text()
        self.newDishName = name

    def delButtonClicked(self):
        """
            Called when the delButtons is clicked
            Says controller.py to remove selected dish
        Uses:
            imported module controller
            parameter selectedDishName
        """
        if self.selectedDishName == '':
            return
        controller.removeDish(self.selectedDishName)
        self.updateSelectDishBox()
        controller.save()

    def newButtonClicked(self):
        """
            Called when the newButton is clicked
            Says controller.py to set the newDishName as the name of the current dish
        Uses:
            imported module controller
            parameter newDishName
        """
        controller.resetDishParameters()
        controller.setCurrentName(self.newDishName)
        mainwindow.windowObject.resetToDefaults()
        mainwindow.windowObject.show()
        self.hide()

    def editButtonClicked(self):
        """
            Called when the editButton is clicked
            Says the controller.py to load the selected dish
            Says the mainWindow to load the productTable using the loaded dish parameters
        Uses:
            imported module controller.py
            parameter selectedDishName
        """
        if self.selectedDishName == '':
            return
        controller.loadDish(self.selectedDishName)
        mainwindow.windowObject.loadTableFromController()
        dishwindow.windowObject.show()
        self.hide()

    def updateSelectDishBox(self):
        """
            Updates the selectDishBox using the imported module controller
        Uses:
            imported module controller
        """
        self.selectDishBox.clear()
        for dish in controller.getDishes():
            self.selectDishBox.addItem(dish)

    def layoutWidgets(self):
        """
            Distributes all of the widgets on the layout
        """
        mainHLayout = self.mainHLayout

        mainHLayout.addLayout(self.selectDishVLayout)
        mainHLayout.addLayout(self.buttonsVLayout)

        selectDishVLayout = self.selectDishVLayout
        selectDishVLayout.addWidget(self.nameLabel)
        selectDishVLayout.addWidget(self.nameInput)
        selectDishVLayout.addWidget(self.selectDishLabel)
        selectDishVLayout.addWidget(self.selectDishBox)

        buttonsVLayout = self.buttonsVLayout
        buttonsVLayout.addSpacing(32)
        buttonsVLayout.addWidget(self.newButton)
        buttonsVLayout.addSpacing(32)
        buttonsVLayout.addLayout(self.selectButtonsHLayout)
        buttonsVLayout.addSpacing(3)

        selectButtonsHLayout = self.selectButtonsHLayout
        selectButtonsHLayout.addWidget(self.editButton)
        selectButtonsHLayout.addWidget(self.delButton)

        self.setLayout(mainHLayout)

    def initWidgets(self):
        """
            Sets parameters for all widgets
        """
        global mainFont, colors
        font = QFont(mainFont)
        font.setBold(False)
        color0 = colors[0]
        color1 = colors[1]
        color3 = colors[3]

        self.setFixedSize(600, 150)
        self.setStyleSheet('background-color: {0};'.format(color1))
        self.setWindowTitle('Выбор блюда')
        self.setWindowIcon(QIcon('images/select_icon.png'))

        # comboBox for selecting the dish
        font.setBold(False)
        font.setPointSize(12)
        self.selectDishBox.setFont(font)
        self.selectDishBox.setObjectName('selectDishBox')
        self.selectDishBox.setStyleSheet('background-color: {0};'
                                         'border: 2px solid black;'
                                         'border-radius: 3;'.format(color3)
                                         )
        self.selectDishBox.setFixedHeight(22)
        self.selectDishBox.currentIndexChanged.connect(self.selectingDishChanged)

        # label over the selectDishBox
        font.setBold(False)
        font.setPointSize(14)
        self.selectDishLabel.setFont(font)
        self.selectDishLabel.setObjectName('selectDishLabel')
        self.selectDishLabel.setFixedHeight(22)
        self.selectDishLabel.setAlignment(Qt.AlignCenter)
        self.selectDishLabel.setText('Существующее блюдо')

        # field for input the new dishName
        font.setBold(False)
        font.setPointSize(12)
        self.nameInput.setFont(font)
        self.nameInput.setObjectName('nameInput')
        self.nameInput.setStyleSheet('background-color: {0};'
                                     'border: 2px solid black;'
                                     'border-radius: 3;'.format(color3)
                                     )
        self.nameInput.setFixedHeight(22)
        self.nameInput.setPlaceholderText('имя')
        self.nameInput.setAlignment(Qt.AlignCenter)
        self.nameInput.setMaxLength(15)
        self.nameInput.textChanged.connect(self.inputNameChanged)

        # label over the nameLabel
        font.setBold(False)
        font.setPointSize(14)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName('nameLabel')
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setText('Новое блюдо')
        self.nameLabel.setFixedHeight(22)

        # button to create a new dish
        font.setBold(False)
        font.setPointSize(11)
        self.newButton.setFont(font)
        self.newButton.setObjectName('newButton')
        self.newButton.setStyleSheet('background-color: ' + color0 + ';')
        self.newButton.setText('создать блюдо')
        self.newButton.setMinimumWidth(120)
        self.newButton.clicked.connect(self.newButtonClicked)

        # button to delete selected dish
        font.setBold(False)
        font.setPointSize(11)
        self.delButton.setFont(font)
        self.delButton.setObjectName('delButton')
        self.delButton.setStyleSheet('background-color: ' + '#e03f3f' + ';')
        self.delButton.setText('удалить')
        self.delButton.setMinimumWidth(120)
        self.delButton.clicked.connect(self.delButtonClicked)

        # button to edit selected dish
        font.setBold(False)
        font.setPointSize(11)
        self.editButton.setFont(font)
        self.editButton.setObjectName('editButton')
        self.editButton.setStyleSheet('background-color: ' + color0 + ';')
        self.editButton.setText('выбрать')
        self.editButton.setMinimumWidth(120)
        self.editButton.clicked.connect(self.editButtonClicked)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    config.mainFont = 'Century Gothic'
    window = SelectWindow()
    window.show()
    sys.exit(app.exec_())
