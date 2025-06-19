"""
You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.

 

Example 1:

Input: cost = [10,15,20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.
Example 2:

Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.
"""

#Using Recursion (Time Limit Exceded)
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        return min(self.minCost(cost, n - 1), self.minCost(cost, n - 2))

    def minCost(self, cost: List[int], n: int):
        if n < 0:
            return 0
        if n == 0 or n == 1:
            return cost[n]
        return cost[n] + min(self.minCost(cost, n - 1), self.minCost(cost,n - 2))  

#Time Complexity :O(2^N)
#Space Complexity:O(N)


#Using Memoization (Time limit Exception)
from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        self.dp = [0] * n  # Initialize memoization list
        return min(self.minCost(cost, n - 1), self.minCost(cost, n - 2))

    def minCost(self, cost: List[int], n: int) -> int:
        if n < 0:
            return 0
        if n == 0 or n == 1:
            return cost[n]
        if self.dp[n] != 0:
            return self.dp[n]
        self.dp[n] = cost[n] + min(self.minCost(cost, n - 1), self.minCost(cost, n - 2))
        return self.dp[n]
#Time Complexity :O(N)
#Space Complexity:O(N)



#Using DP Tabulation
from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * (n + 1)
        for i in range(2, n + 1):
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        return dp[n]
#Time Complexity :O(N)
#Space Complexity:O(N)


#Using Space Optimization
from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n=len(cost)
        first=cost[0]
        second=cost[1]
        for i in range(2,n):
            curr=cost[i]+min(first,second)
            first=second
            second=curr
        return min(first,second)

#Time Complexity :O(N)
#Space Complexity:O(1)