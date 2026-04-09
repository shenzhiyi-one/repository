#======================week 1-列表删除====================
from typing import Iterable,Any
class DeleteItem:
  #接受任意可迭代对象转为列表
  def __init__(self,data:Iterable[Any]):
    self.iterable = list(data)
  def delete(self,index_to_delete:int)->list[Any]:
    '''
    按索引删除
    :param index_to_delete: 要删除的元素的索引
    :return:删除操作后的新列表
    :raise IndexError:索引越界
    '''
    #索引检验
    list_length = len(self.iterable)
    if index_to_delete < 0 or index_to_delete > = list_length:
      raise IndexError("索引越界！")
    #从index_to_delete下一位开始到列表最后一位即list_length-1结束，逐个前移一位
    for i in range (index_to_delete + 1,list_length):
      self.iterable[i-1] = self.iterable[i]
    #清空末位内存
    self.iterable.pop()
    return self.iterable
#------------------------使用示例------------------------
if __name__ == "__main__":
  
  deleter1 = DeleteItem([0,1,2,3,4,5]) #实例化，把列表传入类中
  # 示例1 - 删除中间元素
  result1 = deleter1.delete(2)
  print("示例1 - 删除中间元素：",result1) # 输出：示例1 - 删除中间元素：[0,1,3,4,5]
  
  # 示例2 - 删除第一个元素
  deleter2 = DeleteItem(["a","b","c","d"])
  result2 = deleter2.delete(0)
  print("示例2 - 删除第一个元素：",result2) # 输出：示例2 - 删除第一个元素：["b","c","d"]
  
  # 示例3 - 删除最后一个元素
  deleter3 = DeleteItem([1.0,1.2,3.14,5.6])
  result3 = deleter3.delete(3)
  print("示例3 - 删除最后一个元素：",result3) # 输出：示例3 - 删除最后一个元素：[1.0,1.2,3.14]
