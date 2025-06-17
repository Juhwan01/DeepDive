class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        
    def push(self,data):
        if self.top is None:
            self.top = Node(data)
        else:
            node = Node(data)
            node.next = self.top
            self.top = node
            
    def pop(self):
        if self.top is None:
            return None
        else:
            node = self.top
            self.top = self.top.next
            return node.data
    
    def peek(self):
        if self.top is None:
            return None
        else:
            self.top.data
            
    def is_empty(self):
        return self.top is None
  
  
    
## 예제 1
def reverse_word(str):
    s = Stack()
    for char in str:
        s.push(char)
    
    result=""
    while s.top is not None:
        result+=s.pop()
    return result

print(reverse_word("aircraft"))
    
