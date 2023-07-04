
def add_stocksuffix(x):
    # returnvalue = x
    if len(x) < 8 and len(x) > 0:
        if x[0] == '6':
            x = x[:6] + '.SH'
        elif x[0] == '8':
            x = x[:6] + '.BJ'
        else:
            x = x[:6] + '.SZ'
    return x