#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : sort_by_insertion.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2020-12-21 17:21 
@Author: buweiqiang
@Version: 1.0
@Desciption: 插入排序法思想：假设已经有一个有序序列，将未排序的数组，逐个个的插入到有序序列的合适位置
'''
import random
import time


def sort_forward(array: list):
    '''
    正序插入：假设第一位是有序序列，从第二位开始迭代，依次将后面的数字，插入到前面的有序序列
    方法：假设第一位i=0是有序序列，从i+1开始，每次取有序序列后面位置的一个数j=i+1，将这个数与前面的有序序列（长度为i+1）向前逐个比较，如果比前面的小，就与之交换（即永远将小的数插入到大数的前面），如果不比前面的小，就可以中止退出本次循环
    :param array: 未排序的数组
    :return: 无
    '''

    n = len(array)
    if len(array) < 2:
        print(f'The length of the array is {n}, no need to sort')
        return

    for i in range(n - 1):
        # 从第二位开始，第一轮过后，前二位是有序序列，第二轮后，前三位是有序序列，以次类推，直到整个数组排序完成
        j = i + 1
        swap_count = 0  # 记录交换次数
        while j > 0:
            if array[j] < array[j - 1]:
                temp = array[j]
                array[j] = array[j - 1]
                array[j - 1] = temp
                j -= 1
                swap_count += 1
            else:
                # 因为前面已经是有序序列，所以只要出现了一个数不比后面的小，就可以中止比较了，这点与比冒泡排序要好，不用每次都遍历到末尾
                break
        # print(f'round {i + 1}, swap_count={swap_count}: {array}')


def sort_backward(array: list):
    '''
    倒序插入：假设倒数第一位是有序序列，从倒数第二位开始迭代，依次将前面的数字，插入到后面的有序序列
    方法：假设最后一位n-1是有序序列，i=1~n，从n-1-i开始，每次取有序序列前面位置的一个数j=n-1-i，将这个数与后面的有序序列（长度为i）逐个比较，如果比后面的大，就与之交换（即永远将大的数插入到小数的后面），如果不比后面的大，就可以中止退出本次循环
    :param array: 未排序的数组
    :return: 无
    '''

    n = len(array)
    if len(array) < 2:
        print(f'The length of the array is {n}, no need to sort')
        return

    for i in range(1, n):
        # 从倒数第二位开始，第一轮过后，倒数二位是有序序列，第二轮后，倒数三位是有序序列，以次类推，直到整个数组排序完成
        j = n - 1 - i
        swap_count = 0
        while j < n - 1:
            if array[j] > array[j + 1]:
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
                j += 1
                swap_count += 1
            else:
                # 因为后面已经是有序序列，所以只要出现了前一个数不比后面的大，就可以中止比较了，这点与比冒泡排序要好，不用每次都遍历到末尾
                break
        # print(f'round {i + 1}, swap_count={swap_count}: {array}')


def quick_sort(array: list, l_index, r_index):
    if r_index > l_index:
        m_value = array[l_index]
        array[l_index] = None
        # print(f'middle value = {m_value}')

        l = l_index
        r = r_index
        while l < r:
            if array[l] is None:
                # 此时array[l]=None，左边有坑，从右边依次找小于中间数m_value的数，移到左边坑位
                if array[r] < m_value:
                    array[l] = array[r]  # 将r的值移到l的坑位上
                    array[r] = None  # 此时r位置变成了坑位
                    l += 1
                    # print(f'r={r}: {array}')
                else:
                    r -= 1
            else:
                # 此时array[r]=None，右边有坑，从左边依次找大于中间数m_value的数，移到右边坑位
                if array[l] > m_value:
                    array[r] = array[l]  # 将l的值移到r的坑位上
                    array[l] = None  # 此时l位置变成了坑位
                    r -= 1
                    # print(f'l={l}: {array}')
                else:
                    l += 1

        # 当l和r相遇时，代表左右已经分完，左边全是小于m数，右边全是大于m的数
        array[l] = m_value
        # print(f'quick sort finished at {l}: {array}')

        # 对m_value左边数组和右边的数组分别进行递归分隔，至到数组长度=1
        if l - l_index > 1:
            quick_sort(array, l_index, l - 1)
        if r_index - r > 1:
            quick_sort(array, r + 1, r_index)


if __name__ == "__main__":
    # array = [5, 7, 8, 5, 9, 3, 2, 10, 1, 13, 10]
    # 如需做性能测试，把数组变长和循环次数加大即可
    array = [random.randint(0, 1000) for i in range(200)]
    print(array)

    # 快排
    start_time = time.time()
    for i in range(100):
        quick_sort(array.copy(), 0, len(array) - 1)
    end_time = time.time()
    duration = end_time - start_time
    print(f'duration of quick sort: {duration}')

    # 正排
    start_time = time.time()
    for i in range(100):
        sort_forward(array.copy())
    end_time = time.time()
    duration = end_time - start_time
    print(f'duration of forward insertion: {duration}')

    # 倒排
    start_time = time.time()
    for i in range(100):
        sort_backward(array.copy())
    end_time = time.time()
    duration = end_time - start_time
    print(f'duration of backward insertion: {duration}')
