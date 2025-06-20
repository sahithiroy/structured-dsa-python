"""
53. Maximum Subarray
Given an integer array nums, find the subarray with the largest sum, and return its sum.

 

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
"""


#Uisng BruteForce Approach

import sys

def maxSubarraySum(arr, n):
    maxi = -sys.maxsize - 1  # maximum sum

    for i in range(n):
        for j in range(i, n):
            # subarray = arr[i.....j]
            summ = 0

            # add all the elements of subarray:
            for k in range(i, j+1):
                summ += arr[k]

            maxi = max(maxi, summ)

    return maxi
#Time Complexity :O(N**3)
#Space Complexity:O(1)



#Using Better Approach
def maxSubarraySum(arr, n):
    maxi = -sys.maxsize - 1 # maximum sum

    for i in range(n):
        sum = 0
        for j in range(i, n):
            # current subarray = arr[i.....j]

            #add the current element arr[j]
            # to the sum i.e. sum of arr[i...j-1]
            sum += arr[j]

            maxi = max(maxi, sum) # getting the maximum

    return maxi

#Time Complexity :O(N**2)
#Space Complexity:O(1)



#Using Optimization
from typing import List
import sys
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        maxi = -sys.maxsize-1
        sum=0
        for i in range(len(nums)):
            sum+=nums[i]
            if sum>maxi:
                maxi=sum
            if sum<0:
                sum=0
        return maxi

#Time Complexity :O(N)
#Space Complexity:O(1)