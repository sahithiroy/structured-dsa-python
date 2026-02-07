'''
Docstring for python-core-day1.missingNumber
Find missing number in a sequence
I/P:[1,2,4,5]
O/P:3
'''
def missing_number(nums):
    n=len(nums)+1
    total_sum=(n*(n+1))/2
    actual_sum=0
    for num in nums:
        actual_sum+=num
    return total_sum-actual_sum
print(missing_number([1,2,4]))
'''
Time Complexity: O(n)
Space Complexity: O(1)
'''
def missing_number(nums):
    n = len(nums) + 1
    total_sum = n * (n + 1) // 2   # integer division
    actual_sum = sum(nums)
    return total_sum - actual_sum

print(missing_number([1, 2, 4]))

def missing_number(nums):
    n = len(nums) + 1
    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i
    for num in nums:
        xor_all ^= num
    return xor_all

print(missing_number([1, 2, 4]))
'''
Time Complexity: O(n)
Space Complexity: O(1)    
'''