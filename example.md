

Here's an example recursive function in Python that checks if a given word is a palindrome:

```
def is_palindrome(word):
    # Base case
    if len(word) == 0 or len(word) == 1:
        return True

    # Recursive case
    if word[0] == word[-1]:
        return is_palindrome(word[1:-1])
    else:
        return False
```

Explanation:

The function takes a word as an input and returns `True` if the word is a palindrome, and `False` otherwise.

The base case is when the length of the word is either 0 or 1. In such cases, we can assume that the word is a palindrome.

In the recursive case, we compare the first and last characters of the word. If they are equal, we remove them from the word and call the same function again with the remaining part of the word. This process continues until we reach the base case.

If at any point the first and last characters don't match, we can safely assume that the word is not a palindrome.

Example usage:

```
>>> is_palindrome("racecar")
True

>>> is_palindrome("hello")
False
```