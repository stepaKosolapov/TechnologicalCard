groups = {
    'все': {'productCounter': 1, 'products': {'помидор': ('помидор', 60)}},
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


def newProduct(name, price, group):
    """Adds a new product to the 'groups' dictionary
    :param name: name of product
    :param price: price of product in rub/kg
    :param group: group of product
    """

    groups[group]['products'][name.lower()] = name, price
    groups[group]['productCounter'] += 1


def removeProduct(name, group=None):
    """Removes a product from the 'groups' dictionary
    :param name: name of product
    :param group: group of product (may not be specified)
    """

    if group is None:
        group = searchGroupProduct(name)
    del groups[group]['products'][name.lower()]
    groups[group]['productCounter'] -= 1


def showProducts():
    """Prints to Console all products in 'groups'
    """
    for group in groups:
        if groups[group]['products'].__len__() != 0:
            print(group + '(' + str(groups[group]['productCounter']) + ')' + ':', *groups[group]['products'])


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
