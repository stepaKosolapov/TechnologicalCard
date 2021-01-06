from pandas import Series, DataFrame, read_csv
import os

productList = DataFrame({
    'productCounter': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'products': [{}, {}, {}, {}, {}, {}, {}, {}, {}]},
    index=['все', 'другое', 'овощи', 'фрукты', 'мясо', 'рыба', 'жидкости', 'молочное', 'грибы'])
productList.index.name = 'groups'

dishList = {}

currentDish = Series(['Новое блюдо', 0, '', []], index=['name', 'markup', 'recipe', 'products'])


def _fromStrToDict(text):
    """
        Converts str to dictionary:
    only from that form of string: "{'str': ('str', int), 'str': ('str', int), ..., 'str': ('str', int)}"
    to dict: {'str': ('str', int), 'str': ('str', int), ..., 'str': ('str', int)}
    """
    if text.__len__() == 2:
        return {}
    text = text.split(')')
    text[0] = text[0][1:]
    text[0] = text[0].split(':')
    text[0][1] = text[0][1][2:].split(', ')
    text[0][1][0] = text[0][1][0][1:-1]
    text[0][1][1] = int(text[0][1][1])
    text[0][1] = tuple(text[0][1])
    text[0][0] = text[0][0][1:-1]

    text = text[:-1]
    for i in range(1, len(text)):
        text[i] = text[i][2:]
        text[i] = text[i].split(':')
        text[i][1] = text[i][1][2:].split(', ')
        text[i][1][0] = text[i][1][0][1:-1]
        text[i][1][1] = int(text[i][1][1])
        text[i][1] = tuple(text[i][1])
        text[i][0] = text[i][0][1:-1]
    dictionary = {text[i][0]: text[i][1] for i in range(len(text))}
    return dictionary


def _fromStrToList(text):
    """
        Converts str to list:
    only from that form of string: "[('str', int), ('str', int), ..., ('str', int)]"
    to list: [('str', int), ('str', int), ..., ('str', int)]
    """
    if text.__len__ == 2:
        return []
    outList = []
    text = text.split("), (")
    text[0] = text[0][2:]
    text[-1] = text[-1][:-2]
    for tup in text:
        tup = tup.split(', ')
        tup[0] = tup[0][1:-1]
        outList.append(tuple(tup))
    return outList


def save():
    """
        Saves the productList, dishList to CSV
    """
    global productList, dishList
    productsDF = productList
    print()
    productsDF.to_csv('data/productList.csv')
    print('productList successfully saved in productList.csv')
    index = []
    values = []
    for name in dishList:
        index.append(name)
        values.append(dishList[name])
    dishesDF = DataFrame(values, index=index)
    dishesDF.rename(columns={0: 'value'}, inplace=True)
    dishesDF.index.name = 'index'
    dishesDF.to_csv('data/dishList.csv')
    print('dishList successfully saved in dishList.csv')


def load():
    """
        Loads the productList, dishList from CSV
    """
    global productList, dishList
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/productList.csv') or not os.path.exists('data/dishList.csv'):
        save()
    productList = DataFrame(read_csv('data/productList.csv', index_col='groups'))
    for group in productList.index:
        productList.at[group, 'products'] = _fromStrToDict(productList.loc[group, 'products'])
    print('productList successfully loaded from productList.csv')
    df = DataFrame(read_csv('data/dishList.csv', index_col='index'))
    for i in df.index:
        dishList[i] = df['value'][i]
    print('dishList successfully loaded from dishList.csv')
    print(currentDish)


def getDishes():
    """
        Returns list of existing dishes
    :return: list of names of the dishes
    """
    global dishList
    return [dishList[dish] for dish in dishList]


def resetDishParameters():
    """
        Set currentDish Series to ['Новое блюдо', 0, '', []]
    """
    setCurrentName('Новое блюдо')
    setCurrentDishMarkup(0)
    setCurrentDishRecipe('')
    setCurrentDishProducts([])


def saveCurrentDish():
    """
        Saves currentDish to CSV file with name of the current dish
    """
    global currentDish, dishList
    if not os.path.exists('data/dishes'):
        os.mkdir('data/dishes')
    dishName = str(currentDish['name'])
    dishList[dishName.lower()] = dishName
    currentDish.index.name = 'index'
    currentDish.name = 'parameters'
    currentDish.to_csv('data/dishes/' + dishName.lower() + '.csv')
    print(dishName + ' was successfully saved')
    print('\n--------------------------------------\n', currentDish, '\n--------------------------------------\n', sep='')


