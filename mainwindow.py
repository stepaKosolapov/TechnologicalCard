from PyQt5.QtWidgets import (
                            QWidget, QPushButton,
                            QComboBox, QLabel, QTableWidget,
                            QLineEdit,
                            QHBoxLayout, QVBoxLayout,
                            QGridLayout, QHeaderView,
                            QAbstractItemView,
                            )
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import products


colors = ['#8ab82e', '#77d496', '#dec476', '#DBD7D2']
mainFont = 'Times New Roman'
currency = ' руб'
postfixCost = currency
postfixPrice = postfixCost + '/кг'
postfixWeight = ' г'
counterProducts = 0
currentProduct = {'name': '', 'price': 0, 'cost': 0.0, 'weight': 0}
currentGroup = ''


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        self.totalSum = QLabel()

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
        self.show()
        self.updateGroupBox()

    def updateGroupBox(self):
        """
            Updates the groupBox using the imported dictionary product.groups
        Uses:
            imported dictionary product.groups
        """
        groupBox = self.groupBox
        groupBox.clear()
        for group in products.groups:
            groupBox.addItem(group)

    def updateProductBox(self):
        """
            Updates the productBox using the imported dictionary products.groups
        Uses:
            global parameter currentGroup
            imported dictionary product.groups
        Changes:
             object productBox
        """
        global currentGroup
        productBox = self.productBox
        productBox.clear()
        for product in products.groups[currentGroup]['products']:
            productName = products.groups[currentGroup]['products'][product][0]
            productBox.addItem(productName)

    def updateCurrentParameters(self):
        """
            Updates current price and current cost using the productBox and the weightInput
        Uses:
            global dictionary currentProduct
            global parameters currentGroup, postfixPrice, postfixCost
            imported dictionary product.groups
            object weightInput
        Changes:
            objects priceCurrent, costCurrent
        """
        global currentProduct, currentGroup, postfixPrice, postfixCost
        priceCurrent = self.priceCurrent
        costCurrent = self.costCurrent
        productName = currentProduct['name']
        if productName != '':
            price = currentProduct['price']
            cost = currentProduct['cost']
            priceCurrent.setText(str(price) + postfixPrice)
            costCurrent.setText(str(cost) + postfixCost)
        else:
            priceCurrent.setText('0')
            costCurrent.setText('0')

    def groupChanged(self):
        """
            Called when the group changes.
            Updates the global parameter currentGroup using the groupBox
        Uses:
            object groupBox
        Changes:
            global parameter currentGroup
        Calls:
            function updateProductBox
        """
        global currentGroup
        groupBox = self.groupBox
        currentGroup = groupBox.currentText()
        self.updateProductBox()

    def productChanged(self):
        """
            Called when the product changes
            Updates global parameter currentProduct['name'] using the productBox
            Updates global parameter currentProduct['price'] using the imported dictionary product.groups
        Uses:
            object productBox
            imported dictionary product.groups
        Changes:
            global parameter currentProduct['name'], currentProduct['price']
        Calls:
            function updateCurrentParameters
        """
        global currentProduct
        productBox = self.productBox
        name = productBox.currentText()
        currentProduct['name'] = name
        try:
            currentProduct['price'] = products.groups[currentGroup]['products'][name][1]
        except KeyError:
            currentProduct['price'] = 0
        self.updateCurrentParameters()

    def weightChanged(self):
        """
            Called when the weight changes
            Updates global parameter currentProduct['weight'] using the inputWeight
            Updates global parameter currentProduct['cost'] using the global parameter currentProduct['price']
        Uses:
            object productBox
            global dictionary currentProduct
        Changes:
            global parameter currentProduct['weight'], currentProduct['cost']
        Calls:
            function updateCurrentParameters
                """
        global currentProduct
        weightInput = self.weightInput
        try:
            weight = int(weightInput.text())
        except ValueError:
            weight = 0
        currentProduct['weight'] = weight
        price = currentProduct['price']
        currentProduct['cost'] = weight * price / 1000
        self.updateCurrentParameters()

    def layoutWidgets(self):
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
        productSelectingVLayout.addWidget(self.addButton)

        editButtonVLayout = self.editButtonVLayout
        editButtonVLayout.addSpacing(46)
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
        productTableVLayout.setContentsMargins(0, 10, 0, 40)
        productTableVLayout.addWidget(self.productTable)
        productTableVLayout.addLayout(self.totalHLayout)

        totalHLayout = self.totalHLayout
        totalHLayout.addWidget(self.totalLabel)
        totalHLayout.addWidget(self.totalWeight)
        totalHLayout.addWidget(self.totalSum)
        totalHLayout.setSpacing(0)

        self.setLayout(mainGLayout)

    def initWidgets(self):
        font = QFont(mainFont)
        font.setBold(False)
        color0 = colors[0]
        color1 = colors[1]
        color2 = colors[2]
        color3 = colors[3]

        self.setFixedSize(542, 600)
        self.setStyleSheet('background-color: {0};'.format(color1))
        self.setWindowTitle('Технологическая карта')

        # comboBox for selecting a product group
        groupBox = self.groupBox
        font.setBold(False)
        font.setPointSize(15)
        groupBox.setFont(font)
        groupBox.setObjectName('groupBox')
        groupBox.setStyleSheet('background-color: {0}; border: 2px solid black; border-radius: 3;'.format(color3))
        groupBox.setFixedSize(175, 20)
        groupBox.currentIndexChanged.connect(self.groupChanged)

        # label over the groupBox
        groupLabel = self.groupLabel
        font.setBold(False)
        font.setPointSize(15)
        groupLabel.setFont(font)
        groupLabel.setObjectName('groupLabel')
        groupLabel.setFixedSize(175, 20)
        groupLabel.setAlignment(Qt.AlignCenter)
        groupLabel.setText('группа')

        # comboBox for product selection
        productBox = self.productBox
        font.setBold(False)
        font.setPointSize(15)
        productBox.setFont(font)
        productBox.setObjectName('productBox')
        productBox.setStyleSheet('background-color: {0}; border: 2px solid black; border-radius: 3;'.format(color3))
        productBox.setFixedSize(175, 20)
        productBox.currentIndexChanged.connect(self.productChanged)

        # label over the productBox
        productLabel = self.productLabel
        font.setBold(False)
        font.setPointSize(15)
        productLabel.setFont(font)
        productLabel.setObjectName('productLabel')
        productLabel.setAlignment(Qt.AlignCenter)
        productLabel.setText('продукт')
        productLabel.setFixedSize(175, 20)

        # button to open the editWindow
        editButton = self.editButton
        font.setBold(False)
        font.setPointSize(15)
        editButton.setFont(font)
        editButton.setObjectName('editButton')
        editButton.setStyleSheet('background-color: ' + color2 + ';')
        editButton.setFixedSize(20, 20)

        # field for input the product weight
        weightInput = self.weightInput
        font.setBold(False)
        font.setPointSize(15)
        weightInput.setFont(font)
        weightInput.setObjectName('weightInput')
        weightInput.setAlignment(Qt.AlignCenter)
        weightInput.setPlaceholderText('грамм')
        weightInput.setStyleSheet('background-color: {0}; border: 2px solid black; border-radius: 10;'.format(color3))
        weightInput.setFixedSize(100, 30)
        weightInput.textChanged.connect(self.weightChanged)

        # label over the weightInput
        weightLabel = self.weightLabel
        font.setBold(False)
        font.setPointSize(15)
        weightLabel.setFont(font)
        weightLabel.setObjectName('weightLabel')
        weightLabel.setAlignment(Qt.AlignCenter)
        weightLabel.setText('вес')
        weightLabel.setFixedSize(100, 30)

        # field showing the price of the current product
        priceCurrent = self.priceCurrent
        font.setBold(False)
        font.setPointSize(15)
        priceCurrent.setFont(font)
        priceCurrent.setObjectName('priceCurrent')
        priceCurrent.setAlignment(Qt.AlignCenter)
        priceCurrent.setStyleSheet('background-color: {0}; border: 2px solid black; border-radius: 3;'.format(color3))
        priceCurrent.setFixedSize(100, 30)

        # label over the priceCurrent
        priceLabel = self.priceLabel
        font.setBold(False)
        font.setPointSize(15)
        priceLabel.setFont(font)
        priceLabel.setObjectName('priceLabel')
        priceLabel.setAlignment(Qt.AlignCenter)
        priceLabel.setText('цена')
        priceLabel.setFixedSize(100, 30)

        # field showing the cost of the product considering the weight
        costCurrent = self.costCurrent
        font.setBold(False)
        font.setPointSize(15)
        costCurrent.setFont(font)
        costCurrent.setObjectName('costCurrent')
        costCurrent.setAlignment(Qt.AlignCenter)
        costCurrent.setStyleSheet('background-color: {0}; border: 2px solid black; border-radius: 3;'.format(color3))
        costCurrent.setFixedSize(100, 30)

        # label over the costCurrent
        costLabel = self.costLabel
        font.setBold(False)
        font.setPointSize(15)
        costLabel.setFont(font)
        costLabel.setObjectName('costLabel')
        costLabel.setAlignment(Qt.AlignCenter)
        costLabel.setText('итого')
        costLabel.setFixedSize(100, 30)

        # button to add the current product to the product table
        addButton = self.addButton
        font.setBold(False)
        font.setPointSize(13)
        addButton.setFont(font)
        addButton.setObjectName('addButton')
        addButton.setStyleSheet('background-color: ' + color0 + ';')
        addButton.setText('добавить')
        addButton.setFixedSize(120, 30)

        # table of added products
        productTable = self.productTable
        productTable.setFixedHeight(350)
        font.setBold(False)
        font.setPointSize(15)
        productTable.setFont(font)
        productTable.setObjectName('productTable')
        productTable.setStyleSheet('background-color:' + color3 + ';')
        productTable.setColumnCount(5)
        productTable.setHorizontalHeaderLabels(['продукт', 'вес', 'цена', 'стоимость', ''])
        productTable.verticalHeader().setVisible(False)
        productTable.setColumnWidth(0, 175)
        productTable.setColumnWidth(1, 85)
        productTable.setColumnWidth(2, 85)
        productTable.setColumnWidth(3, 120)
        header = productTable.horizontalHeader()
        header.setFont(font)
        header.setStyleSheet('::section{Background-color:' + color2 + '}')
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        productTable.setSelectionMode(QAbstractItemView.NoSelection)
        productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # label total
        totalLabel = self.totalLabel
        totalLabel.setFixedSize(175, 40)
        font.setBold(False)
        totalLabel.setObjectName('totalLabel')
        font.setPointSize(15)
        totalLabel.setFont(font)
        totalLabel.setAlignment(Qt.AlignCenter)
        totalLabel.setText('Итого')
        totalLabel.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color2))

        # total weight of all products
        totalWeight = self.totalWeight
        totalWeight.setFixedSize(170, 40)
        font.setBold(False)
        totalWeight.setObjectName('totalWeight')
        font.setPointSize(15)
        totalWeight.setFont(font)
        totalWeight.setAlignment(Qt.AlignCenter)
        totalWeight.setText('')
        totalWeight.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))

        # total weight of all products
        totalSum = self.totalSum
        totalSum.setFixedSize(175, 40)
        font.setBold(False)
        totalSum.setObjectName('totalSum')
        font.setPointSize(15)
        totalSum.setFont(font)
        totalSum.setAlignment(Qt.AlignCenter)
        totalSum.setText('')
        totalSum.setStyleSheet('background-color: {0}; border: 1px solid black;'.format(color0))
