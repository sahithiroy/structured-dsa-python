'''
Docstring for python-core-day1.detectDuplicates
Detect duplicates in a list
I/P:[1, 2, 3, 2, 4, 1]
O/P:True
'''
def detectDuplicates(lst):
    arr=set(lst)
    return len(arr)!=len(lst)

'''Time complexity:O(n)
Space Complexity:O(n)'''

#optimized solution using dict
def detectDuplicates(lst):
    dict={}
    for num in lst:
        if num in dict:
            return True
        else:
            dict[num]=1
    return False
print(detectDuplicates([1, 2, 3, 2, 4, 1]))
'''Time complexity:O(n)
Space Complexity:O(n)'''


def detect_duplicates(lst):
    seen = set()
    for num in lst:
        if num in seen:
            return True
        seen.add(num)
    return False