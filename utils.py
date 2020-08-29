def lget(l, index, default=None):
    try:
        return l[index]
    except IndexError:
        return default


