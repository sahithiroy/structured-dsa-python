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

'''what's the meaning of float('-inf')?
float('-inf') represents negative infinity in Python. It's a special floating-point value that is smaller than any other number. 
In the context of finding the maximum key, we initialize max_value to float('-inf') so that any value in the dictionary will be greater than this initial value, 
ensuring that the first comparison will update max_value and max_key correctly.'''