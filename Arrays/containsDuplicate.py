#Uisng BruteForce
class Solution:
    def hasDuplicate(self, nums: list[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False
    
#Time Complexity :O(N**2)
#Space Complexity:O(1)



#Using Sorting
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        nums.sort()
        for i in range(len(nums)-1):
            if nums[i]==nums[i+1]:
                return True
        return False
#Time Complexity O(NlogN)
#Space Complexity O(1)


#Using HashMap
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        dict={}
        for i in nums:
            if i not in dict:
                dict[i]=1
            else:
                dict[i]+=1
                 
                return True
        return False
#Time Complexity :O(N)
#Space Complexity:O(N)


#Uisng HashSetLength
class Solution:
    def hasDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)
        
#Time Complexity :O(N)
#Space Complexity:O(N)