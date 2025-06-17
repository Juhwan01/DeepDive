# class HashTable:
#     def __init__(self, length=5):
#         self.max_len = length
#         self.table = [[]for _ in range(self.max_len)]
    
#     def _hash(self,key):
#         # ord함수 -> 문자를 아스키 코드로 변환해줌
#         res = sum([ ord(s) for s in key])
#         return res % self.max_len
    
#     def set(self, key, value):
#         index = self._hash(key)
#         self.table[index].append((key,value))
    
#     def get(self, key):
#         index = self._hash(key)
#         value = self.table[index]
#         if not value:
#             return None
#         for v in value:
#             if v[0] == key:
#                 return v[1]
#         return None

class HashTable:
    def __init__(self, length=5):
        self.max_len = length
        self.table = [[]for _ in range(self.max_len)]
        
    #hash 내장 함수 사용
    #키가 중복되면 덮어쓰는 방법
    def set(self, key, value):
        index = hash(key)%self.max_len
        for i, (k,v) in enumerate(self.table[index]):
            if k==key:
                self.table[index][i] = (key,value)
                return
        self.table[index].append((key,value))
         
    def get(self, key):
        index = hash(key)%self.max_len
        value = self.table[index]
        if not value:
            return None
        for v in value:
            if v[0] == key:
                return v[1]
        return None