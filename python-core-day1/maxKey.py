'''
Docstring for python-core-day1.maxKey
Find key with max value (without using max())
I/P:{1: 2, 3: 4, 5: 6}
O/P:5
'''
def maxKey(d):
    max_key = None
    max_value = float('-inf')
    for key, value in d.items():
        if value > max_value:
            max_value = value
            max_key = key
    return max_key
print(maxKey({1: 2, 3: 4, 5: 6}))
'''Time complexity:O(n)
Space Complexity:O(1)'''
