class ReverserList:

    def __init__(self, reverse):
        self.reverse = reverse

    def reverse(list):
        reversed_list = []
        for word in list:
            word_reversed = word[::-1]
            reversed_list.append(word_reversed)
        print(reversed_list)