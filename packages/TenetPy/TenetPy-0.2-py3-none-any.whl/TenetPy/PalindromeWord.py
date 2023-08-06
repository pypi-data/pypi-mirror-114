class PalindromeWord:

    def __init__(self, check):
        self.check = check

    def check(word):
        word_reversed = word[::-1]

        if word_reversed == word:
            print("palindrome")
        else:
            print("not palindrome")

    


