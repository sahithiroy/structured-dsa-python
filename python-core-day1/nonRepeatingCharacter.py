'''
Docstring for python-core-day1.nonRepeatingCharacter
Find first non-repeating character in a string
I/P:"hello"
O/P:'h'
'''
def firstNonRepeatingCharacter(s):
    dict={}
    arr=[]
    for num in s:
        if num not in dict:
            arr.append(num)
            dict[num]=1
        else:
            arr.remove(num)
    return arr[0]
print(firstNonRepeatingCharacter('sahithi'))
'''
Time complexity:O(n)
Space Complexity:O(n)'''
#Optimized solution using collections module
from collections import Counter
def firstNonRepeatingCharacter(s):
    freq=Counter(s)
    for char in s:
        if freq[char]==1:
            return char
    return None
print(firstNonRepeatingCharacter('sahithi'))
'''Time complexity:O(n)
Space Complexity:O(n)'''

def first_non_repeating(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    for ch in s:
        if freq[ch] == 1:
            return ch

    return None
print(first_non_repeating('sahithi'))