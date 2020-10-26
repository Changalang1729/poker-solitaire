def lget(l, index, default=None):
    try:
        return l[index]
    except IndexError:
        return default


def setify(drawnCards):
    try:
        return set(drawnCards)
    except TypeError:
        return set([drawnCards])