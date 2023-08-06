class PalindromeWordInList:

    def __init__(self, check):
        self.check = check

    def check(list):
        palindrome_list=[]
        for word in list:
            word_reversed = word[::-1]
            if word_reversed == word:
                palindrome_list.append(word_reversed)
        
        print("the palindrome words in the list are: "+str(palindrome_list))
