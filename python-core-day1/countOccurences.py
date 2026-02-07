'''
Docstring for python-core-day1.countOccurences
Count occurrences in a list 

I/P:[1,2,2,3,3,3]
O/P:{1: 1, 2: 2, 3: 3}
'''
def countOccurrences(lst):
    dict={}
    for num in lst:
        dict[num]=dict.get(num,0)+1
    return dict
print(countOccurrences([1,2,2,3,3,3]))
'''
Time complexity:O(n)
Space Complexity:O(n)'''
#Optimized solution using collections module
from collections import Counter
def countOccurrences(lst):
    return dict(Counter(lst))
print(countOccurrences([1,2,2,3,3,3]))
'''Time complexity:O(n)
Space Complexity:O(n)'''