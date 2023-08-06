#This function packge will give you a better uses
def count(num):
    string = str(num)
    List = [i for i in string]
    return List.count()

def number_base_conversion_ten_to_other(number,conversion = 2):
    a=['0','1','2','3','4','5','6','7','8','9','A','b','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    b=[]
    while True:
        s = number // conversion
        y = number % conversion
        b.append(a[y])
        if s==0:
            break
        number = s
    b.reverse()
    returns = ''
    for i in b:
        returns = returns + i
    return returns

def number_base_conversion_other_to_ten(number,conversion = 2):
    return int(number,conversion)

def number_base_conversion(number,firstconversion = 10,lastconversion = 10):
    number = int(number,firstconversion)
    a=['0','1','2','3','4','5','6','7','8','9','A','b','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    b=[]
    while True:
        s = number // lastconversion
        y = number % lastconversion
        b.append(a[y])
        if s==0:
            break
        number = s
    b.reverse()
    returns = ''
    for i in b:
        returns = returns + i
    return returns

def regroup(*numberList):
    numbers = [str(i) for i in numberList]
    number = ''
    for i in numbers:
        number = '{}{}'.format(number,i)
    returns = int(number)
    return returns

if __name__ == '__main__':
    pass