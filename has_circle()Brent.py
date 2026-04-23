class ListNode:
    """链表节点类"""
    def __init__(self, val):
        self.val = val
        self.next = None


def has_circle_brent(head):
    """
    Brent算法检测链表是否有环
    时间复杂度: O(n)
    空间复杂度: O(1)
    
    核心思想: 
    - fast每次走1步
    - slow每2^k步重置到fast的位置
    - 如果slow == fast说明有环
    - 如果fast走到None说明无环
    """
    # 空链表或只有一个节点且无自环的情况
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    power = 1      # 当前搜索区间大小（2^k）
    steps = 1      # 当前区间内已走的步数
    
    while fast:
        # 达到区间边界，重置slow指针
        if steps == power:
            slow = fast
            power *= 2      # 区间翻倍
            steps = 0       # 重置计数器
        
        # 检测是否相遇（有环）
        if slow == fast:
            return True
        
        # 继续前进
        fast = fast.next
        steps += 1
    
    # fast走到链表末尾，无环
    return False


def has_circle_floyd(head):
    """
    Floyd判圈算法（快慢指针），用于性能对比
    """
    if not head:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False


# ==================== 辅助函数：构建测试用例 ====================

def create_list_without_cycle(arr):
    """创建无环链表"""
    if not arr:
        return None
    
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def create_list_with_cycle(arr, cycle_start_index):
    """
    创建有环链表
    arr: 链表节点值的数组
    cycle_start_index: 环的起始位置（从0开始），尾节点会指向这个位置的节点
    """
    if not arr:
        return None
    
    # 创建所有节点
    nodes = [ListNode(val) for val in arr]
    
    # 连接节点
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # 创建环
    if 0 <= cycle_start_index < len(nodes):
        nodes[-1].next = nodes[cycle_start_index]
    
    return nodes[0] if nodes else None


def print_linked_list(head, max_nodes=20):
    """
    打印链表（用于调试，有环时自动停止）
    """
    if not head:
        print("空链表")
        return
    
    visited = set()
    current = head
    result = []
    count = 0
    
    while current and count < max_nodes:
        if current in visited:
            result.append(f"... → {current.val} (回到此节点，有环)")
            break
        visited.add(current)
        result.append(str(current.val))
        current = current.next
        count += 1
    
    if not current and count < max_nodes:
        print(" → ".join(result) + " → None")
    else:
        print(" → ".join(result))


# ==================== 测试代码 ====================

def run_tests():
    """运行所有测试用例"""
    print("=" * 60)
    print("Brent算法检测链表环 - 完整测试")
    print("=" * 60)
    
    test_cases = [
        # (描述, 数组, 环起始索引, 期望结果)
        ("空链表", [], -1, False),
        ("单节点无环", [1], -1, False),
        ("单节点自环", [1], 0, True),
        ("两节点无环", [1, 2], -1, False),
        ("两节点成环", [1, 2], 0, True),
        ("三节点无环", [1, 2, 3], -1, False),
        ("三节点成环（尾→头）", [1, 2, 3], 0, True),
        ("三节点成环（尾→中间）", [1, 2, 3], 1, True),
        ("长链无环", list(range(1, 11)), -1, False),
        ("长链有环（尾→中间）", list(range(1, 11)), 4, True),
        ("长链有环（尾→头）", list(range(1, 11)), 0, True),
    ]
    
    passed = 0
    failed = 0
    
    for i, (desc, arr, cycle_start, expected) in enumerate(test_cases, 1):
        # 创建链表
        if cycle_start >= 0:
            head = create_list_with_cycle(arr, cycle_start)
        else:
            head = create_list_without_cycle(arr)
        
        # 执行检测
        result = has_circle_brent(head)
        
        # 输出结果
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n测试{i}: {desc}")
        print(f"  链表: ", end="")
        print_linked_list(head)
        print(f"  期望: {'有环' if expected else '无环'}")
        print(f"  结果: {'有环' if result else '无环'}")
        print(f"  状态: {status}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return passed, failed


def performance_comparison():
    """性能对比测试（Brent vs Floyd）"""
    import time
    
    print("\n" + "=" * 60)
    print("性能对比测试 (Brent vs Floyd)")
    print("=" * 60)
    
    # 测试配置
    test_sizes = [
        (1000, 100),      # 小链表，环在中间
        (10000, 1000),    # 中链表
        (50000, 5000),    # 大链表
        (100000, 10000),  # 超大链表
    ]
    
    iterations = 1000  # 每个测试重复次数（取平均）
    
    for total_nodes, cycle_start in test_sizes:
        arr = list(range(total_nodes))
        head = create_list_with_cycle(arr, cycle_start)
        
        # 测试Brent
        start = time.perf_counter()
        for _ in range(iterations):
            has_circle_brent(head)
        brent_time = time.perf_counter() - start
        
        # 测试Floyd
        start = time.perf_counter()
        for _ in range(iterations):
            has_circle_floyd(head)
        floyd_time = time.perf_counter() - start
        
        # 计算提升比例
        speedup = ((floyd_time - brent_time) / floyd_time) * 100
        
        print(f"\n节点数: {total_nodes}, 环起始位置: {cycle_start} (环长: {total_nodes - cycle_start})")
        print(f"  Brent: {brent_time:.4f}s")
        print(f"  Floyd: {floyd_time:.4f}s")
        print(f"  Brent 快 {speedup:.1f}%")


def find_cycle_start(head):
    """
    扩展功能：使用Brent算法找到环的起点
    返回环的起点节点，如果没有环返回None
    """
    if not head or not head.next:
        return None
    
    # 第一阶段：找到环内的一个点
    slow = head
    fast = head.next
    power = 1
    steps = 1
    
    while fast:
        if steps == power:
            slow = fast
            power *= 2
            steps = 0
        
        if slow == fast:
            break
        
        fast = fast.next
        steps += 1
    
    # 无环
    if not fast:
        return None
    
    # 第二阶段：找到环的长度
    cycle_length = 1
    current = slow.next
    while current != slow:
        cycle_length += 1
        current = current.next
    
    # 第三阶段：找到环的起点
    p1 = head
    p2 = head
    for _ in range(cycle_length):
        p2 = p2.next
    
    while p1 != p2:
        p1 = p1.next
        p2 = p2.next
    
    return p1


def test_find_cycle_start():
    """测试查找环起点功能"""
    print("\n" + "=" * 60)
    print("查找环起点测试")
    print("=" * 60)
    
    # 创建链表: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10
    #                                 ↑_______________↓
    # 环起点是5（索引4）
    arr = list(range(1, 11))
    head = create_list_with_cycle(arr, 4)  # 尾节点指向索引4（值为5）
    
    print("链表结构: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → (回到5)")
    
    cycle_start_node = find_cycle_start(head)
    if cycle_start_node:
        print(f"\n找到环的起点: 值为 {cycle_start_node.val}")
    else:
        print("\n链表无环")


# ==================== 主函数 ====================

if __name__ == "__main__":
    # 运行正确性测试
    passed, failed = run_tests()
    
    # 运行性能对比
    if passed > 0:
        performance_comparison()
    
    # 测试扩展功能
    test_find_cycle_start()
    
    # 手动验证示例
    print("\n" + "=" * 60)
    print("手动验证示例")
    print("=" * 60)
    
    # 示例1：无环链表
    head1 = create_list_without_cycle([1, 2, 3, 4, 5])
    print(f"无环链表: {has_circle_brent(head1)}")  # False
    
    # 示例2：有环链表
    head2 = create_list_with_cycle([1, 2, 3, 4, 5], 2)
    print(f"有环链表: {has_circle_brent(head2)}")  # True
