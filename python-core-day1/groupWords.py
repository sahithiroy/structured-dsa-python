'''
Docstring for python-core-day1.groupWords
Group words by length
I/P:["cat","dog","apple","bat"]
O/P:{3: ['cat', 'dog', 'bat'], 5: ['apple']}
'''
def groupWords(words):
    dict={}
    for word in words:
        length=len(word)
        if length not in dict:
            dict[length]=[word]
        else:
            dict[length].append(word)
    return dict
print(groupWords(["cat","dog","apple","bat"]))
'''
Time complexity:O(n)
Space Complexity:O(n)'''
#Optimized solution using collections module
from collections import defaultdict 
def groupWords(words):
    dict=defaultdict(list)
    for word in words:
        dict[len(word)].append(word)
    return dict
print(groupWords(["cat","dog","apple","bat"]))
'''Time complexity:O(n)
Space Complexity:O(n)'''
from collections import defaultdict

def groupWords(words):
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return groups

'''
Say this out loud:

This is a hash-based grouping

Same pattern as SQL GROUP BY

Same logic underlies Pandas groupby

defaultdict avoids conditional logic

Complexity depends on number of elements, not group count
I iterate once, compute the word length, and use it as a dictionary key mapping to a list.
 defaultdict lets me avoid existence checks.
 Time and space are linear.'''


'''what's the difference between dict vs defaultdict
A regular dict raises a KeyError if you try to access a key that doesn't exist.
A defaultdict, on the other hand, provides a default value for a key that doesn't exist. 
When you access a key that isn't present in the defaultdict, it automatically creates an entry for that key with a default value (like an empty list, 0, etc.)
 based on the type specified when creating the defaultdict.'''