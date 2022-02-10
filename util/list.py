def overlap(a: [], b: []) -> []:
    """Returns list of common elements in 2 input lists"""
    return [i for i in a if i in b]


def add_if_not_in(a: [], b: []):
    for ai in a:
        if ai not in b:
            b.append(ai)
