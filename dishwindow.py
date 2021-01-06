from PyQt5.QtWidgets import (
                                QWidget, QPushButton,
                                QLabel, QTableWidget,
                                QLineEdit, QTableWidgetItem,
                                QHBoxLayout, QVBoxLayout,
                                QGridLayout, QHeaderView,
                                QAbstractItemView, QTextEdit
                            )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import mainwindow
import selectwindow
import controller
import config

windowObject = ''

colors = []
mainFont = ''
postfixCost = ''
postfixPrice = ''
postfixWeight = ''


def _setConfigs():
    """
        Sets the global settings of  mainwindow using the config.py
    """
    global colors, mainFont, postfixCost, postfixPrice, postfixWeight
    colors = config.colors
    mainFont = config.mainFont
    postfixCost = config.postfixCost
    postfixPrice = config.postfixPrice
    postfixWeight = config.postfixWeight


class DishWindow(QWidget):
    def __init__(self):
        global windowObject
        windowObject = self
        super().__init__()
        _setConfigs()

        self.dishName = ''
        self.recipe = ''
        self.productList = []
        self.markup = 100
        self.totalValue = 0
        self.totalWeight = 0

        self.markupField = QLineEdit()
        self.markupLabel = QLabel()
        self.saveButton = QPushButton()
        self.changeButton = QPushButton()
        self.backButton = QPushButton()
        self.dishNameInput = QLineEdit()
        self.recipeLabel = QLabel()
        self.recipeField = QTextEdit()
        self.productTable = QTableWidget()
        self.totalLabel = QLabel()
        self.dishWeight = QLabel()
        self.dishCost = QLabel()

        self.mainGLayout = QGridLayout()

        self.dishSelectingVLayout = QVBoxLayout()
        self.markupFieldVLayout = QVBoxLayout()
        self.addButtonHLayout = QHBoxLayout()
        self.recipeVLayout = QVBoxLayout()
        self.productTableVLayout = QVBoxLayout()
        self.totalHLayout = QHBoxLayout()

        self.layoutWidgets()
        self.initWidgets()

    def closeEvent(self, QCloseEvent):
        controller.save()
        self.close()

    def showEvent(self, QShowEvent):
        self.show()
        self.loadParameters()

    def _loadFromController(self):
        """
            Updates the dishNameInput, markupField and recipeField using the controller
        Uses:
            imported module controller.py
        Changes:
            objects markupField, recipeField, dishNameInput
        """
        self.dishNameInput.setText(controller.getCurrentDishName())
        self.markupField.setText(str(controller.getCurrentDishMarkup()))
        self.recipeField.setText(controller.getCurrentDishRecipe())

    def _loadFromMainwindow(self):
        """
            Loads the productTable using mainwindow
            Updates the totalValue, totalWeight, productList using mainwindow
        Uses:
            imported module mainwindow
        Changes:
            objects productTable
            parameters totalValue, totalWeight, productList
        """
        mainTable = mainwindow.windowObject.productTable
        self.productTable.setRowCount(0)
        self.totalValue = mainwindow.windowObject.currentTotals['cost']
        self.totalWeight = mainwindow.windowObject.currentTotals['weight']

        self.productList = []
        mainList = mainwindow.windowObject.productList
        for name in mainList:
            self.productList.append((name, mainList[name]))
        self.productTable.setRowCount(mainTable.rowCount())

        for row in range(mainTable.rowCount()):
            name = mainTable.item(row, 0).text()
            weight = int(mainTable.item(row, 1).text().split()[0])
            cost = float(mainTable.item(row, 3).text().split()[0])
            self.addToTable(row, name, weight, cost)

    def saveButtonClicked(self):
        controller.removeDish(controller.getCurrentDishName())
        if self.dishName == '':
            self.dishName = 'newDish'
        controller.setCurrentName(self.dishName)
        controller.setCurrentDishMarkup(self.markup)
        controller.setCurrentDishRecipe(self.recipe)
        controller.setCurrentDishProducts(self.productList)
        controller.saveCurrentDish()

    def changeButtonClicked(self):
        selectwindow.windowObject.show()
        self.hide()

    def backButtonClicked(self):
        mainwindow.windowObject.show()
        self.hide()

    def dishNameChanged(self):
        """
            Called when the dishNameInput's text changes
            Updates the dishName with dishNameInput
        Uses:
            object dishNameInput
        Changes:
            parameter dishName
        """
        self.dishName = self.dishNameInput.text()
        if self.dishName == '':
            self.dishName = 'new dish'

    def recipeChanged(self):
        """
            Called when the recipeField's text changes
            Updates the recipe with recipeField
        Uses:
            object recipeField
        Changes:
            parameter recipe
        """
        self.recipe = self.recipeField.toPlainText()

    def markupChanged(self):
        """
            Called when the markupField's text changes
            Tries to update the markup with markupField
        Uses:
            object markupField
        Changes:
            parameter markup
        """
        try:
            markup_ = round(float(self.markupField.text()), 2)
            self.markup = markup_
            self.updateTotals()
        except ValueError as e:
            self.markup = 0
            self.updateTotals()
            print(e)

    def updateTotals(self):
        """
            Updates the dishCost and the dishWeight with the totalValue and the totalWeight
        Uses:
            parameters totalValue, totalWeight
        Changes:
            objects dishWeight, dishCost
        """
        totalCost = round(self.totalValue + (self.markup/100 * self.totalValue), 2)
        totalWeight = self.totalWeight
        self.dishCost.setText(str(totalCost) + postfixCost)
        self.dishWeight.setText(str(totalWeight) + postfixWeight)

    def loadParameters(self):
        self._loadFromMainwindow()
        self._loadFromController()

    def addToTable(self, row: int, name: str, weight: int, cost: float):
        """
            Adds the current product to the productTable
        Uses:
            global parameters postfixWeight, postfixPrice, postfixCost, mainFont
        Changes:
            object productTable
        :param row: row number for adding the product
        :param name: name of product
        :param weight: weight of product
        :param cost: cost of product
        """
        global postfixWeight, postfixCost, mainFont
        name = str(name)
        weight = str(weight) + postfixWeight
        cost = str(cost) + postfixCost
        print(name, weight, cost)

        self.productTable.setRowCount(row + 1)

        font = QFont(mainFont)
        font.setPointSize(14)

        item = QTableWidgetItem(name)
        item.setFont(font)
        self.productTable.setItem(row, 0, item)

        item = QTableWidgetItem(weight)
        item.setFont(font)
        self.productTable.setItem(row, 1, item)

        item = QTableWidgetItem(cost)
        item.setFont(font)
        self.productTable.setItem(row, 2, item)

    def layoutWidgets(self):
        """
            Distributes all of the widgets on the layout
        """
        mainGLayout = self.mainGLayout
        mainGLayout.addLayout(self.dishSelectingVLayout, 1, 0, 3, 3)
        mainGLayout.addWidget(self.backButton, 2, 6, 2, 2)
        mainGLayout.addLayout(self.markupFieldVLayout, 1, 10, 3, 2)
        mainGLayout.addLayout(self.productTableVLayout, 4, 0, 12, 15)
        mainGLayout.addLayout(self.recipeVLayout, 1, 16, 15, 30)

        markupFieldVLayout = self.markupFieldVLayout
        markupFieldVLayout.addSpacing(23)
        markupFieldVLayout.addWidget(self.markupLabel)
        markupFieldVLayout.addWidget(self.markupField)
        markupFieldVLayout.addSpacing(20)

        dishSelectingVLayout = self.dishSelectingVLayout
        dishSelectingVLayout.setSpacing(10)
        dishSelectingVLayout.addWidget(self.dishNameInput)
        dishSelectingVLayout.addWidget(self.saveButton)
        dishSelectingVLayout.addWidget(self.changeButton)

        recipeVLayout = self.recipeVLayout
        recipeVLayout.addWidget(self.recipeLabel)
        recipeVLayout.addWidget(self.recipeField)

        productTableVLayout = self.productTableVLayout
        productTableVLayout.setSpacing(0)
        productTableVLayout.setContentsMargins(0, 10, 0, 0)
        productTableVLayout.addWidget(self.productTable)
        productTableVLayout.addLayout(self.totalHLayout)

        totalHLayout = self.totalHLayout
        totalHLayout.addSpacing(1)
        totalHLayout.addWidget(self.totalLabel)
        totalHLayout.addWidget(self.dishWeight)
        totalHLayout.addWidget(self.dishCost)
        totalHLayout.addSpacing(1)
        totalHLayout.setSpacing(0)

        self.setLayout(mainGLayout)

    def initWidgets(self):
        """
            Sets parameters for all widgets
        """
        font = QFont(mainFont)
        font.setBold(False)
        color0 = colors[0]
        color1 = colors[1]
        color2 = colors[2]
        color3 = colors[3]

        self.setFixedSize(912, 600)
        self.setStyleSheet('background-color: {0};'.format(color1))
        self.setWindowTitle('Блюдо')
        self.setWindowIcon(QIcon('images/dish_icon.png'))

        # field for input the markup
        font.setBold(False)
        font.setPointSize(14)
        self.markupField.setFont(font)
        self.markupField.setObjectName('markupField')
        self.markupField.setAlignment(Qt.AlignCenter)
        self.markupField.setPlaceholderText('%')
        self.markupField.setStyleSheet('background-color: {0};'
                                       'border: 2px solid black;'
                                       'border-radius: 10;'.format(color3)
                                       )
        self.markupField.setFixedSize(100, 30)
        self.markupField.setMaxLength(4)
        self.markupField.textChanged.connect(self.markupChanged)

        # label over the markupField
        font.setBold(True)
        font.setPointSize(12)
        self.markupLabel.setFont(font)
        self.markupLabel.setObjectName('markupLabel')
        self.markupLabel.setAlignment(Qt.AlignCenter)
        self.markupLabel.setText('Наценка')
        self.markupLabel.setFixedSize(100, 30)

        # name of the dish
        font.setBold(True)
        font.setPointSize(12)
        self.dishNameInput.setFont(font)
        self.dishNameInput.setObjectName('dishNameInput')
        self.dishNameInput.setAlignment(Qt.AlignCenter)
        self.dishNameInput.setFixedSize(140, 22)
        self.dishNameInput.textChanged.connect(self.dishNameChanged)

        # button to save the dish
        font.setBold(False)
        font.setPointSize(9)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName('saveButton')
        self.saveButton.setStyleSheet('background-color: ' + color0 + ';')
        self.saveButton.setText('сохранить блюдо')
        self.saveButton.setFixedSize(140, 30)
        self.saveButton.clicked.connect(self.saveButtonClicked)

        # button to change the dish
        font.setBold(False)
        font.setPointSize(9)
        self.backButton.setFont(font)
        self.backButton.setObjectName('backButton')
        self.backButton.setStyleSheet('background-color: ' + color0 + ';')
        self.backButton.setText('изменить список')
        self.backButton.setFixedSize(140, 30)
        self.backButton.clicked.connect(self.backButtonClicked)

        # button to change the dish
        font.setBold(False)
        font.setPointSize(9)
        self.changeButton.setFont(font)
        self.changeButton.setObjectName('changeButton')
        self.changeButton.setStyleSheet('background-color: ' + color0 + ';')
        self.changeButton.setText('сменить блюдо')
        self.changeButton.setFixedSize(140, 30)
        self.changeButton.clicked.connect(self.changeButtonClicked)

        # table of added products
        self.productTable.setMinimumHeight(400)
        self.productTable.setFixedWidth(495)
        font.setBold(False)
        font.setPointSize(13)
        self.productTable.setFont(font)
        self.productTable.setObjectName('productTable')
        self.productTable.setStyleSheet('background-color:' + color3 + ';')
        self.productTable.setColumnCount(3)
        self.productTable.setHorizontalHeaderLabels(['продукт', 'вес', 'стоимость'])
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setColumnWidth(1, 100)
        self.productTable.setColumnWidth(2, 130)
        header = self.productTable.horizontalHeader()
        header.setFont(font)
        header.setStyleSheet('::section{Background-color:' + color2 + '}')
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.productTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # field to input the recipe of the dish
        self.recipeField.setMinimumSize(100, 300)
        font.setBold(False)
        font.setPointSize(13)
        self.recipeField.setFont(font)
        self.recipeField.setObjectName('recipeField')
        self.recipeField.setStyleSheet('background-color: {0};'.format(color3))
        self.recipeField.setAlignment(Qt.AlignTop)
        self.recipeField.setPlaceholderText('Это рецепт. Тут должно быть написано, как готовить выбранное блюдо.')
        self.recipeField.textChanged.connect(self.recipeChanged)

        # label over the recipe
        self.recipeLabel.setMinimumSize(100, 20)
        font.setBold(True)
        font.setPointSize(13)
        self.recipeLabel.setFont(font)
        self.recipeLabel.setObjectName('recipeLabel')
        self.recipeLabel.setText('Рецепт')
        self.recipeLabel.setAlignment(Qt.AlignCenter)

        # label total
        self.totalLabel.setFixedSize(264, 40)
        font.setBold(False)
        self.totalLabel.setObjectName('totalLabel')
        font.setPointSize(13)
        self.totalLabel.setFont(font)
        self.totalLabel.setAlignment(Qt.AlignCenter)
        self.totalLabel.setText('Итого')
        self.totalLabel.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color2))

        # total weight of the dish
        self.dishWeight.setFixedSize(100, 40)
        font.setBold(False)
        self.dishWeight.setObjectName('dishWeight')
        font.setPointSize(13)
        self.dishWeight.setFont(font)
        self.dishWeight.setAlignment(Qt.AlignCenter)
        self.dishWeight.setText('')
        self.dishWeight.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))

        # total cost of the dish
        self.dishCost.setFixedSize(130, 40)
        font.setBold(False)
        self.dishCost.setObjectName('dishCost')
        font.setPointSize(13)
        self.dishCost.setFont(font)
        self.dishCost.setAlignment(Qt.AlignCenter)
        self.dishCost.setText('')
        self.dishCost.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    config.mainFont = 'Century Gothic'
    window = DishWindow()
    window.show()
    sys.exit(app.exec_())
