class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        node = self.head
        while node:
            print(node.data)
            node = node.next

    def insert(self, data):
        if not self.head:
            self.head = Node(data)
            return
        node = self.head
        while node.next != None:
            node = node.next
        node.next = Node(data)
    
    def remove(self, data):
        if self.head.data == data:
            self.head = self.head.next
            return
        
        node = self.head
        while node.next and node.next.data != data:
            node = node.next

        node.next = node.next.next
        return