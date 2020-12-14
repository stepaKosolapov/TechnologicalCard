groups = {
    'все': {'productCounter': 0, 'products': {}},
    'другое': {'productCounter': 0, 'products': {}},
    'овощи': {'productCounter': 0, 'products': {}},
    'фрукты': {'productCounter': 0, 'products': {}},
    'мясо': {'productCounter': 0, 'products': {}},
    'рыба': {'productCounter': 0, 'products': {}},
    'жидкости': {'productCounter': 0, 'products': {}},
    'молочное': {'productCounter': 0, 'products': {}},
    'грибы': {'productCounter': 0, 'products': {}},
    }


def searchGroupProduct(name):
    """Searches groups of product
    :param name: name of the searched product
    :return: list of groups of the searched product
    """
    searched = []
    name = name.lower()
    for group in groups:
        for product in groups[group]['products']:
            if name == product:
                searched.append(group)
    return searched


def newProduct(name, price, group='все'):
    """Adds a new product to the 'groups' dictionary
    :param name: name of product
    :param price: price of product in rub/kg
    :param group: group of product
    """
    groups[group]['products'][name.lower()] = name, price
    groups[group]['productCounter'] += 1
    if group != 'все':
        groups['все']['products'][name.lower()] = name, price
        groups['все']['productCounter'] += 1


def removeProduct(name, group=None):
    """Removes a product from the 'groups' dictionary
    :param name: name of product
    :param group: group of product (may not be specified)
    """
    if group is None:
        searchedGroups = searchGroupProduct(name)
        for group_ in searchedGroups:
            del groups[group_]['products'][name.lower()]
            groups[group_]['productCounter'] -= 1
    else:
        del groups[group]['products'][name.lower()]
        groups[group]['productCounter'] -= 1


def showProducts():
    """Prints to Console all products in 'groups'
    """
    for group in groups:
        if groups[group]['products'].__len__() != 0:
            print(group + '(' + str(groups[group]['productCounter']) + ')' + ':', *groups[group]['products'])


newProduct('Помидор', 123, 'овощи')
newProduct(group='овощи', name='Огурец', price=241)
newProduct('Творог', 123, 'молочное')
newProduct('Говядина', 123, 'мясо')


if __name__ == '__main__':
    newProduct('Помидор', 123, 'овощи')
    newProduct(group='овощи', name='огурец', price=241)
    newProduct('Творог', 123, 'молочное')
    newProduct('Говядина', 123, 'мясо')

    showProducts()
    print()
    removeProduct('ПоМидор')

    showProducts()

    help(removeProduct)
