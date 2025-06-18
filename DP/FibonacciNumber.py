"""
The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1. That is,

F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.
Given n, calculate F(n).

 

Example 1:

Input: n = 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1.
Example 2:

Input: n = 3
Output: 2
Explanation: F(3) = F(2) + F(1) = 1 + 1 = 2.
Example 3:

Input: n = 4
Output: 3
Explanation: F(4) = F(3) + F(2) = 2 + 1 = 3.
"""

#Using Recursion
class Solution:
    def fib(self, n: int) -> int:
        if n==0 or n==1:
            return n
        return self.fib(n-1)+self.fib(n-2)
#Time Complexity :O(2^N)
#Space Complexity:O(N)


#Using Memoization
class Solution:
    def fib(self, n: int) -> int:
        memo = {}
        return self.helper(n, memo)
    
    def helper(self, n: int, memo: dict[int, int]) -> int:
        if n == 0 or n == 1:
            return n
        if n not in memo:
            memo[n] = self.helper(n-1, memo) + self.helper(n-2, memo)
        return memo[n]
        
#Time Complexity :O(N)
#Space Complexity:O(N)

#using DP
class Solution:
    def fib(self, n: int) -> int:
        if n==0 or n==1:
            return n
        dp=[0]*(n+1)
        dp[0]=0
        dp[1]=1
        for i in range(2,n+1):
            dp[i]=dp[i-1]+dp[i-2]
        return dp[n]
#Time Complexity :O(N)
#Space Complexity:O(N)



#Using Space Optimization
class Solution:
    def fib(self, n: int) -> int:
        if n==0 or n==1:
            return n
        prev,curr=0,1
        for i in range(2,n+1):
            temp=curr
            curr=prev+curr
            prev=temp
        return curr
#Time Complexity :O(N)
#Space Complexity:O(1)