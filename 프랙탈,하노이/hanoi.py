def hanoi(n, source, destination, auxiliary):
    if n == 1:
        print(f"{source} → {destination}")
        return
    
    hanoi(n-1, source, auxiliary, destination)
    print(f"{source} → {destination}")
    hanoi(n-1, auxiliary, destination, source)

# 실행 및 검증
print("=== 하노이 탑 3개 원판 ===")
hanoi(3, 'A', 'C', 'B')

print("\n=== 이동 횟수 검증 ===")
def count_hanoi_moves(n):
    count = 0
    
    def hanoi_counter(n, source, destination, auxiliary):
        nonlocal count
        if n == 1:
            count += 1
            return
        
        hanoi_counter(n-1, source, auxiliary, destination)
        count += 1
        hanoi_counter(n-1, auxiliary, destination, source)
    
    hanoi_counter(n, 'A', 'C', 'B')
    return count

for n in range(1, 6):
    actual = count_hanoi_moves(n)
    formula = (2 ** n) - 1
    print(f"{n}개 원판: 실제={actual}, 공식={formula}, 일치={actual == formula}")

print("\n✅ 하노이 탑 구현 완료 및 검증 성공!")