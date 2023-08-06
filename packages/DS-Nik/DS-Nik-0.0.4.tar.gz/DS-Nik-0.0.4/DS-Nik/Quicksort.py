def partition(start, end, data):
    pivot = data[end]
    i = start - 1
    for j in range(start, end):
        if data[j] < pivot:
            i = i + 1
            temp = data[i]
            data[i] = data[j]
            data[j] = temp
    temp = data[i+1]
    data[i+1] = data[end]
    data[end] = temp
    return i+1
    
def quicksort(start, end, data):
    if start < end:
        pivotIndex = partition(start, end, data)
        quicksort(start, pivotIndex - 1, data)
        quicksort(pivotIndex+1, end, data)

