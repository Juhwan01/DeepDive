class Node:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def preorder(self):
        res = []
        def _preorder(node):
            if node is None:
                return
            res.append(node.data)
            _preorder(node.left)
            _preorder(node.right)
        _preorder(self.root)
        return res
    
    def inorder(self):
        res = []
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left)
            res.append(node.data)
            _inorder(node.right)
        _inorder(self.root)
        return res
    
    def postorder(self):
        res = []
        def _postorder(node):
            if node  is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            res.append(node.data)
        _postorder(self.root)
        return res
    
    def levelorder(self):
        res = []
        if not self.root:
            return res
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            res.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return res
    
    def make_tree(self, arr):
        if not arr:  # 배열이 비어있으면 종료
            return
            
        # 루트 노드 생성 (배열의 첫 번째 원소)
        self.root = Node(arr[0])
        q = [self.root]  # 큐에 루트 노드 추가
        index = 1  # 배열의 두 번째 원소부터 시작
        
        # 큐가 비어있지 않고, 배열의 모든 원소를 처리할 때까지
        while q and index < len(arr):
            # 현재 노드를 큐에서 꺼냄
            node = q.pop(0)
            
            # 왼쪽 자식 처리
            if index < len(arr) and arr[index] is not None:
                node.left = Node(arr[index])  # 왼쪽 자식 노드 생성
                q.append(node.left)  # 큐에 추가
            index += 1
            
            # 오른쪽 자식 처리
            if index < len(arr) and arr[index] is not None:
                node.right = Node(arr[index])  # 오른쪽 자식 노드 생성
                q.append(node.right)  # 큐에 추가
            index += 1