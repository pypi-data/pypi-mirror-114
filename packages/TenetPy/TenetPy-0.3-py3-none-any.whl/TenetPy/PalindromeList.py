class PalindromeList:

    def __init__(self, check):
        self.check = check

    def check(list):
        reversed_list=[]
        for word in list:
            word_reversed = word[::-1]
            reversed_list.append(word_reversed)

        if reversed_list == list:
            print("palindrome")
        else:
            print("not all palindrome")