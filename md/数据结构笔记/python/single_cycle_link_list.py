
class Node(object):
    """
    节点
    """
    def __init__(self, item):
        self.item = item
        self.next = None


class SingleCycleLinkList(object):
    """
    单循环链表
    """
    def __init__(self, node=None):
        self.__head = node
        if node is not None:
            node.next = self.__head

    def is_empty(self):
        """ 链表是否为空 """
        return self.__head is None

    def length(self):
        """ 链表长度 """
        if self.is_empty():
            return 0
        # cur 游标，用来移动遍历节点
        cur = self.__head

        # count 记录数量
        count = 1
        while cur.next != self.__head:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """ 遍历整个链表 """
        if self.is_empty():
            return

        cur = self.__head
        while cur.next != self.__head:
            print(cur.item, end=' ')
            cur = cur.next
        # 退出循环，cur指向尾节点，尾节点的元素未打印
        print(cur.item, end=' ')
        print()

    def add(self, item):
        """ 链表头部添加元素，头插法 """
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = self.__head
            return
        cur = self.__head
        while cur.next != self.__head:
            cur = cur.next
        # 退出循环，cur指向最后节点
        cur.next = node
        node.next = self.__head
        self.__head = node

    def append(self, item):
        """ 链表尾部添加元素, 尾插法 """
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = self.__head
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            cur.next = node
            node.next = self.__head

    def insert(self, pos, item):
        """
        指定位置添加元素
        :param item:
        :param pos: 从0开始
        """
        if pos <= 0:
            self.add(item)

        elif pos > self.length():
            self.append(item)

        else:
            count = 0
            pre = self.__head
            node = Node(item)
            while count < (pos-1):
                count += 1
                pre = pre.next
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        """删除节点"""

        if self.is_empty():
            return

        pre = None
        cur = self.__head
        while cur.next != self.__head:
            if cur.item == item:
                if cur == self.__head:
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    self.__head = cur.next
                    rear.next = self.__head
                else:
                    pre.next = cur.next
                return
            else:
                pre = cur
                cur = cur.next
        if cur.item == item:
            # if pre is not None:
            if cur != self.__head:
                pre.next = self.__head
            else:
                self.__head = None

    def search(self, item):
        """ 查找节点是否存在 """

        if self.is_empty():
            return False

        cur = self.__head
        while cur.next != self.__head:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        if cur.item == item:
            return True
        return False


if __name__ == '__main__':
    ll = SingleCycleLinkList()

    print('is_empty:', ll.is_empty())
    print('len:', ll.length())

    ll.append(1)
    print('is_empty:', ll.is_empty())
    print('len:', ll.length())

    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    ll.append(6)
    ll.travel()
    ll.remove(1)
    ll.travel()

