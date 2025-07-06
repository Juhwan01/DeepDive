import math

class FractalTree:
    def __init__(self):
        self.branches = []
    
    def draw_tree(self, x, y, length, angle, depth):
        if depth == 0:
            return
        
        end_x = x + length * math.cos(angle)
        end_y = y + length * math.sin(angle)
        
        self.branches.append(((x, y), (end_x, end_y)))
        
        new_length = length * 0.7
        angle_offset = math.pi / 6
        
        self.draw_tree(end_x, end_y, new_length, angle - angle_offset, depth - 1)
        self.draw_tree(end_x, end_y, new_length, angle + angle_offset, depth - 1)
    
    def print_tree(self):
        for i, branch in enumerate(self.branches, 1):
            start, end = branch
            print(f"{i:2d}. ({start[0]:5.1f}, {start[1]:6.1f}) → ({end[0]:5.1f}, {end[1]:6.1f})")

# 실행 및 검증
print("=== 프랙탈 트리 깊이 4 ===")
tree = FractalTree()
tree.draw_tree(0, 0, 100, -math.pi/2, 4)
tree.print_tree()
print(f"\n총 가지 수: {len(tree.branches)}개")

print("\n=== 가지 수 검증 ===")
for depth in range(1, 5):
    test_tree = FractalTree()
    test_tree.draw_tree(0, 0, 100, -math.pi/2, depth)
    actual = len(test_tree.branches)
    expected = (2 ** depth) - 1
    print(f"깊이 {depth}: 실제={actual:2d}개, 예상={expected:2d}개, 일치={actual == expected}")

print("\n✅ 프랙탈 트리 구현 완료 및 검증 성공!")