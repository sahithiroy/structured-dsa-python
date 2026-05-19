'''
Docstring for python-core-day1.commonElementsList
Find common elements between two lists
I/P:[1,2,3,4],[3,4,5,6]
O/P:[3,4]
'''
def commonElementsList(lst1, lst2):
    set1=set(lst1)
    set2=set(lst2)
    common_elements=list(set1.intersection(set2))
    return common_elements
print(commonElementsList([1,2,3,4],[3,4,5,6]))
'''Complexity (correct)

Time: O(n + m)

Building sets: O(n), O(m)

Intersection: O(min(n, m))

Space: O(n + m)'''    
#optimized solution using list comprehension
def commonElementsList(lst1, lst2): 
    return [num for num in lst1 if num in lst2]
print(commonElementsList([1,2,3,4],[3,4,5,6]))
'''Time complexity:O(n^2)       
Space Complexity:O(n)'''       

def common_elements(lst1, lst2):
    set2 = set(lst2)
    return [x for x in lst1 if x in set2]

print(common_elements([1,2,3,4],[3,4,5,6]))
'''Time complexity:O(n + m)     
Space Complexity:O(m)'''



