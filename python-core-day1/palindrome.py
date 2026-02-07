'''
Docstring for python-core-day1.palindrome

Check if a string is a palindrome 
I/p="madam"
O/P:True
'''
def isPalindrome(s):
    return s==s[::-1]
print(isPalindrome("madam"))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

#optimized solution
def isPalindrome(s):
    n=len(s)
    for i in range(n//2):
        res=s[i]
        if res!=s[n-(i+1)]:
            return False
    return True
print(isPalindrome('madam'))
'''
Time complexity:O(n)
Space Complexity:O(1)'''


#optimized solution using two pointer approach
def isPalindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
print(isPalindrome('madam'))
'''
Time complexity:O(n)
Space Complexity:O(1)'''