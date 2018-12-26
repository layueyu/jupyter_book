def bubble_sort(alist):
    """冒泡排序"""
    n = len(alist)
    for i in range(0, n-1):
        for j in range(0, n-i-1):
            if alist[j] > alist[j+1]:
                alist[j], alist[j+1] = alist[j+1], alist[j]


def seelct_sort(alist):
    """选择排序"""
    n = len(alist)
    for i in range(0, n-1):
        min_index = i
        for j in range(i+1, n):
            if alist[min_index] > alist[j]:
                min_index = j
        alist[i], alist[min_index] = alist[min_index], alist[i]


def insert_sort(alist):
    """插入排序"""
    n = len(alist)
    for i in range(1, n):
        j = i
        for j in range(j, 0, -1):
            if alist[j] < alist[j-1]:
                alist[j], alist[j-1] = alist[j-1], alist[j]
            else:
                break


def quick_sort(alist, start, end):
    """快速排序"""

    if start >= end:
        return

    mid_value = alist[start]
    low = start
    high = end

    while low < high:
        # high 左移动
        while low < high and alist[high] >= mid_value:
                high -= 1
        alist[low] = alist[high]

        # low 右移动
        while low < high and alist[low] < mid_value:
            low += 1
        alist[high] = alist[low]
    # 循环退出时，low == high
    alist[low] = mid_value

    # 对low左边的列表执行快速排序
    quick_sort(alist, start, low-1)

    # 对low右边的列表执行快速排序
    quick_sort(alist, low+1, end)


def shell_sort(alist):
    """希尔排序"""
    n = len(alist)
    gap = n//2

    while gap >= 1:
        for i in range(gap, n):
            for j in range(i, 0, -gap):
                if alist[j] < alist[j-gap]:
                    alist[j], alist[j-gap] = alist[j-gap], alist[j]
                else:
                    break
        gap //= 2


def merge_sort(alist):
    """归并排序"""
    n = len(alist)
    if n <= 1:
        return alist

    mid = n // 2

    # left 采用归并后的有序的新的列表
    left_li = merge_sort(alist[:mid])

    # right 采用归并后的有序的新的列表
    right_li = merge_sort(alist[mid:])

    # 将两个有序子序列合并为一个新的整体
    left_pointer, right_pointer = 0, 0
    result = []

    while left_pointer < len(left_li) and right_pointer < len(right_li):
        if left_li[left_pointer] < right_li[right_pointer]:
            result.append(left_li[left_pointer])
            left_pointer += 1
        else:
            result.append(right_li[right_pointer])
            right_pointer += 1

    result += left_li[left_pointer:]
    result += right_li[right_pointer:]
    return result


def print_list(alist):
    for i in alist:
        print(i, end=" ")
    print()


if __name__ == '__main__':
    ls = [1, 5, 2, 9, 3,  6]
    sorted_li = merge_sort(ls)
    print_list(sorted_li)
