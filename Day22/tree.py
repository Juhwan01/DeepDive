tree = ["A", "B", "C", "D", "E", "F", None, "G"]

i = 0
n = len(tree)

while i < n:
    if tree[i]:
        print(f"Parent: {tree[i]}", end = ", ")
        
        # 왼쪽 자식 인덱스 계산
        left = 2 * i + 1
        # 오른쪽 자식 인덱스 계산
        right = left + 1
        
        # 왼쪽 자식이 존재하면 출력
        if left < n and tree[left] is not None:
            print(f"Left: {tree[left]}", end = ", ")
            
        # 오른쪽 자식이 존재하면 출력
        if right < n and tree[right] is not None:
            print(f"Right: {tree[right]}", end = ", ")
            
        print()
    i += 1