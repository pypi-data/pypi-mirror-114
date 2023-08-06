def category(l:list):
    string = ""
    if len(l)==1:
        string = ""
    elif len(l)==2:
        string = " thoudand"
    elif len(l)==3:
        string = " million"
    elif len(l)==4:
        string = " billion"
    elif len(l)==5:
        string = " trillion"
    return string

def words():
    """This function returns a number in words.

    This function takes in no arguements.

    return type: dict() of numbers in words
    """

    nums = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',

            10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17:'seventeen',
            18:'eighteen',19: 'nineteen',

            20: 'twenty',21: 'twenty one', 22: 'twenty two', 23: 'twenty three', 24: 'twenty four',25: 'twenty five',
            26: 'twenty six',27: 'twenty seven', 28: 'twenty eight', 29: 'twenty nine',

            30:'thirty',31: 'thirty one', 32: 'thirty two', 33: 'thirty three',34: 'thirty four', 35: 'thirty five',
            36: 'thirty six',37: 'thirty seven', 38: 'thirty eight', 39: 'thirty nine',

            40:'forty', 41: 'forty one', 42: 'forty two', 43: 'forty three', 44: 'forty four', 45: 'forty five', 46:'forty six',
            47: 'forty seven',48: 'forty eight',49: 'forty nine',

            50: 'fifty',51:'fifty one',52:'fifty two',53:'fifty three',54:'fifty four',55:'fifty five',56: 'fifty six',
            57: 'fifty seven',58: 'fifty eight', 59: 'fifty nine',

            60: 'sixty',61: 'sixty one', 62: 'sixty two', 63: 'sixty three', 64: 'sixty four', 65: 'sixty five', 66:'sixty six',
            67: 'sixty seven', 68: 'sixty eight',69: 'sixty nine',

            70: 'seventy',71: 'seventy one', 72: 'seventy two', 73: 'seventy three',
            74: 'seventy four', 75: 'seventy five',76: 'seventy six', 77: 'seventy seven', 78: 'seventy eight',
            79: 'seventy nine',

            80: 'eighty', 81: 'eighty one', 82: 'eighty two', 83: 'eighty three', 84: 'eighty four', 85: 'eighty five', 86: 'eighty six',
            87: 'eighty seven', 88: 'eighty eight', 89: 'eighty nine',

            90: 'ninety', 91: 'ninety one', 92: 'ninety two', 93: 'ninety three',94: 'ninety four', 95: 'ninety five', 96: 'ninety six',
            97: 'ninety seven', 98: 'ninety eight', 99: 'ninety nine'}


    for i in range(1,10): #loop to include basic numbers 100-900
        for j in range(0,100): #loop to add hundreds like 101-199
            if j!=0:
                nums.update({int(str(i)+'00')+j:nums[i]+' '+'hundred'+' '+nums[j]})
            else:
                nums.update({int(str(i)+'00')+j:nums[i]+' '+'hundred'})
    return nums

def numberInWords(n):
        """
        This function accepts one argument, numberInWords(n).
        Args:
        n: any numeric number.

        return: a string reading the number.
        """
        number_in_words = ''
        floating_points = ''

        #check if input is string and return an error string
        if type(n)==str:
            return 'only numbers are allowed!'

        #return a string if n is beyond 999 trillion
        if n<=-1000000000000000 or n >= 1000000000000000:
            return "figure is too large!"

        #convert n to a string for easy manipulation
        string_number = str(n)
        if string_number.startswith('-'):
            number_in_words += 'negative '
            string_number = string_number[1:]


        #get a string for floating numbers
        try:
            floating_numbers = string_number.split('.')[1]
            floating_points += ' point'
            for i in range(len(floating_numbers)):
                floating_points += ' '+words()[int(floating_numbers[i])]
            string_number = string_number.split('.')[0]
        except:
            pass

        l = []
        if len(string_number)%3==0:
            for i in range(0,len(string_number),3):
                l += [string_number[i:i+3]]
        else:
            l += [string_number[:len(string_number)%3]]
            new_string = string_number[len(string_number)%3:]
            for i in range(0,len(new_string),3):
                l += [new_string[i:i+3]]

        #generate the words approriate for the number
        if len(l)==1 and int(l[0])==0:
            number_in_words += words()[0]
        else:
            for i in range(len(l)):
                space = ' ' if i<len(l)-1 else ''
                if int(l[i])==0:
                    continue
                number_in_words += words()[int(l[i])]+category(l[i:])+space
        return number_in_words+floating_points


if __name__=='__main__':
    print(numberInWords(1))
    print(numberInWords(1889))
    print(numberInWords(-2.3501))
    print(numberInWords(2.3501))
