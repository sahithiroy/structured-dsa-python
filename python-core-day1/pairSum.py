'''
Docstring for python-core-day1.pairSum
Count pairs with a given sum

I/P:[1,2,3,4,5],5
O/P:2 (1,4) and (2,3)
'''
def count_pairs(nums, target_sum):
    count=0
    for num in nums:
        if target_sum-num in nums:
            count+=1
    return count//2
print(count_pairs([1,2,3,4,5],5))
''' 
Time Complexity: O(n^2)
Space Complexity: O(1)
'''
def count_pairs(nums, target_sum):
    count = 0
    seen = set()
    for num in nums:
        complement = target_sum - num
        if complement in seen:
            count += 1
        seen.add(num)
    return count    

print(count_pairs([1, 2, 3, 4, 5], 5))
'''
Time Complexity: O(n)   
Space Complexity: O(n)    
'''