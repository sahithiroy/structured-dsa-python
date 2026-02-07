'''Split a list into chunks of size n

Rules:

Handle leftover elements

Handle invalid n

Explain time & space
I/p=[1, 2, 3, 4, 5], n=2
O/P=[[1, 2], [3, 4], [5]]'''
def chunk(lst,n):
    if n<=0:
        return []
    arr=[]
    for i in range(0,len(lst),n):
        arr.append(lst[i:i+n])
    return arr
print(chunk([1, 2, 3, 4, 5],2))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

'''
“I iterate in steps of n and slice the list into sublists.
 Python slicing naturally handles leftover elements, and I guard against invalid n values.”'''
#Manual implementation without slicing
def chunk_manual(lst, n):
    if n <= 0:
        return []

    result = []
    temp = []

    for item in lst:
        temp.append(item)
        if len(temp) == n:
            result.append(temp)
            temp = []

    if temp:
        result.append(temp)

    return result
