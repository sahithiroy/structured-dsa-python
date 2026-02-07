'''
Docstring for python-core-day1.countFrequencyCharacters

Count frequency of characters in a string
I/P:"hello"
O/P:{'h': 1, 'e': 1, 'l': 2, 'o': 1}
'''
def countFrequencyCharacters(s):
    dict={}
    for i in range(len(s)):
        if s[i] not in dict:
            dict[s[i]]=1
        else:
            dict[s[i]]+=1
    return dict
print(countFrequencyCharacters("hello"))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

#Optimized solution using collections module
from collections import Counter
def countFrequencyCharacters(s):
    return dict(Counter(s))
print(countFrequencyCharacters("hello"))
'''Time complexity:O(n)
Space Complexity:O(n)'''


def count_frequency(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq
print(count_frequency("hello"))

'''“I can implement it manually in O(n) using a dictionary. 
Python also provides Counter, which internally does the same thing more efficiently.
This counts all characters including spaces and is case-sensitive.”'''