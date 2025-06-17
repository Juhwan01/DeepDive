class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)

    
node = Node(0)

node.next = head
head = node

while node:
    print(node.data)
    node = node.next