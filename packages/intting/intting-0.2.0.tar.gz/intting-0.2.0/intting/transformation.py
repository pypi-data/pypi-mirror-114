#here can to help you made other data type
def to_str(num):
    num = float(num)
    return str(num)

def to_list(*num):
    number = []
    for i in num:
        i = float(i)
        number.append(str(i))
    return [i for i in number]

def to_dictionary(*num):
    dic = {}
    number = [i for i in num]
    for i in range(len(number)):
        key,num = number[i]
        dic[key] = num
    return dic

def back_int(string):
    try:
        return int(string)
    except:
        raise TypeError("The data type can't int")

if __name__ == '__main__':
    print(to_dictionary(('我是帅逼',6666666666666),('我是傻逼',38)))
    print(to_str(123.123))
    print(to_list(1,1,1,1,1))