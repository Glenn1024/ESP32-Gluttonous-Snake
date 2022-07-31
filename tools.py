class DoubleNode:
    def __init__(self, val=None, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev 

class DoubleLinkedList:
    '''双向链表'''
    def __init__(self, node=None):
        self.head = node
        self.tail = self.head
        self.length = 0
        if node:
            self.length+=1

    def append(self, node):
        '''尾插'''
        if self.length:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = node
            self.tail = self.head
        self.length+=1
    
    def add(self, node):
        '''头插'''
        if self.length:
            self.head.prev = node
            node.next = self.head
            self.head = node
        else:
            self.head = node
            self.tail = self.head
        self.length+=1

    def pop(self):
        '''尾删除'''
        self.tail = self.tail.prev
        node = self.tail.next
        self.tail.next = None
        return node