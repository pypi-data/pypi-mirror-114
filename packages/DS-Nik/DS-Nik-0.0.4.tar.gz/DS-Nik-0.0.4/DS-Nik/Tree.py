class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def traverseNode(self, node):
        if node:
            self.traverseNode(node.left)
            print(node.data)
            self.traverseNode(node.right)

    def traverse(self):
        self.traverseNode(self.root)

    def level_order_traversal(self):
        nodes = [self.root]
        while len(nodes) > 0:
            node = nodes[0]
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)
            print(node.data, end=' ')
            del(nodes[0])

    def removeNodeRec(self, root, data):
        if not root:
            return None
        if root.data > data:
            root.left = self.removeNode(root.left, data)
        elif root.data < data:
            root.right = self.removeNode(root.right, data)
        else:
            if not root.left and not root.right:
                root = None
            elif root.left:
                root = root.left
            elif root.right:
                root = root.right
            else:
                tempNode = self.getMaximum(root.left)
                root.data = tempNode.data
                root.left = self.removeNode(root.left, tempNode.data)
        return root

    def removeNodeIter(self, data):
        currNode = self.root
        parentNode = None
        if not currNode:
            return print('Currently no nodes in the tree')
        while currNode.data != data:
            if currNode.data > data:
                parentNode = currNode
                currNode = currNode.left
            elif currNode.data < data:
                parentNode = currNode
                currNode = currNode.right
        if parentNode.left == currNode:
            pass;
        else:
            pass;
            
        if parentNode.left and parentNode.left.data == currNode.data:
            if not currNode.left and not currNode.right:
                currNode = None
            elif currNode.left:
                parentNode.left = currNode.left
            elif currNode.right:
                parentNode.left = currNode.right
            else:
                tempNode = self.getMaximum(currNode.left)
                currNode.data = tempNode.data
                self.remove(tempNode.data)
        else:
            if not currNode.left and not currNode.right:
                currNode = None
            elif currNode.left:
                parentNode.right = currNode.left
            elif currNode.right:
                parentNode.right = currNode.right
            else:
                tempNode = self.getMaximum(currNode.left)
                currNode.data = tempNode.data
                self.remove(tempNode.data)

    def getMaximum(self, node):
        while node.right:
            node = node.right
        return node
        
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
            return

        node = self.root
        is_inserted = False
        while not is_inserted:
            if data > node.data:
                if node.right == None:
                    node.right = Node(data)
                    is_inserted = True
                else:
                    node = node.right
            else:
                if node.left == None:
                    node.left = Node(data)
                    is_inserted = True
                else:
                    node = node.left
