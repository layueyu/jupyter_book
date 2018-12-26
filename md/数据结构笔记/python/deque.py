class Deque(object):
    def __init__(self):
        self.__list = []

    def add_front(self, item):
        """从对头加入一个元素"""
        self.__list.insert(0, item)

    def add_rear(self, item):
        """从对尾加入一个元素"""
        self.__list.append(item)

    def remove_front(self):
        """从对头删除一个元素"""
        return self.__list.pop(0)

    def remove_rear(self):
        """从对尾删除一个元素"""
        return self.__list.pop()

    def is_empty(self):
        """判断一个队列是否为空"""
        return not self.__list

    def size(self):
        """返回队列的大小"""
        return len(self.__list)


if __name__ == '__main__':
    dq = Deque()
    dq.add_front(1)
    dq.add_rear(2)
    dq.add_rear(3)
    dq.add_rear(4)
    dq.add_front(11)
    dq.add_front(12)
    dq.add_front(13)
    print(dq.remove_front())
    print(dq.remove_rear())


