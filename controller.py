from pandas import DataFrame, read_csv

productList = DataFrame({
    'productCounter': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'products': [{}, {}, {}, {}, {}, {}, {}, {}, {}]},
    index=['все', 'другое', 'овощи', 'фрукты', 'мясо', 'рыба', 'жидкости', 'молочное', 'грибы'])
productList.index.name = 'groups'


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


def save():
    global productList
    productsDF = productList
    print()
    productsDF.to_csv('data/products.csv')
    print('successfully saved in products.csv')


def load():
    import os.path
    global productList
    if not os.path.exists('data/products.csv'):
        save()
    productList = DataFrame(read_csv('data/products.csv', index_col='groups'))
    for group in productList.index:
        productList.at[group, 'products'] = fromStrToDict(productList.loc[group, 'products'])
    print('successfully loaded from products.csv')


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
    newProduct('Помидор', 123, 'овощи')
    newProduct(group='овощи', name='Огурец', price=241)
    newProduct('Творог', 123, 'молочное')
    print(searchProductGroup('Огурец'))
    print(productList)
    save()
    print(productList)
    load()
    print(productList)
