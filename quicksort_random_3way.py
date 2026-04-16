import random as rand

def quicksort_random_3way(arr, low=0, high=None):
    """三路分区快速排序，正确处理重复元素"""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 随机选择基准
        pivot_index = rand.randint(low, high)
        pivot = arr[pivot_index]
        
        # 三路分区：< pivot, == pivot, > pivot
        lt = low      # 小于区域的边界
        i = low       # 当前扫描位置
        gt = high     # 大于区域的边界
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:  # arr[i] == pivot
                i += 1
        
        # 递归排序小于和大于的部分
        quicksort_random_3way(arr, low, lt - 1)
        quicksort_random_3way(arr, gt + 1, high)
    
    return arr

# 测试
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(quicksort_random_3way(arr))  # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
