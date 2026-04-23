class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def deleteNode(head, target):
    """删除链表中第一个值为target的节点"""
    # 空链表
    if not head:
        return None
    
    # 删除头节点
    if head.val == target:
        return head.next
    
    # 删除中间或尾部节点
    current = head
    while current.next and current.next.val != target:
        current = current.next
    
    # 找到了就删除
    if current.next:
        current.next = current.next.next
    
    return head

# 辅助函数：打印链表
def printList(head):
    values = []
    while head:
        values.append(str(head.val))
        head = head.next
    print(" -> ".join(values) + " -> NULL")

# 测试
if __name__ == "__main__":
    # 创建链表 1->2->3->4->NULL
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    
    print("原链表:", end=" ")
    printList(head)
    
    # 删除值为3的节点
    head = deleteNode(head, 3)
    print("删除3后:", end=" ")
    printList(head)
    
    # 删除头节点
    head = deleteNode(head, 1)
    print("删除1后:", end=" ")
    printList(head)
