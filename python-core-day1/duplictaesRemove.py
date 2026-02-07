'''
Docstring for python-core-day1.duplictaesRemove
Remove duplicates from a list while preserving order
I/P:[1, 2, 3, 2, 4, 1]
O/P:[1, 2, 3, 4]
'''
def removeDuplicates(lst):
    arr=set(lst)
    return list(arr)
print(removeDuplicates([1, 2, 3, 2, 4, 1]))
'''
Time complexity:O(n)
Space Complexity:O(n)'''
#Optimized solution
def removeDuplicates(lst):
    dict={}
    for i in range(len(lst)):
         if lst[i] not in dict :
             dict[lst[i]]=i
    print(dict)
    
    return list(dict.keys())
print(removeDuplicates([1, 2, 3, 2, 4, 1]))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

#Another optimized solution

def removeDuplicates(lst):
    if not lst:
        return []

    j = 0
    for i in range(1, len(lst)):
        if lst[i] != lst[j]:
            j += 1
            lst[j] = lst[i]

    return lst[:j+1]

print(removeDuplicates([1,1,2,2,3,4]))
'''
Time complexity:O(n)
Space Complexity:O(1)'''


#Another optimized solution using dict above i make mistake i am using dict to remove duplicates but it is not preserving order so i am using list to preserve order and dict to check if element is already present or not
def remove_duplicates_preserve_order(lst):
    seen = {}
    for item in lst:
        if item not in seen:
            seen[item] = True
    return list(seen.keys())

'''
INTERVIEW EXPLANATION (MEMORIZE)

“Using a set removes duplicates but doesn’t preserve order.
Using a dictionary preserves insertion order in Python, making it suitable here.
A two-pointer approach only works if the list is sorted.”
'''