class InputError(Exception):
    """
        Exception should be raised when an invalid value is entered
    """
    pass


colors = ['#8ab82e', '#77d496', '#dec476', '#DBD7D2']
mainFont = 'Times New Roman'
currency = ' руб'
postfixCost = currency
postfixPrice = postfixCost + '/кг'
postfixWeight = ' г'
