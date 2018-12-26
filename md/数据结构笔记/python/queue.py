
class Queue(object):

    def __init__(self):
        self.__list = []

    """队列"""
    def enqueue(self, item):
        """往队列中添加一个item元素"""
        self.__list.append(item)

    def dequeue(self):
        """从队列头部删除一个元素"""
        if self.__list:
            return self.__list.pop(0)
        else:
            return None

    def is_empty(self):
        """判断一个队列是否为空"""
        return not self.__list

    def size(self):
        """返回队列的大小"""
        return len(self.__list)


if __name__ == '__main__':
    q = Queue()

    q.enqueue(1)
    print(q.is_empty())
    print(q.size())
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
