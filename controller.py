from pandas import Series, DataFrame, read_csv
import os

productList = DataFrame({
    'productCounter': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'products': [{}, {}, {}, {}, {}, {}, {}, {}, {}]},
    index=['все', 'другое', 'овощи', 'фрукты', 'мясо', 'рыба', 'жидкости', 'молочное', 'грибы'])
productList.index.name = 'groups'

dishList = {}

currentDish = Series(['Новое блюдо', 0, '', []], index=['name', 'markup', 'recipe', 'products'])


def fromStrToDict(text):
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


def fromStrToList(text):
    """
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
    global productList, dishList
    productsDF = productList
    print()
    productsDF.to_csv('data/products.csv')
    print('productList successfully saved in products.csv')
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
    global productList, dishList
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/products.csv') or not os.path.exists('data/dishList.csv'):
        save()
    productList = DataFrame(read_csv('data/products.csv', index_col='groups'))
    for group in productList.index:
        productList.at[group, 'products'] = fromStrToDict(productList.loc[group, 'products'])
    print('productList successfully loaded from products.csv')
    df = DataFrame(read_csv('data/dishList.csv', index_col='index'))
    for i in df.index:
        dishList[i] = df['value'][i]
    print('dishList successfully loaded from dishList.csv')


def getDishes():
    global dishList
    return [dish for dish in dishList]


def resetDishParameters():
    setCurrentDishRecipe('')
    setCurrentDishMarkup(0)
    setCurrentDishProducts([])
    setCurrentName('Новое блюдо')


def saveCurrentDish():
    global currentDish, dishList
    if not os.path.exists('data/dishes'):
        os.mkdir('data/dishes')
    dishName = str(currentDish['name'])
    dishList[dishName.lower()] = dishName
    currentDish.index.name = 'index'
    currentDish.name = 'parameters'
    currentDish.to_csv('data/dishes/' + dishName.lower() + '.csv')
    print(dishName + ' was successfully saved')


def loadDish(dishName: str):
    global currentDish
    df = read_csv('data/dishes/' + dishName.lower() + '.csv', index_col='index')
    currentDish = Series(df['parameters'].tolist(), index=df.index.tolist())
    currentDish['markup'] = int(currentDish['markup'])
    currentDish['products'] = fromStrToList(currentDish['products'])


def removeDish(dishName: str):
    global dishList
    del dishList[dishName.lower()]
    os.remove('data/dishes/' + dishName.lower() + '.csv')


def getCurrentDishName():
    global currentDish
    return currentDish['name']


def getCurrentDishMarkup():
    global currentDish
    return currentDish['markup']


def getCurrentDishProducts():
    global currentDish
    return currentDish['products']


def getCurrentDishRecipe():
    global currentDish
    return currentDish['recipe']


def setCurrentName(newName: str):
    global currentDish
    currentDish['name'] = newName


def setCurrentDishMarkup(newMarkup: int):
    global currentDish
    currentDish['markup'] = newMarkup


def setCurrentDishProducts(newProducts: list):
    global currentDish
    currentDish['products'] = newProducts


def setCurrentDishRecipe(newRecipe: str):
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
    return productList.index


def getProducts(group='все'):
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
