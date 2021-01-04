from PyQt5.QtWidgets import (
                                QWidget, QPushButton,
                                QComboBox, QLabel, QTableWidget,
                                QLineEdit, QTableWidgetItem,
                                QHBoxLayout, QVBoxLayout,
                                QGridLayout, QHeaderView,
                                QAbstractItemView,
                            )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import editwindow
import controller
from config import InputError
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


class MainWindow(QWidget):
    def __init__(self):  # TODO: Add the dishButton that will be show the dishWindow!
        global windowObject
        windowObject = self
        super().__init__()
        _setConfigs()

        self.productList = []
        self.counterProducts = 0
        self.currentProduct = {'name': '', 'price': 0, 'cost': 0.00, 'weight': 0}
        self.currentGroup = ''
        self.currentTotals = {'weight': 0, 'cost': 0.00}

        self.groupBox = QComboBox()
        self.groupLabel = QLabel()
        self.productBox = QComboBox()
        self.productLabel = QLabel()
        self.editButton = QPushButton()
        self.weightInput = QLineEdit()
        self.weightLabel = QLabel()
        self.priceCurrent = QLabel()
        self.priceLabel = QLabel()
        self.costCurrent = QLabel()
        self.costLabel = QLabel()
        self.addButton = QPushButton()
        self.productTable = QTableWidget()
        self.totalLabel = QLabel()
        self.totalWeight = QLabel()
        self.totalCost = QLabel()

        self.mainGLayout = QGridLayout()

        self.currentParametersHLayout = QHBoxLayout()
        self.productSelectingVLayout = QVBoxLayout()
        self.editButtonVLayout = QVBoxLayout()
        self.weightInputVLayout = QVBoxLayout()
        self.priceCurrentVLayout = QVBoxLayout()
        self.costCurrentVLayout = QVBoxLayout()
        self.addButtonHLayout = QHBoxLayout()
        self.productTableVLayout = QVBoxLayout()
        self.totalHLayout = QHBoxLayout()

        self.layoutWidgets()
        self.initWidgets()
        self.updateGroupBox()
        self.updateTotals()

    def closeEvent(self, QCloseEvent):
        editwindow.windowObject.close()
        controller.save()
        self.close()

    def updateGroupBox(self):
        """
            Updates the groupBox using the imported dictionary product.groups
        Uses:
            imported dictionary product.groups
        """
        self.groupBox.clear()
        for group in controller.getGroups():
            self.groupBox.addItem(group)

    def updateProductBox(self):
        """
            Updates the productBox using the imported controller
        Uses:
            parameter currentGroup
            imported dictionary product.groups
        Changes:
             object productBox
        """
        self.productBox.clear()
        for product in controller.getProducts(self.currentGroup):
            productName = controller.getProducts(self.currentGroup)[product][0]
            self.productBox.addItem(productName)

    def updateCurrentParameters(self):
        """
            Updates the current price and the current cost using the productBox and the weightInput
        Uses:
            dictionary currentProduct
            global parameters postfixPrice, postfixCost
            imported dictionary product.groups
            object weightInput
        Changes:
            objects priceCurrent, costCurrent
        """
        global postfixPrice, postfixCost
        productName = self.currentProduct['name']
        if productName != '':
            price = self.currentProduct['price']
            cost = self.currentProduct['cost']
            self.priceCurrent.setText(str(price) + postfixPrice)
            self.costCurrent.setText(str(cost) + postfixCost)
        else:
            self.priceCurrent.setText('0')
            self.costCurrent.setText('0')

    def updateTotals(self):
        """
            Updates the totalWeight and the totalCost using the currentTotals
        Uses:
            dictionary currentTotals
            global parameters postfixCost, postfixWeight
        Changes:
            objects totalWeight, totalCost
        """
        global postfixCost, postfixWeight

        cost = self.currentTotals['cost']
        weight = self.currentTotals['weight']
        self.totalCost.setText(str(cost) + postfixCost)
        self.totalWeight.setText(str(weight) + postfixWeight)

    def groupChanged(self):
        """
            Called when the group changes or called by the editwindow.EditWindow.addProduct function
            Updates the currentGroup parameter using the groupBox
        Uses:
            object groupBox
        Changes:
            parameter currentGroup
        Calls:
            function updateProductBox
        """
        self.currentGroup = self.groupBox.currentText()
        self.updateProductBox()

    def productChanged(self):
        """
            Called when the product changes
            Updates the currentProduct['name'] parameter using the productBox
            Updates the currentProduct['price'] parameter using the imported module controller
        Uses:
            object productBox
            imported module controller
        Changes:
            parameters currentProduct['name'], currentProduct['price']
        Calls:
            function updateCurrentParameters
        """
        name = self.productBox.currentText()
        self.currentProduct['name'] = name
        try:
            self.currentProduct['price'] = controller.getProducts(self.currentGroup)[name.lower()][1]
        except KeyError:
            self.currentProduct['price'] = 0
        self.weightChanged()
        self.updateCurrentParameters()

    def weightChanged(self):
        """
            Called when the weight changes
            Updates the currentProduct['weight'] parameter
            Updates the currentProduct['cost'] parameter
        Uses:
            object productBox
            dictionary currentProduct
        Changes:
            parameters currentProduct['weight'], currentProduct['cost']
        Calls:
            function updateCurrentParameters
        """
        try:
            weight = int(self.weightInput.text())
            if weight < 0:
                raise InputError
        except (InputError, ValueError):
            print('weight is error')
            weight = 0
        self.currentProduct['weight'] = weight
        price = self.currentProduct['price']
        self.currentProduct['cost'] = round(weight * price / 1000, 2)
        print(weight, price, self.currentProduct['cost'])
        self.updateCurrentParameters()

    def loadTableFromController(self):
        """
            Loads the productTable using the controller
        Uses:
            imported module controller
            object addButton
        Changes:
            object productTable, groupBox, productBox, weightInput
        """
        if self.counterProducts > 0:
            for row in range(self.counterProducts):
                self.productTable.cellWidget(0, 4).clicked.emit()
        for product in controller.getCurrentDishProducts():
            name = controller.getProducts()[product[0]][0]
            weight = product[1]
            self.groupBox.setCurrentText('Все')
            self.productBox.setCurrentText(name)
            self.weightInput.setText(str(weight))
            self.addButton.clicked.emit()

    def addExistingProduct(self, row):
        """
            Does the same thing as the "add product" function, but for for an already added product.
            Adds the weight and cost of the product to the one already in the table.
        :param row: index of the line required to add an existing product
        """

        self.currentTotals['cost'] = round(self.currentTotals['cost'] + self.currentProduct['cost'], 2)
        self.currentTotals['weight'] += self.currentProduct['weight']
        self.updateTotals()
        weight = int(self.productTable.item(row, 1).text().split()[0]) + self.currentProduct['weight']
        cost = float(self.productTable.item(row, 3).text().split()[0]) + self.currentProduct['cost']
        cost = round(cost, 2)

        item = QTableWidgetItem(str(weight) + postfixWeight)
        self.productTable.setItem(row, 1, item)
        item = QTableWidgetItem(str(cost) + postfixCost)
        self.productTable.setItem(row, 3, item)

    def addProduct(self):
        """
            Called when the addButton pushed
            Gets parameters of the current product and send them to the addToTable function
            Creates a delButton with number=row that deletes this row and send it to the addToTable function
        Uses:
            dictionary currentProduct
        Changes:
            dictionary currentTotals
            parameter counterProducts
        Calls:
            functions updateTotals, addToTable, addExistingProduct
        """
        name = self.currentProduct['name']
        price = self.currentProduct['price']
        cost = self.currentProduct['cost']
        weight = self.currentProduct['weight']

        for row, item in enumerate(self.productList):
            print(name, row, item)
            if name == item:
                self.addExistingProduct(row)
                return
        try:
            if name == '' or weight == 0:
                raise InputError('Can\'t add')

            self.currentTotals['cost'] = round(self.currentTotals['cost'] + cost, 2)
            self.currentTotals['weight'] += weight
            self.updateTotals()

            self.counterProducts += 1
            self.productList.append(name)
            print(name + ' need to add')
            row = self.counterProducts - 1

            delButton = QPushButton()
            delButton.setStyleSheet('background-color: #e03f3f;')
            delButton.setIcon(QIcon('images/delete_icon.png'))
            delButton.setIconSize(QSize(20, 20))
            delButton.number = row
            delButton.clicked.connect(self.deleteProduct)

            self.addToTable(row, name, weight, price, cost, delButton)
        except InputError as e:
            print(e)

    def addToTable(self, row: int, name: str, weight: int, price: int, cost: float, delButton: QPushButton):
        """
            Adds the current product to the productTable
        Uses:
            global parameters postfixWeight, postfixPrice, postfixCost, mainFont
        Changes:
            object productTable
        :param row: row number for adding the product
        :param name: name of product
        :param weight: weight of product
        :param price: price of product
        :param cost: cost of product
        :param delButton: object created by addProduct
        """
        global postfixWeight, postfixPrice, postfixCost, mainFont
        name = str(name)
        weight = str(weight) + postfixWeight
        price = str(price) + postfixPrice
        cost = str(cost) + postfixCost

        self.productTable.setRowCount(row + 1)

        font = QFont(mainFont)
        font.setPointSize(14)

        item = QTableWidgetItem(name)
        item.setFont(font)
        self.productTable.setItem(row, 0, item)

        item = QTableWidgetItem(weight)
        item.setFont(font)
        self.productTable.setItem(row, 1, item)

        item = QTableWidgetItem(price)
        item.setFont(font)
        self.productTable.setItem(row, 2, item)

        item = QTableWidgetItem(cost)
        item.setFont(font)
        self.productTable.setItem(row, 3, item)

        self.productTable.setCellWidget(row, 4, delButton)

    def deleteProduct(self):
        """
            Called when one of the delButtons pushed
            Deletes a row in the productTable with the delButton number
        Changes:
            parameter counterProducts
            dictionary currentTotals
            objects productTable, totalWeight, totalCost
        Calls:
            function updateTotals
        """
        row = self.sender().number

        weight = int(self.productTable.item(row, 1).text().split()[0])
        cost = round(float(self.productTable.item(row, 3).text().split()[0]), 2)
        self.currentTotals['weight'] -= weight
        self.currentTotals['cost'] = round(self.currentTotals['cost'] - cost, 2)
        self.updateTotals()

        self.productTable.removeRow(row)
        self.counterProducts -= 1
        if row != self.counterProducts:
            for r in range(row, self.counterProducts):
                self.productTable.cellWidget(r, 4).number -= 1

    def layoutWidgets(self):
        """
            Distributes all of the widgets on the layout
        """
        mainGLayout = self.mainGLayout
        mainGLayout.addLayout(self.currentParametersHLayout, 1, 0, 2, 20)
        mainGLayout.addLayout(self.productTableVLayout, 4, 0, 11, 20)

        currentParametersHLayout = self.currentParametersHLayout
        currentParametersHLayout.addLayout(self.editButtonVLayout)
        currentParametersHLayout.addLayout(self.productSelectingVLayout)
        currentParametersHLayout.addLayout(self.weightInputVLayout)
        currentParametersHLayout.addLayout(self.priceCurrentVLayout)
        currentParametersHLayout.addLayout(self.costCurrentVLayout)

        productSelectingVLayout = self.productSelectingVLayout
        productSelectingVLayout.addWidget(self.groupLabel)
        productSelectingVLayout.addWidget(self.groupBox)
        productSelectingVLayout.addWidget(self.productLabel)
        productSelectingVLayout.addWidget(self.productBox)
        productSelectingVLayout.addSpacing(10)
        productSelectingVLayout.addWidget(self.addButton)
        productSelectingVLayout.addSpacing(10)

        editButtonVLayout = self.editButtonVLayout
        editButtonVLayout.addSpacing(35)
        editButtonVLayout.addWidget(self.editButton)
        editButtonVLayout.addSpacing(0)

        weightInputVLayout = self.weightInputVLayout
        weightInputVLayout.addSpacing(30)
        weightInputVLayout.addWidget(self.weightLabel)
        weightInputVLayout.addWidget(self.weightInput)
        weightInputVLayout.addSpacing(50)

        priceCurrentVLayout = self.priceCurrentVLayout
        priceCurrentVLayout.addSpacing(30)
        priceCurrentVLayout.addWidget(self.priceLabel)
        priceCurrentVLayout.addWidget(self.priceCurrent)
        priceCurrentVLayout.addSpacing(50)

        costCurrentVLayout = self.costCurrentVLayout
        costCurrentVLayout.addSpacing(30)
        costCurrentVLayout.addWidget(self.costLabel)
        costCurrentVLayout.addWidget(self.costCurrent)
        costCurrentVLayout.addSpacing(50)

        productTableVLayout = self.productTableVLayout
        productTableVLayout.setSpacing(0)
        productTableVLayout.setContentsMargins(0, 10, 0, 0)
        productTableVLayout.addWidget(self.productTable)
        productTableVLayout.addLayout(self.totalHLayout)

        totalHLayout = self.totalHLayout
        totalHLayout.addWidget(self.totalLabel)
        totalHLayout.addWidget(self.totalWeight)
        totalHLayout.addWidget(self.totalCost)
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

        self.setFixedSize(612, 600)
        self.setStyleSheet('background-color: {0};'.format(color1))
        self.setWindowTitle('Технологическая карта')
        self.setWindowIcon(QIcon('images/tomato_icon.png'))

        # comboBox for selecting a product group
        font.setBold(False)
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName('groupBox')
        self.groupBox.setStyleSheet('background-color: {0};'
                                    'border: 2px solid black;'
                                    'border-radius: 3;'.format(color3)
                                    )
        self.groupBox.setFixedSize(175, 22)
        self.groupBox.currentIndexChanged.connect(self.groupChanged)

        # label over the groupBox
        font.setBold(False)
        font.setPointSize(14)
        self.groupLabel.setFont(font)
        self.groupLabel.setObjectName('groupLabel')
        self.groupLabel.setFixedSize(175, 20)
        self.groupLabel.setAlignment(Qt.AlignCenter)
        self.groupLabel.setText('группа')

        # comboBox for product selection
        font.setBold(False)
        font.setPointSize(12)
        self.productBox.setFont(font)
        self.productBox.setObjectName('productBox')
        self.productBox.setStyleSheet('background-color: {0};'
                                      'border: 2px solid black;'
                                      'border-radius: 3;'.format(color3)
                                      )
        self.productBox.setFixedSize(175, 22)
        self.productBox.setPlaceholderText(' ')
        self.productBox.currentIndexChanged.connect(self.productChanged)

        # label over the productBox
        font.setBold(False)
        font.setPointSize(14)
        self.productLabel.setFont(font)
        self.productLabel.setObjectName('productLabel')
        self.productLabel.setAlignment(Qt.AlignCenter)
        self.productLabel.setText('продукт')
        self.productLabel.setFixedSize(175, 20)

        # button to open the editWindow
        font.setBold(False)
        font.setPointSize(14)
        self.editButton.setFont(font)
        self.editButton.setObjectName('editButton')
        self.editButton.setIcon(QIcon('images/edit_icon.png'))
        self.editButton.setIconSize(QSize(13, 13))
        self.editButton.setStyleSheet('background-color: ' + color2 + ';')
        self.editButton.setFixedSize(20, 20)
        self.editButton.clicked.connect(editwindow.windowObject.show)

        # field for input the product weight
        font.setBold(False)
        font.setPointSize(14)
        self.weightInput.setFont(font)
        self.weightInput.setObjectName('weightInput')
        self.weightInput.setAlignment(Qt.AlignCenter)
        self.weightInput.setPlaceholderText('грамм')
        self.weightInput.setStyleSheet('background-color: {0};'
                                       'border: 2px solid black;'
                                       'border-radius: 10;'.format(color3)
                                       )
        self.weightInput.setFixedSize(100, 30)
        self.weightInput.setMaxLength(4)
        self.weightInput.textChanged.connect(self.weightChanged)

        # label over the weightInput
        font.setBold(False)
        font.setPointSize(14)
        self.weightLabel.setFont(font)
        self.weightLabel.setObjectName('weightLabel')
        self.weightLabel.setAlignment(Qt.AlignCenter)
        self.weightLabel.setText('вес')
        self.weightLabel.setFixedSize(100, 30)

        # field showing the price of the current product
        font.setBold(False)
        font.setPointSize(14)
        self.priceCurrent.setFont(font)
        self.priceCurrent.setObjectName('priceCurrent')
        self.priceCurrent.setAlignment(Qt.AlignCenter)
        self.priceCurrent.setStyleSheet('background-color: {0};'
                                        'border: 2px solid black;'
                                        'border-radius: 3;'.format(color3)
                                        )
        self.priceCurrent.setFixedSize(120, 30)

        # label over the priceCurrent
        font.setBold(False)
        font.setPointSize(14)
        self.priceLabel.setFont(font)
        self.priceLabel.setObjectName('priceLabel')
        self.priceLabel.setAlignment(Qt.AlignCenter)
        self.priceLabel.setText('цена')
        self.priceLabel.setFixedSize(120, 30)

        # field showing the cost of the product considering the weight
        font.setBold(False)
        font.setPointSize(14)
        self.costCurrent.setFont(font)
        self.costCurrent.setObjectName('costCurrent')
        self.costCurrent.setAlignment(Qt.AlignCenter)
        self.costCurrent.setStyleSheet('background-color: {0};'
                                       'border: 2px solid black;'
                                       'border-radius: 3;'.format(color3)
                                       )
        self.costCurrent.setFixedSize(120, 30)

        # label over the costCurrent
        font.setBold(False)
        font.setPointSize(13)
        self.costLabel.setFont(font)
        self.costLabel.setObjectName('costLabel')
        self.costLabel.setAlignment(Qt.AlignCenter)
        self.costLabel.setText('итого')
        self.costLabel.setFixedSize(120, 30)

        # button to add the current product to the product table
        font.setBold(False)
        font.setPointSize(11)
        self.addButton.setFont(font)
        self.addButton.setObjectName('addButton')
        self.addButton.setStyleSheet('background-color: ' + color0 + ';')
        self.addButton.setText('добавить')
        self.addButton.setFixedSize(120, 30)
        self.addButton.clicked.connect(self.addProduct)

        # table of added products
        self.productTable.setFixedHeight(370)
        self.productTable.setFixedWidth(585)
        font.setBold(False)
        font.setPointSize(13)
        self.productTable.setFont(font)
        self.productTable.setObjectName('productTable')
        self.productTable.setStyleSheet('background-color:' + color3 + ';')
        self.productTable.setColumnCount(5)
        self.productTable.setHorizontalHeaderLabels(['продукт', 'вес', 'цена', 'стоимость', ''])
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setColumnWidth(0, 180)
        self.productTable.setColumnWidth(1, 75)
        self.productTable.setColumnWidth(2, 120)
        self.productTable.setColumnWidth(3, 140)
        header = self.productTable.horizontalHeader()
        header.setFont(font)
        header.setStyleSheet('::section{Background-color:' + color2 + '}')
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.productTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # label total
        self.totalLabel.setFixedSize(180, 40)
        font.setBold(False)
        self.totalLabel.setObjectName('totalLabel')
        font.setPointSize(13)
        self.totalLabel.setFont(font)
        self.totalLabel.setAlignment(Qt.AlignCenter)
        self.totalLabel.setText('Итого')
        self.totalLabel.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color2))

        # total weight of all products
        self.totalWeight.setFixedSize(195, 40)
        font.setBold(False)
        self.totalWeight.setObjectName('totalWeight')
        font.setPointSize(13)
        self.totalWeight.setFont(font)
        self.totalWeight.setAlignment(Qt.AlignCenter)
        self.totalWeight.setText('')
        self.totalWeight.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))

        # total cost of all products
        self.totalCost.setFixedSize(210, 40)
        font.setBold(False)
        self.totalCost.setObjectName('totalCost')
        font.setPointSize(13)
        self.totalCost.setFont(font)
        self.totalCost.setAlignment(Qt.AlignCenter)
        self.totalCost.setText('')
        self.totalCost.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    controller.load()
    config.mainFont = 'Century Gothic'
    editWindow = editwindow.EditWindow()
    window = MainWindow()
    window.show()
    controller.loadDish('саЛат')
    window.loadTableFromController()
    controller.loadDish('суп')
    window.loadTableFromController()
    sys.exit(app.exec_())
