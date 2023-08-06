from time import localtime

def refresh_time():
    def timewords(*args):
        return localtime().tm_hour,localtime().tm_min
#create a localtime object t
def timeInWords(h=None,m=None):
    '''
    This function returns system time in words if the user does not specify the inputs.

    arguments:
    h(int): hour
    m(int): minute

    Return type(str) eg timeInWords(12,1) is one minute past twelve.
    '''
    if h==None and m == None:
        h = localtime().tm_hour
        m = localtime().tm_min

    string = ''

    hours = {0: 'twelve', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
            10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen',
            18: 'eighteen', 19: 'nineteen', 20: 'twenty', 21: 'twenty one', 22: 'twenty two', 23: 'twenty three'}
    minutes = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
            10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'quarter', 16: 'sixteen', 17: 'seventeen',
            18: 'eighteen', 19: 'nineteen', 20: 'twenty', 21: 'twenty one', 22: 'twenty two', 23: 'twenty three',24:'twenty four',
            25:'twenty five',26:'twenty six',27:'twenty seven',28:'twenty eight',29:'twenty nine'}


    am_pm = ""
    if 0<=h<=11 or ((h+1)>23 and m>30):
        am_pm = "AM"
    else:
        am_pm = "PM"

    if m==0:
        string = "{} o'clock".format(hours[h])
    elif m==1 or 60-m==1:
        string = "{} minute past {}".format(minutes[m],hours[h%12]).capitalize() if m==1 else "{} minute to {}".format(minutes[60-m],hours[(h+1)%12])
    elif 1<m<30:
        if m==15:
            string =  "quarter past {}".format(hours[h%12])
        else:
            string = "{} minutes past {}".format(minutes[m],hours[h%12])
    elif m==30:
        string = "half past {}".format(hours[h%12])
    elif 30<m<=59:
        if h+1 > 23:
            hours[h+1]=hours[0]
        if m==45:
            string = "{} to {}".format(minutes[60-m],hours[(h+1)%12])
        else:
            string = "{} minutes to {}".format(minutes[60-m],hours[(h+1)%12])
    else:
        string =  "This time is not yet configured in your system!"
    #timeInWords(h=localtime().tm_hour,m=localtime().tm_min)
    return string

if __name__=='__main__':
    print(timeInWords())
