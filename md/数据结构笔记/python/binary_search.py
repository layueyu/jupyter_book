def binary_search(alist, item):
    """二分查找"""
    n = len(alist)
    if n > 0:
        mid = n//2

        if alist[mid] == item:
            return True
        elif item < alist[mid]:
            return binary_search(alist[:mid], item)
        else:
            return binary_search(alist[mid+1:], item)
    return False


if __name__ == '__main__':
    li = [1, 2, 3, 4, 5, 6, 7, 8]
    print(binary_search(li, 6))

