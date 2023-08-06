def calculate(num1,num2,operating = 'addition',mode = 'int',roundTo = 0):
    # operating has 3 parameter:'int'/'float'/'round'
    # calculate has operating mode,is'addition''add''+'/'subtraction''sub''-'/'multiplication''mul''*'
    if operating == 'addition' or operating == 'add' or operating == '+':
        if mode == 'int':
            return num1 + num2
        elif mode == 'float':
            num1 = float(num1)
            num2 = float(num2)
            return num1 + num2
        elif mode == 'round':
            return round((num1 + num2),int(roundTo))
        else:
            raise TypeError('The error mode')
    elif operating == 'subtraction' or operating == 'sub' or operating == '-':
        if mode == 'int':
            return num1 - num2
        elif mode == 'float':
            num1 = float(num1)
            num2 = float(num2)
            return num1 - num2
        elif mode == 'round':
            return round((num1 - num2),int(roundTo))
        else:
            raise TypeError('The error mode')
    elif operating == 'multiplication' or operating == 'mul' or operating == '*':
        if mode == 'int':
            return num1 * num2
        elif mode == 'float':
            num1 = float(num1)
            num2 = float(num2)
            return num1 * num2
        elif mode == 'round':
            return round((num1 * num2),int(roundTo))
        else:
            raise TypeError('The error mode')
    elif operating == 'division' or operating == 'div' or operating == '/':
        if mode == 'int':
            return num1 / num2
        elif mode == 'float':
            num1 = float(num1)
            num2 = float(num2)
            return num1 / num2
        elif mode == 'round':
            return round((num1 / num2),int(roundTo))
        else:
            raise TypeError('The error mode')
    else:
        raise TypeError('The error operating mode')

def count(List):
    string = ''
    for i in List:
        string = '{}{}'.format(string,i)
    return len(string)

def add_at(num1,num2,idx):
    end_num = str(num1)
    add_num = str(num2)
    end_num_list = [i for i in end_num]
    end_num_list.insert(idx,add_num)
    return int(''.join(end_num_list))

def text_int(text):
    try:
        int(text)
    except:
        return False
    else:
        return True

def copyright():
    print('It is zjy self having')

if __name__ == '__main__':
    print(add_at(123123123123123,0,0))



