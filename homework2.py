# %% [markdown]
#=============================================作业1：集合类（查询、插入、删除操作）==================================================

# %%
from typing import Iterable, Any, Optional
class MySet:
    """实现集合的基本功能：查询、插入、删除，内部使用列表存储"""
    def __init__(self):
        self._items = []          # 内部列表存储元素
    
    def insert(self, item):
        """插入元素，如果已存在则不重复插入"""
        if item not in self._items:
            self._items.append(item)
            return True
        return False               # 元素已存在
    
    def delete(self, item):
        """删除元素，如果存在则删除并返回True，否则返回False"""
        if item in self._items:
            self._items.remove(item)
            return True
        return False
    
    def contains(self, item):
        """查询元素是否存在"""
        return item in self._items
    
    def __str__(self):
        """返回集合的字符串表示"""
        return str(self._items)
    
    def __repr__(self):
        """返回集合的正式字符串表示"""
        return f"MySet({self._items})"

# 测试集合
s = MySet()
s.insert('apple')
s.insert('banana')
s.insert('cherry')
print("插入后:", s)

print("包含 'banana'?", s.contains('banana'))
print("包含 'grape'?", s.contains('grape'))

s.delete('banana')
print("删除'banana'后:", s)

s.insert('apple')          # 重复插入，不会增加
print("再次插入'apple'后:", s)
###输出
# 插入后: ['apple', 'banana', 'cherry']
# 包含 'banana'? True
# 包含 'grape'? False
# 删除'banana'后: ['apple', 'cherry']
# 再次插入'apple'后: ['apple', 'cherry']


# %% [markdown]
#=========================================================作业2：有序数组插入代码（保持有序）===================================================
# 假设数组（列表）已按升序排列，插入新元素后仍然保持有序。
# %%
def insert_ordered(arr, value):
    """
    将value插入有序列表arr（升序）中，保持有序，返回插入位置的索引。
    假设arr已经是升序列表。
    """
    # 查找插入位置
    """线性查找插入位置，时间复杂度O(N)"""
    pos = 0
    while pos < len(arr) and arr[pos] < value:
        pos += 1
    
    # 移动元素并插入
    arr.append(None)          # 扩展一位
    for i in range(len(arr)-1, pos, -1):
        arr[i] = arr[i-1]
    arr[pos] = value
    
    return pos

# 测试
ordered = [1, 4, 5, 19, 21]
print("原始有序数组:", ordered)

# 插入中间值
insert_ordered(ordered, 10)
print("插入10后:", ordered)

# 插入最小值
insert_ordered(ordered, 0)
print("插入0后: ", ordered)

# 插入最大值
insert_ordered(ordered, 100)
print("插入100后:", ordered)


###输出
# 原始有序数组: [1, 4, 5, 19, 21]
# 插入10后: [1, 4, 5, 10, 19, 21]
# 插入0后:  [0, 1, 4, 5, 10, 19, 21]
# 插入100后: [0, 1, 4, 5, 10, 19, 21, 100] 

# %% [markdown]
#========================================================用二分查找的优化版本（插入位置查找更快）=========================================================

# %%
def insert_ordered_binary(arr, value):
    """
    使用二分查找定位插入位置，然后插入。
    查找O(log N)，移动O(N)，总体O(N)。
    """
    # 二分查找插入位置
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < value:
            low = mid + 1
        else:
            high = mid
    pos = low
    
    # 插入元素
    arr.append(None)
    for i in range(len(arr)-1, pos, -1):
        arr[i] = arr[i-1]
    arr[pos] = value
    return pos

# 测试二分版本
arr2 = [1, 3, 5, 7, 9]
print("\n二分插入测试，原始:", arr2)
insert_ordered_binary(arr2, 4)
print("插入4后:", arr2)
insert_ordered_binary(arr2, 10)
print("插入10后:", arr2)
insert_ordered_binary(arr2, 0)
print("插入0后:", arr2)

###输出
# 二分插入测试，原始: [1, 3, 5, 7, 9]
# 插入4后: [1, 3, 4, 5, 7, 9]
# 插入10后: [1, 3, 4, 5, 7, 9, 10]
# 插入0后: [0, 1, 3, 4, 5, 7, 9, 10]
