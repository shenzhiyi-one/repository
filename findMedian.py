import heapq

class MedianFinder:
    def __init__(self):
        # 大顶堆存储较小的一半（取负数模拟大顶堆）
        self.left = []   # max heap
        # 小顶堆存储较大的一半
        self.right = []  # min heap

    def addNum(self, num: int) -> None:
        # 决定插入到哪个堆
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
        else:
            heapq.heappush(self.right, num)
        
        # 平衡两个堆，使 |left| >= |right| 且差值不超过 1
        if len(self.left) > len(self.right) + 1:
            moved = -heapq.heappop(self.left)
            heapq.heappush(self.right, moved)
        elif len(self.right) > len(self.left):
            moved = heapq.heappop(self.right)
            heapq.heappush(self.left, -moved)

    def findMedian(self) -> float:
        if len(self.left) == len(self.right):
            return (-self.left[0] + self.right[0]) / 2.0
        else:
            return -self.left[0] * 1.0


# 测试代码
if __name__ == "__main__":
    mf = MedianFinder()
    nums = [1, 2, 3, 4, 5]
    for num in nums:
        mf.addNum(num)
        print(f"添加 {num} 后，中位数: {mf.findMedian()}")
