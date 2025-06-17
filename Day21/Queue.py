class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        
    def enqueue(self,data):
        if self.front is None:
            self.front = self.rear = Node(data)
        else:
            node = Node(data)
            self.rear.next = node
            self.rear = node
        
    def dequeue(self):
        if self.front is None:
            return None

        node = self.front
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
        return node.data
    
    def is_empty(self):
        return self.front is None

from stack import Stack
      
# 큐 뒤집기 - 스택을 이용한방법
def reverse_queue(q:Queue):
    s = Stack()
    answer=""
    while not q.is_empty():
        node = q.dequeue()
        s.push(node)
    while not s.is_empty():
        node = s.pop()
        answer+=node
    print(answer)
    
q = Queue()
for char in "hello":
    q.enqueue(char)

reverse_queue(q)