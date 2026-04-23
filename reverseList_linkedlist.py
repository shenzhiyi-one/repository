class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def reverseList_iterative(head):
        """
        迭代法反转链表
        时间复杂度: O(n)
        空间复杂度: O(1)
        """
        prev = None
        curr = head
    
        while curr:
            next_temp = curr.next  # 保存下一个节点
            curr.next = prev       # 反转指针
            prev = curr            # 前驱指针后移
            curr = next_temp       # 当前指针后移
    
        return prev  # prev最终指向新链表的头节点
    # 创建链表辅助函数
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

# 打印链表辅助函数
def print_linked_list(head):
    values = []
    curr = head
    while curr:
        values.append(str(curr.val))
        curr = curr.next
    print(" -> ".join(values) + " -> None")

# 测试
#if __name__ == "__main__":
    # 创建链表 1->2->3->4->5->None
head = create_linked_list([1, 2, 3, 4, 5])
    
print("原链表:")
print_linked_list(head)
# 测试迭代法
reversed_head = reverseList_iterative(head)
print("\n反转后(迭代法):")
print_linked_list(reversed_head)
