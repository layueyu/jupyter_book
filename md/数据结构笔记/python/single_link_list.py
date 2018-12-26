
class Node(object):
    """
    节点
    """
    def __init__(self, item):
        self.item = item
        self.next = None


class SingleLinkList(object):
    """
    单链表
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
            cur.next = node

    def insert(self, pos, item):
        """
        指定位置添加元素
        :param item:
        :param pos: 从0开始
        """
        if pos <= 0:
            self.add(item)
        else:
            count = 0
            pre = self.__head
            node = Node(item)
            while count < (pos-1) and pre.next is not None:
                count += 1
                pre = pre.next
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        """删除节点"""
        pre = None
        cur = self.__head
        while cur is not None:
            if cur.item == item:
                if cur == self.__head:
                    self.__head = cur.next
                else:
                    pre.next = cur.next
                break
            else:
                pre = cur
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
    ll = SingleLinkList()

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
    ll.remove(8)
    ll.travel()
