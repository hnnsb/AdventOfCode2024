def mean(l):
    return sum(l)/len(l)


def var(l):
    m = mean(l)
    return sum((xi - m) ** 2 for xi in l) / len(l)


def std(l):
    return std**(1/2)
