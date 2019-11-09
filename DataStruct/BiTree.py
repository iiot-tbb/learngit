#!/usr/bin/env python
# coding=utf-8
class BitNode:
    def __init__(self,data):
        self.data = data
        self.left =None
        self.right=None
        return

    def has_value(self,value):
        if self.data == value:
            return True
        else:
            return False

class BitTree:
    def __init__(self):
        self.root = None
        self.bitList = []

    def add_bit_item(self, item):
        if not isinstance(item,BitNode):
            item = BitNode(item)

        if self.root is None:
            self.root = item
            self.bitList.append(item)
        else:
            rootNode = self.bitList[0]
            while True:
                if item.data < rootNode.data:
                    '''往左移'''
                    if rootNode.left == None:
                        rootNode.left = item
                        self.bitList.append(item)
                        break
                    else:
                        rootNode =rootNode.left
                elif item.data >rootNode.data:
                    '''往右移'''
                    if rootNode.right == None:
                        rootNode.right = item
                        self.bitList.append(item)
                        break
                    else:
                        rootNode =rootNode.right

    def front_reaverse(self,root):
        if root==None:
            return
        print(root.data)
        self.front_reaverse(root.left)
        self.front_reaverse(root.right)
    
    def middle_traverse(self,root):
        if root==None:
            return
        self.middle_traverse(root.left)
        print(root.data)
        self.middle_traverse(root.right)
    
    def last_traverse(self,root):
        if root ==None:
            return
        self.last_traverse(root.left)
        self.last_traverse(root.right) 
        print(root.data)
    
    def floor_traverse(self,root):
        from collections import deque
        q= deque()
        if root == None:
            return
        q.append(root)
        while q:
            node = q.popleft()
            print(node.data)
            if node.left != None:
                q.append(node.left)
            if node.right != None:
                q.append(node.right)

if __name__ == '__main__':
    node1 = BitNode(15)
    node2 =BitNode(9)
    node3 =BitNode(8)
    node4 =BitNode(16)
    bitree =BitTree()
    for i in [node1, node2, node3, node4]:
        bitree.add_bit_item(i)
    print('\n\n\n----last_traverse-----:')
    bitree.last_traverse(bitree.root)
    print('\n\n\n----front_traverse-----:')
    bitree.front_reaverse(bitree.root)   
    print('\n\n\n----middle_traverse-----:')
    bitree.middle_traverse(bitree.root)
    print('\n\n\n----floor_traverse-----:')
    bitree.floor_traverse(bitree.root)




