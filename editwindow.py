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
import mainwindow
import controller
import config
from config import InputError

windowObject = ''

colors = []
mainFont = ''
postfixPrice = ''


def _setConfigs():
    """
        Sets the global settings of  editwindow using the config.py
    """
    global colors, mainFont, postfixPrice
    colors = config.colors
    mainFont = config.mainFont
    postfixPrice = config.postfixPrice


class EditWindow(QWidget):
    def __init__(self):
        global windowObject
        windowObject = self
        super().__init__()
        _setConfigs()

        self.counterProducts = 0
        self.enteredProduct = {'name': '', 'price': 0}
        self.currentGroup = ''

        self.groupBox = QComboBox()
        self.groupLabel = QLabel()
        self.nameInput = QLineEdit()
        self.nameLabel = QLabel()
        self.priceInput = QLineEdit()
        self.priceLabel = QLabel()
        self.addButton = QPushButton()
        self.productTable = QTableWidget()

        self.mainGLayout = QGridLayout()

        self.inputParametersHLayout = QHBoxLayout()
        self.productSelectingVLayout = QVBoxLayout()
        self.priceInputVLayout = QVBoxLayout()

        self.layoutWidgets()
        self.initWidgets()
        self.updateGroupBox()

    def groupChanged(self):
        """
            Called when the group changes.
            Updates the currentGroup parameter using the groupBox
        Uses:
            object groupBox
        Changes:
            parameter currentGroup
        Calls:
            function updateProductTable
        """
        self.currentGroup = self.groupBox.currentText()
        self.updateProductTable()

    def nameChanged(self):
        """
            Called when the name changes
            Updates enteredProduct['name'] parameter using the inputName
        Uses:
            object nameInput
            dictionary enteredProduct
        Changes:
            parameter enteredProduct['name']
        """
        name = self.nameInput.text()
        self.enteredProduct['name'] = name

    def priceChanged(self):
        """
            Called when the price changes
            Updates enteredProduct['price'] parameter using the inputName
        Uses:
            object priceInput
            dictionary enteredProduct
        Changes:
            parameter enteredProduct['price']
        """
        try:
            price = int(self.priceInput.text())
            if price <= 0:
                raise InputError
        except (InputError, ValueError):
            price = 0
        self.enteredProduct['price'] = price

    def updateGroupBox(self):
        """
            Updates the groupBox using the imported module controller
        Uses:
            imported module controller
        """
        self.groupBox.clear()
        for group in controller.getGroups():
            self.groupBox.addItem(group)

    def updateProductTable(self):
        """
            Clears the product table and adds all products from current group using imported module controller
        Uses:
            imported module controller
        Changes:
            parameter counterProducts
            object productTable
        Calls:
            function addProduct
        """
        self.counterProducts = 0
        self.productTable.setRowCount(0)
        for product in controller.getProducts(self.currentGroup):
            name = controller.getProducts(self.currentGroup)[product][0]
            price = controller.getProducts(self.currentGroup)[product][1]
            self.addProduct(name, price, True)

    def addProduct(self, name='', price=0, from_code=False):
        """
            Called when the addButton pushed or called by the updateProductTable function
            When the addButton pushed:
                gets parameters of the entered product and send them to the addToTable function
            When called by the updateProductTable function:
                gets parameters and send them to the addToTable function
            Creates a delButton with number=row that deletes this row and send it to the addToTable function
            Adds only if the product is not in products.csv
            Updates productBox in mainwindow
        Uses:
            dictionary enteredProduct
            imported module controller
        Changes:
            parameter counterProducts
        Calls:
            function addToTable
            method mainwindow.windowObject.updateProductBox
        """
        if not from_code:
            name = self.enteredProduct['name']
            if name.lower() in controller.getProducts():
                name = ''
            price = self.enteredProduct['price']
        try:
            if name == '' or price == 0:
                raise InputError('Can\'t add')

            self.counterProducts += 1
            row = self.counterProducts - 1

            if not from_code:
                controller.newProduct(name, price, self.currentGroup)

            delButton = QPushButton()
            delButton.setStyleSheet('background-color: #e03f3f;')
            delButton.setIcon(QIcon('images/delete_icon.png'))
            delButton.setIconSize(QSize(20, 20))
            delButton.number = row
            delButton.clicked.connect(self.deleteProduct)

            self.addToTable(row, name, price, delButton)

            if not from_code:
                self.priceInput.setText('')
                self.nameInput.setText('')
                mainWindowCurrentGroup = mainwindow.windowObject.currentGroup
                if mainWindowCurrentGroup == 'все' or mainWindowCurrentGroup == self.currentGroup:
                    mainwindow.windowObject.updateProductBox()
        except InputError as e:
            print(e)

    def addToTable(self, row: int, name: str, price: int, delButton: QPushButton):
        """
            Adds the product to the productTable
        Uses:
            global parameters postfixPrice, mainFont
        Changes:
            object productTable
        :param row: row number for adding the product
        :param name: name of product
        :param price: price of product
        :param delButton: object created by addProduct
        """
        global postfixPrice, mainFont
        name = str(name)
        price = str(price) + postfixPrice

        self.productTable.setRowCount(row + 1)

        font = QFont(mainFont)
        font.setPointSize(14)

        item = QTableWidgetItem(name)
        item.setFont(font)
        self.productTable.setItem(row, 0, item)

        item = QTableWidgetItem(price)
        item.setFont(font)
        self.productTable.setItem(row, 1, item)

        self.productTable.setCellWidget(row, 2, delButton)

    def deleteProduct(self):
        """
            Called when one of the delButtons pushed
            Deletes a row in the productTable with the delButton number
            Deletes the product from the products.csv using imported module controller
        Uses:
            imported module controller
            parameter currentGroup
        Changes:
            parameter counterProducts
            objects productTable
            products.csv
        """
        row = self.sender().number

        name = self.productTable.item(row, 0).text()

        if self.currentGroup == 'все':
            controller.removeProduct(name, 'все')
            searchedGroup = controller.searchProductGroup(name)
            if searchedGroup is not None:
                controller.removeProduct(name, searchedGroup)
        else:
            controller.removeProduct(name, self.currentGroup)
            controller.removeProduct(name, 'все')

        mainWindowCurrentGroup = mainwindow.windowObject.currentGroup
        if mainWindowCurrentGroup == 'все' or mainWindowCurrentGroup == self.currentGroup:
            mainwindow.windowObject.updateProductBox()

        self.productTable.removeRow(row)
        self.counterProducts -= 1
        if row != self.counterProducts:
            for r in range(row, self.counterProducts):
                self.productTable.cellWidget(r, 2).number -= 1

    def layoutWidgets(self):
        """
            Distributes all of the widgets on the layout
        """
        mainGLayout = self.mainGLayout
        mainGLayout.addLayout(self.inputParametersHLayout, 1, 0, 2, 10)
        mainGLayout.addWidget(self.productTable, 3, 0, 10, 10)

        inputParametersHLayout = self.inputParametersHLayout
        inputParametersHLayout.addLayout(self.productSelectingVLayout)
        inputParametersHLayout.addLayout(self.priceInputVLayout)

        productSelectingVLayout = self.productSelectingVLayout
        productSelectingVLayout.addWidget(self.groupLabel)
        productSelectingVLayout.addWidget(self.groupBox)
        productSelectingVLayout.addWidget(self.nameLabel)
        productSelectingVLayout.addWidget(self.nameInput)
        productSelectingVLayout.addSpacing(10)
        productSelectingVLayout.addWidget(self.addButton)
        productSelectingVLayout.addSpacing(10)

        priceInputVLayout = self.priceInputVLayout
        priceInputVLayout.addSpacing(30)
        priceInputVLayout.addWidget(self.priceLabel)
        priceInputVLayout.addWidget(self.priceInput)
        priceInputVLayout.addSpacing(61)

        self.setLayout(mainGLayout)

    def initWidgets(self):
        """
            Sets parameters for all widgets
        """
        global mainFont, colors, postfixPrice
        font = QFont(mainFont)
        font.setBold(False)
        color0 = colors[0]
        color1 = colors[1]
        color2 = colors[2]
        color3 = colors[3]

        self.setFixedSize(440, 600)
        self.setStyleSheet('background-color: {0};'.format(color1))
        self.setWindowTitle('Добавить продукт')
        self.setWindowIcon(QIcon('images/edit_icon.png'))

        # comboBox for selecting the group of entered product
        font.setBold(False)
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName('groupBox')
        self.groupBox.setStyleSheet('background-color: {0};'
                                    'border: 2px solid black;'
                                    'border-radius: 3;'.format(color3)
                                    )
        self.groupBox.setFixedHeight(22)
        self.groupBox.currentIndexChanged.connect(self.groupChanged)

        # label over the groupBox
        font.setBold(False)
        font.setPointSize(14)
        self.groupLabel.setFont(font)
        self.groupLabel.setObjectName('groupLabel')
        self.groupLabel.setFixedHeight(22)
        self.groupLabel.setAlignment(Qt.AlignCenter)
        self.groupLabel.setText('группа')

        # field for input the product name
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
        self.nameInput.textChanged.connect(self.nameChanged)

        # label over the nameLabel
        font.setBold(False)
        font.setPointSize(14)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName('nameLabel')
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setText('продукт')
        self.nameLabel.setFixedHeight(22)

        # field to input the product price
        font.setBold(False)
        font.setPointSize(14)
        self.priceInput.setFont(font)
        self.priceInput.setObjectName('priceInput')
        self.priceInput.setAlignment(Qt.AlignCenter)
        self.priceInput.setStyleSheet('background-color: {0};'
                                      'border: 2px solid black;'
                                      'border-radius: 3;'.format(color3)
                                      )
        self.priceInput.setFixedSize(120, 32)
        self.priceInput.setMaxLength(4)
        self.priceInput.setPlaceholderText(postfixPrice)
        self.priceInput.textChanged.connect(self.priceChanged)

        # label over the priceInput
        font.setBold(False)
        font.setPointSize(14)
        self.priceLabel.setFont(font)
        self.priceLabel.setObjectName('priceLabel')
        self.priceLabel.setAlignment(Qt.AlignCenter)
        self.priceLabel.setText('цена')
        self.priceLabel.setFixedSize(120, 32)

        # button to add the product to the product table
        font.setBold(False)
        font.setPointSize(11)
        self.addButton.setFont(font)
        self.addButton.setObjectName('addButton')
        self.addButton.setStyleSheet('background-color: ' + color0 + ';')
        self.addButton.setText('добавить')
        self.addButton.setFixedSize(120, 40)
        self.addButton.clicked.connect(self.addProduct)

        # table of added products
        font.setBold(False)
        font.setPointSize(13)
        self.productTable.setFont(font)
        self.productTable.setObjectName('productTable')
        self.productTable.setStyleSheet('background-color:' + color3 + ';')
        self.productTable.setColumnCount(3)
        self.productTable.setHorizontalHeaderLabels(['продукт', 'цена', ' '])
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setColumnWidth(0, 180)
        self.productTable.setColumnWidth(1, 160)
        header = self.productTable.horizontalHeader()
        header.setFont(font)
        header.setStyleSheet('::section{Background-color:' + color2 + '}')
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.productTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
