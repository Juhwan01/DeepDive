def first_unique_char(string):
    count = {}
    for c in string:
        count[c] = count.get(c,0)+1
    for k,v in count.items():
        if v==1:
            for i,c in enumerate(string):
                if k==c:
                    return i
    return -1

for s in ("leetcode","loveleetcode","aabb"):
    print(first_unique_char(s))