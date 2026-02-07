''' Reverse a list without using reverse()
 I/O: [1, 2, 3, 4, 5]
 output: [5, 4, 3, 2, 1]

'''
def reverseList(lst):
    n=len(lst)
    arr=[]
    while n>0:
        arr.append(lst[n-1])
        n-=1
    return arr
print(reverseList([1, 2, 3, 4, 5]))

'''
Time complexity:O(n)
Space Complexity:O(n)
'''

#Optimized solution
def reverseList(arr):
    n=len(arr)
    for i in range(len(arr)//2):
        temp=arr[i]
        arr[i]=arr[n-(i+1)]
        arr[n-(i+1)]=temp
    return arr
print(reverseList([1, 2, 3, 4, 5]))

'''
Time complexity:O(n)
Space Complexity:O(1)
'''
#Another optimized solution
def reverseList(arr):
    n=len(arr)
    for i in range(len(arr)//2):
        arr[i],arr[n-(i+1)]=arr[n-(i+1)],arr[i]
    return arr
print(reverseList([1, 2, 3, 4, 5]))
'''
Time complexity:O(n)
Space Complexity:O(1)
'''