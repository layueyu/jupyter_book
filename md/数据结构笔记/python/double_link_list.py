class Node(object):
    """节点"""
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None


class DoubleLinkList(object):
    """
        双列表
    """
    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        """ 链表是否为空 """
        return self.__head is None

    def length(self):
        """ 链表长度 """
        # cur 游标，用来移动遍历节点
        cur = self.__head

        # count 记录数量
        count = 0

        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """ 遍历整个链表 """
        cur = self.__head
        while cur is not None:
            print(cur.item, end=' ')
            cur = cur.next
        print()

    def add(self, item):
        """ 链表头部添加元素，头插法 """
        node = Node(item)
        self.__head.prev = node
        node.next = self.__head
        self.__head = node

    def append(self, item):
        """ 链表尾部添加元素, 尾插法 """
        node = Node(item)
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next is not None:
                cur = cur.next
            node.prev = cur
            cur.next = node

    def insert(self, pos, item):
        """
        指定位置添加元素
        :param item:
        :param pos: 从0开始
        """
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:
            count = 0
            cur = self.__head
            node = Node(item)
            while count < pos:
                count += 1
                cur = cur.next
            node.next = cur
            node.prev = cur.prev
            cur.prev.next = node
            cur.prev = node

    def remove(self, item):
        """删除节点"""
        cur = self.__head
        while cur is not None:
            if cur.item == item:
                if cur == self.__head:
                    self.__head = cur.next
                    if cur.next is not None:
                        cur.next.prev = None
                else:
                    if cur.next is not None:
                        cur.next.prev = cur.prev
                    cur.prev.next = cur.next

                break
            else:
                cur = cur.next

    def search(self, item):
        """ 查找节点是否存在 """
        cur = self.__head
        while cur is not None:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        return False


if __name__ == '__main__':

    dl = DoubleLinkList()

    print('lem:', dl.length())
    print('is:', dl.is_empty())

    dl.append(1)
    dl.append(2)
    dl.append(3)
    dl.append(4)
    dl.append(5)
    dl.append(6)
    dl.insert(6, 13)
    dl.travel()
    dl.remove(1)

    dl.travel()
