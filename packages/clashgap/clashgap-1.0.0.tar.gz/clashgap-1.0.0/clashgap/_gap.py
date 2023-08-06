# This file contains the gap implementation and all the functions required for it

def _list_has(arr, index):
    return (len(arr) > index)

def _collision(arr, brr):
    for i, _ in enumerate(arr):
        collision = brr.find(arr[i])
        if collision != -1:
            return i, collision
    return -1, 0

def gap(clash):
    res = []
    buff = ['', '']
    for i, _ in enumerate(clash[0]):
        buff[0] += clash[0][i]
        if _list_has(clash[1], i):
            buff[1] += clash[1][i]

        o, l = _collision(buff[0], buff[1])

        if o != -1:
            if buff[0][:o] or buff[1][:l]:
                res += [[buff[0][:o], buff[1][:l]], buff[1][l]]
            elif (len(res) == 0) or (isinstance(res[-1], list)):
                res += buff[1][l]
            else:
                res[-1] += buff[1][l]

            buff[0] = buff[0][o+1:]
            buff[1] = buff[1][l+1:]

    if buff[0] or buff[1]:
        res.append(buff)

    return res
