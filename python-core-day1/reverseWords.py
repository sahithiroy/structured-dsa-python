'''
Docstring for python-core-day1.reverseWords

Reverse words in a sentence
I/P:"Hello World"
O/P:"World Hello"
'''
def reverseWords(s):
    return ' '.join(s.split()[::-1])
print(reverseWords("Hello World"))
'''
Time complexity:O(n)
Space Complexity:O(n)'''

def reverse_words(s):
    words = []
    word = ""

    for ch in s:
        if ch != " ":
            word += ch
        else:
            if word:
                words.append(word)
                word = ""

    if word:
        words.append(word)

    return " ".join(words[::-1])
print(reverse_words("Hello World"))
'''Time complexity:O(n)
Space Complexity:O(n)'''