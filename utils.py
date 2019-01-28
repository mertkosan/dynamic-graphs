# Ex: if arr=[2,3,4], result will (1*2 + 2*3 + 3*4) / 1+2+3
def weighted_average_based_on_index(arr):
    if arr is None or len(arr) == 0:
        return 0
    _sum = 0
    for i, elm in enumerate(arr):
        _sum += elm * (i + 1)
    return _sum / (len(arr) * (len(arr) + 1) / 2)
