'''
Docstring for python-core-day1.secongLargest
Find the second largest element in a list
I/P:[1, 2, 3, 4, 5]
O/P:4
'''

# If the array is sorted then we can easily find the second largest element by accessing the second last element of the array but if the array is not sorted then we can use the following approach
def secondLargest(lst):
    return lst[-2]
print(secondLargest([1, 2, 3, 4, 5]))
'''
Time complexity:O(1)
Space Complexity:O(1)'''
#if the array is not sorted then we can use the following approach
def secondLargest(lst):
    lst.sort()
    return lst[-2]
print(secondLargest([1, 2, 3, 4, 5]))
'''
Time complexity:O(nlogn)
Space Complexity:O(1)'''

#optimized solution
def secondLargest(lst):
    if len(lst)<2:
        return None
    first=second=float('-inf')
    for i in range(len(lst)):
        if lst[i]>first:
            second=first
            first=lst[i]
        elif lst[i]>second and lst[i]!=first:
            second=lst[i]
    return second
'''
Time complexity:O(n)
Space Complexity:O(1)'''

#Interview explanation (memorize)
def second_largest(lst):
    if len(lst) < 2:
        return None

    first = second = float('-inf')

    for num in lst:
        if num > first:
            second = first
            first = num
        elif first > num > second:
            second = num

    return second if second != float('-inf') else None

'''
INTERVIEW EXPLANATION (MEMORIZE THIS)

“Sorting works but costs O(n log n).
A single-pass approach tracks the largest and second largest values in O(n) time.
I also handle edge cases like duplicates and insufficient elements.”'''