'''Rotate a list by k positions
I/P:[1, 2, 3, 4, 5], k=2
O/P:[4, 5, 1, 2, 3]'''

def rotateByKElements(lst,k):
    arr=[]
    n=len(lst)
    for i in range(k,n):
        arr.append(lst[i])
    for i in range(k):
        arr.append(lst[i])
    return arr
print(rotateByKElements([1,2,3,4,5],2))
'''
Time complexity:O(n)
Space Complexity:O(n)'''
#Optimized solution
'''Left Rotattion'''
def rotateByKElements(lst,k):
    n=len(lst)
    k=k%n
    return lst[k:]+lst[:k]
print(rotateByKElements([1,2,3,4,5],2))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

'''Right Rotation'''
def rotate_right(lst, k):
    n = len(lst)
    if n == 0:
        return lst

    k = k % n
    return lst[-k:] + lst[:-k]

print(rotate_right([1, 2, 3, 4, 5], 2))
'''
Time complexity:O(n)
Space Complexity:O(n)'''


#Interview algorithm explanation
def rotate_right_inplace(lst, k):
    n = len(lst)
    if n == 0:
        return lst

    k = k % n

    def reverse(start, end):
        while start < end:
            lst[start], lst[end] = lst[end], lst[start]
            start += 1
            end -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

    return lst
print(rotate_right_inplace([1, 2, 3, 4, 5], 2))
'''
“There are two versions.
Using slicing is simpler but uses O(n) extra space.
The optimized solution reverses parts of the array to rotate in-place with O(1) space.”
'''

'''Instead of simulating each rotation one by one, we can get the rotated array in-place by reversing specific parts of the array. This works because rotating is just rearranging sections of the array.
For Right Rotation by k steps:
Reverse the entire array
Reverse the first k elements
Reverse the remaining n - k elements
For Left Rotation by k steps:
Reverse the first k elements
Reverse the remaining n - k elements
Reverse the entire array
Normalize k by doing k = k % N
If direction is "right":
Reverse the entire array
Reverse the first k elements
Reverse the rest (from k to end)
If direction is "left":
Reverse the first k elements
Reverse the rest (from k to end)
Reverse the entire array'''