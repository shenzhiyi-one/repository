
import random as rand
def quicksort_random(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 正确做法：随机选择基准，并直接使用它进行分区
        pivot_index = rand.randint(low, high)
        pivot = arr[pivot_index]
        
        # 分区：将小于基准的放左边，大于的放右边
        i = low
        j = high
        
        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        
        # 递归排序左右两部分
        quicksort_random(arr, low, j)
        quicksort_random(arr, i, high)
    
    return arr

# 测试最坏情况
arr_sorted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(quicksort_random(arr_sorted))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
