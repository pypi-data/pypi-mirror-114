def binary_search(arr, start, end, value):
    while start <= end:
        mid = start + (end-start)//2
        if arr[mid] == value:
            return mid
        elif value > arr[mid]:
            start = mid + 1
        else:
            end = mid - 1
