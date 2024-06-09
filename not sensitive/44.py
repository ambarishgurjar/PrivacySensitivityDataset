

import string

class Solution(object):
    def cellsInRange(self, s):

        alphabet = list(string.ascii_uppercase)
        num1 = s[1]
        num2 = s[4]
        letter1 = s[0]
        letter2 = s[3]
        output = []
        letter = alphabet.index(letter1)
        number = num1

        for i in range((alphabet.index(letter2)-alphabet.index(letter1))+1):
            number = int(num1)
            for j in range(int(num2) - int(num1) + 1):
                output.append(str(alphabet[letter])+(str(number)))
                number = number + 1
            letter = letter + 1


        return output
        