def loadDish(dishName: str):
    """
        Load currentDish from CSV file with name = dishName.lower()
    :param dishName: name of the required dish
    """
    global currentDish
    df = read_csv('data/dishes/' + dishName.lower() + '.csv', index_col='index')
    currentDish = Series(df['parameters'].tolist(), index=df.index.tolist())
    currentDish['markup'] = round(float(currentDish['markup']))
    currentDish['products'] = _fromStrToList(currentDish['products'])
    if str(currentDish['recipe']) == 'nan':
        currentDish['recipe'] = ''


def removeDish(dishName: str):
    """
        Removes the dish from dishList
        Removes the CSV file with name = dishName
    :param dishName: name of the required dish
    """
    global dishList
    try:
        del dishList[dishName.lower()]
        os.remove('data/dishes/' + dishName.lower() + '.csv')
    except KeyError:
        print('dish is missing')


def getCurrentDishName():
    """
        Returns the name of the current dish
    :return: str: name
    """
    global currentDish
    return currentDish['name']


def getCurrentDishMarkup():
    """
        Returns the markup of the current dish
    :return: int: markup
    """
    global currentDish
    return currentDish['markup']


def getCurrentDishProducts():
    """
        Returns the products of the current dish
    :return: list: list of added products
    """
    global currentDish
    return currentDish['products']


def getCurrentDishRecipe():
    """
        Returns the recipe of the current dish
    :return: str: recipe
    """
    global currentDish
    return currentDish['recipe']


def setCurrentName(newName: str):
    """
        Replace the name of the current dish with newName
    :param newName: the new name of the current dish
    """
    global currentDish
    currentDish['name'] = newName


def setCurrentDishMarkup(newMarkup: int):
    """
        Replace the markup of the current dish with newMarkup
    :param newMarkup: the new markup of the current dish
    """
    global currentDish
    currentDish['markup'] = newMarkup


def setCurrentDishProducts(newProducts: list):
    """
        Replace the products of the current dish with newProducts
    :param newProducts: the new list of added products of the current dish
    """
    global currentDish
    currentDish['products'] = newProducts


def setCurrentDishRecipe(newRecipe: str):
    """
        Replace the recipe of the current dish with newRecipe
    :param newRecipe: the new recipe products of the current dish
    """
    global currentDish
    currentDish['recipe'] = newRecipe


def newProduct(name, price, group='все'):
    """
        Adds a new product to the 'productList' DataFrame
    :param name: name of product
    :param price: price of product in rub/kg
    :param group: group of product
    """
    productList.loc[group, 'products'][name.lower()] = name, price
    productList.loc[group, 'productCounter'] += 1
    print(name + ' was added to ' + group, 'counter:', productList.loc[group, 'productCounter'])
    if group != 'все':
        productList.loc['все', 'products'][name.lower()] = name, price
        productList.loc['все', 'productCounter'] += 1
        print(name + ' was added to ' + 'все', 'counter:', productList.loc['все', 'productCounter'])


def searchProductGroup(name):
    name = name.lower()
    for group in getGroups()[1:]:
        for product in getProducts(group):
            if product == name:
                return group


def removeProduct(name, group):
    """
        Removes a product from the 'productList' DataFrame
    :param name: name of product
    :param group: group of product
    """
    del productList.loc[group, 'products'][name.lower()]
    print(group, 'counter:', productList.loc[group, 'productCounter'])
    productList.loc[group, 'productCounter'] -= 1
    print(name + ' was deleted from ' + group, 'counter:', productList.loc[group, 'productCounter'])


def getGroups():
    """
        Returns the list of groups from productList
    :return: list: list of groups
    """
    return productList.index


def getProducts(group='все'):
    """
        Returns list of the group
    :param group: required group
    :return: list: list of products
    """
    return productList.loc[group, 'products']


if __name__ == '__main__':
    load()

    newProduct('помидор', 60)
    newProduct('огурец', 100)
    newProduct('майонез', 200)
    newProduct('картофель', 20)
    newProduct('лук', 50)
    newProduct('перец', 1000)
    newProduct('курица', 300)

    resetDishParameters()
    setCurrentName('Салат')
    setCurrentDishProducts([('помидор', 340), ('огурец', 400), ('майонез', 100)])
    setCurrentDishMarkup(20)
    setCurrentDishRecipe('1.Порезать помидоры и огурцы.\n'
                         '2.Добавить майонез.'
                         )
    saveCurrentDish()

    resetDishParameters()
    setCurrentName('Суп')
    setCurrentDishProducts([('картофель', 1500), ('лук', 200), ('перец', 30), ('курица', 700)])
    setCurrentDishMarkup(20)
    setCurrentDishRecipe('1.Порезать картофель и курицу.\n'
                         '2.Поставить воду кипятиться.\n'
                         '3.Закинуть в кипящую воду овощи и курицу'
                         )
    saveCurrentDish()

    loadDish('СаЛат')
    save()
