def fill(gap):
    res = ["", ""]
    for g in gap:
        if isinstance(g, str):
            res[0] += g
            res[1] += g
        else: #type(g) is list
            res[0] += g[0]
            res[1] += g[1]

    return res
