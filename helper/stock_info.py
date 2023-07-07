
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

def is_a_market(x):
    aaa = x.split(".")
    if len(aaa)>1:
       houzui = aaa[len(aaa)-1]
       if houzui == 'SH' or houzui == 'SZ' or houzui == 'BJ' :
           return True
    return False

# is_a_market('a.b')