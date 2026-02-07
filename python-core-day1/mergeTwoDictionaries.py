'''
Docstring for python-core-day1.mergeTwoDictionaries
Merge two dictionaries (sum values if keys match)
I/P:dict1={1: 2, 3: 4}, dict2={1: 3, 5: 6}
O/P:{1: 5, 3: 4, 5: 6}
'''
def mergeDictionaries(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged:
            merged[key] += value
        else:
            merged[key] = value
    return merged
print(mergeDictionaries({1: 2, 3: 4}, {1: 3, 5: 6}))
''' Time complexity:O(n + m)
Space Complexity:O(n + m)'''
#Optimized solution using collections module
from collections import Counter 
def mergeDictionaries(dict1, dict2):
    merged = Counter(dict1) + Counter(dict2)
    return dict(merged) 
print(mergeDictionaries({1: 2, 3: 4}, {1: 3, 5: 6}))
'''Time complexity:O(n + m)
Space Complexity:O(n + m)'''
def merge_dictionaries(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        merged[key] = merged.get(key, 0) + value
    return merged

print(merge_dictionaries({1: 2, 3: 4}, {1: 3, 5: 6}))
'''Say these out loud:

Dictionary merging is a reduction operation

.get() simplifies accumulation logic

Copying avoids side effects

Counters are specialized dicts, not magic

Edge cases matter (negative / zero values)'''

