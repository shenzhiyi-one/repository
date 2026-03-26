import hashlib
import json
from typing import Any, Optional, List, Tuple
import time

class HashTable:
    """使用真正的哈希函数实现的哈希表"""
    
    def __init__(self, capacity: int = 100, hash_type: str = 'md5'):
        """
        初始化哈希表
        :param capacity: 初始容量
        :param hash_type: 哈希函数类型 ('md5', 'sha1', 'sha256')
        """
        self.capacity = capacity
        self.size = 0
        self.load_factor = 0.75
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]
        self.hash_type = hash_type
        self.collisions = 0
        
    def _hash_function(self, key: str) -> int:
        """使用真正的加密哈希函数"""
        key_bytes = key.encode('utf-8')
        
        if self.hash_type == 'md5':
            hash_obj = hashlib.md5(key_bytes)
        elif self.hash_type == 'sha1':
            hash_obj = hashlib.sha1(key_bytes)
        elif self.hash_type == 'sha256':
            hash_obj = hashlib.sha256(key_bytes)
        else:
            raise ValueError(f"不支持的哈希类型: {self.hash_type}")
        
        hex_hash = hash_obj.hexdigest()
        int_hash = int(hex_hash[:8], 16)
        
        return int_hash % self.capacity
    
    def _resize(self):
        """当负载因子超过阈值时，扩展哈希表"""
        if self.size / self.capacity < self.load_factor:
            return
        
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collisions = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key: str, value: Any) -> None:
        """插入键值对"""
        self._resize()
        
        index = self._hash_function(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        self.table[index].append((key, value))
        self.size += 1
        
        if len(self.table[index]) > 1:
            self.collisions += 1
    
    def get(self, key: str) -> Optional[Any]:
        """获取键对应的值"""
        index = self._hash_function(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: str) -> bool:
        """删除键值对"""
        index = self._hash_function(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.size -= 1
                if len(self.table[index]) == 0:
                    self.collisions -= 1
                return True
        
        return False
    
    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None
    
    def __len__(self) -> int:
        return self.size
    
    def keys(self) -> List[str]:
        keys = []
        for bucket in self.table:
            for key, _ in bucket:
                keys.append(key)
        return keys
    
    def values(self) -> List[Any]:
        values = []
        for bucket in self.table:
            for _, value in bucket:
                values.append(value)
        return values
    
    def items(self) -> List[Tuple[str, Any]]:
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return items
    
    def stats(self) -> dict:
        bucket_sizes = [len(bucket) for bucket in self.table]
        return {
            'capacity': self.capacity,
            'size': self.size,
            'load_factor': self.size / self.capacity,
            'collisions': self.collisions,
            'empty_buckets': sum(1 for s in bucket_sizes if s == 0),
            'max_bucket_size': max(bucket_sizes) if bucket_sizes else 0,
            'avg_bucket_size': self.size / self.capacity,
            'hash_type': self.hash_type
        }
    
    def __str__(self) -> str:
        return f"哈希表(大小={self.size}, 容量={self.capacity})"


class HashTableWithLinearProbing:
    """使用线性探测法处理冲突的哈希表"""
    
    def __init__(self, capacity: int = 100, hash_type: str = 'md5'):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.hash_type = hash_type
        self.DELETED = object()
        
    def _hash_function(self, key: str) -> int:
        key_bytes = key.encode('utf-8')
        
        if self.hash_type == 'md5':
            hash_obj = hashlib.md5(key_bytes)
        elif self.hash_type == 'sha256':
            hash_obj = hashlib.sha256(key_bytes)
        else:
            hash_obj = hashlib.sha1(key_bytes)
        
        hex_hash = hash_obj.hexdigest()
        int_hash = int(hex_hash[:8], 16)
        return int_hash % self.capacity
    
    def _probe(self, key: str, hash_val: int) -> int:
        index = hash_val
        first_deleted = -1
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return index
            if self.keys[index] is self.DELETED and first_deleted == -1:
                first_deleted = index
            index = (index + 1) % self.capacity
            if index == hash_val:
                break
        
        return first_deleted if first_deleted != -1 else index
    
    def put(self, key: str, value: Any) -> None:
        if self.size >= self.capacity * 0.75:
            self._resize()
        
        hash_val = self._hash_function(key)
        index = self._probe(key, hash_val)
        
        if self.keys[index] != key:
            self.size += 1
        
        self.keys[index] = key
        self.values[index] = value
    
    def get(self, key: str) -> Optional[Any]:
        hash_val = self._hash_function(key)
        index = hash_val
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.capacity
            if index == hash_val:
                break
        
        return None
    
    def remove(self, key: str) -> bool:
        hash_val = self._hash_function(key)
        index = hash_val
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.keys[index] = self.DELETED
                self.values[index] = None
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
            if index == hash_val:
                break
        
        return False
    
    def _resize(self):
        old_keys = self.keys
        old_values = self.values
        
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for key, value in zip(old_keys, old_values):
            if key is not None and key is not self.DELETED:
                self.put(key, value)
    
    def stats(self) -> dict:
        return {
            'size': self.size,
            'capacity': self.capacity,
            'load_factor': self.size / self.capacity,
            'hash_type': self.hash_type
        }


if __name__ == "__main__":
    print("测试不同的哈希函数")
    
    test_keys = ["苹果", "香蕉", "橙子", "葡萄", "苹果"]
    hash_types = ['md5', 'sha1', 'sha256']
    
    for key in test_keys:
        print(f"\n键: '{key}'")
        for hash_type in hash_types:
            key_bytes = key.encode('utf-8')
            if hash_type == 'md5':
                hash_obj = hashlib.md5(key_bytes)
            elif hash_type == 'sha1':
                hash_obj = hashlib.sha1(key_bytes)
            else:
                hash_obj = hashlib.sha256(key_bytes)
            
            hex_hash = hash_obj.hexdigest()
            int_hash = int(hex_hash[:8], 16)
            mod_result = int_hash % 100
            print(f"  {hash_type.upper()}: {hex_hash[:12]}... -> {int_hash:10d} (模100: {mod_result})")
    
    print("\n测试链地址法哈希表")
    
    ht = HashTable(capacity=10, hash_type='sha256')
    
    test_data = {
        "姓名": "张三",
        "年龄": 25,
        "城市": "北京",
        "职业": "工程师",
        "爱好": "阅读",
        "邮箱": "zhangsan@example.com"
    }
    
    print("\n插入数据:")
    for key, value in test_data.items():
        ht.put(key, value)
        print(f"  {key} -> {value}")
    
    print("\n获取数据:")
    for key in ["姓名", "城市", "不存在"]:
        value = ht.get(key)
        print(f"  {key}: {value}")
    
    print("\n更新数据:")
    ht.put("年龄", 26)
    print(f"  年龄 -> {ht.get('年龄')}")
    
    print("\n删除数据:")
    ht.remove("爱好")
    print(f"  爱好是否存在: {'爱好' in ht}")
    
    print("\n哈希表统计信息:")
    stats = ht.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n测试大量数据插入:")
    large_ht = HashTable(capacity=50, hash_type='sha256')
    start_time = time.time()
    
    for i in range(1000):
        large_ht.put(f"键{i}", f"值{i}")
    
    elapsed = time.time() - start_time
    print(f"  插入1000个键值对耗时: {elapsed:.4f}秒")
    large_stats = large_ht.stats()
    print(f"  容量: {large_stats['capacity']}")
    print(f"  大小: {large_stats['size']}")
    print(f"  负载因子: {large_stats['load_factor']:.3f}")
    print(f"  冲突次数: {large_stats['collisions']}")
    print(f"  最大桶大小: {large_stats['max_bucket_size']}")
    
    print("\n测试线性探测法哈希表")
    
    ht_lp = HashTableWithLinearProbing(capacity=10, hash_type='md5')
    
    words = ["苹果", "香蕉", "樱桃", "枣", "接骨木", "无花果", "葡萄"]
    
    print("\n插入单词:")
    for i, word in enumerate(words):
        ht_lp.put(word, f"定义{i+1}")
        print(f"  {word} -> 定义{i+1}")
    
    print("\n查询结果:")
    for word in ["苹果", "樱桃", "斑马"]:
        value = ht_lp.get(word)
        print(f"  {word}: {value}")
    
    lp_stats = ht_lp.stats()
    print(f"\n统计信息: {lp_stats}")
    
    print("\n测试哈希碰撞分布")
    
    ht_collision = HashTable(capacity=100, hash_type='sha256')
    
    for i in range(500):
        ht_collision.put(f"键_{i}", i)
    
    collision_stats = ht_collision.stats()
    print(f"\n碰撞统计:")
    print(f"  总冲突次数: {collision_stats['collisions']}")
    print(f"  空桶比例: {collision_stats['empty_buckets']/collision_stats['capacity']*100:.1f}%")
    print(f"  最大桶大小: {collision_stats['max_bucket_size']}")
    print(f"  平均桶大小: {collision_stats['avg_bucket_size']:.2f}")
    
    bucket_sizes = [len(bucket) for bucket in ht_collision.table]
    distribution = {}
    for size in bucket_sizes:
        distribution[size] = distribution.get(size, 0) + 1
    
    print(f"\n桶大小分布:")
    for size in sorted(distribution.keys()):
        bar = "*" * distribution[size]
        print(f"  大小 {size}: {bar} ({distribution[size]}个桶)")
    
    print("\n所有测试完成")
##输出
"""
测试不同的哈希函数

键: '苹果'
  MD5: e6803e21b9c6... -> 3867164193 (模100: 93)
  SHA1: b38d961e7096... -> 3012400670 (模100: 70)
  SHA256: 50537dab7650... -> 1347648939 (模100: 39)

键: '香蕉'
  MD5: b7c03bbf2b8b... -> 3082828735 (模100: 35)
  SHA1: bc098b15118c... -> 3154742037 (模100: 37)
  SHA256: dbf9f9c94fc9... -> 3690592713 (模100: 13)

键: '橙子'
  MD5: f24b6a378162... -> 4065028663 (模100: 63)
  SHA1: 858036f881b3... -> 2239772408 (模100: 8)
  SHA256: c8d3209aaa4a... -> 3369279642 (模100: 42)

键: '葡萄'
  MD5: 05b1b3102be2... ->   95531792 (模100: 92)
  SHA1: df9eaffa238b... -> 3751718906 (模100: 6)
  SHA256: ae86f9a1daef... -> 2928081313 (模100: 13)

键: '苹果'
  MD5: e6803e21b9c6... -> 3867164193 (模100: 93)
  SHA1: b38d961e7096... -> 3012400670 (模100: 70)
...
  大小 3: ******************* (19个桶)
  大小 4: * (1个桶)

所有测试完成
"""
