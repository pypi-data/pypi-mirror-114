#Hello
import os,operating,sys

class init():
    @classmethod
    def reload(cls):
        sys.path.append(os.path.dirname(operating.__file__))
        f = open('.cfg','w')
        f.close()
    @classmethod
    def cache(cls,num):
        sys.path.append(os.path.dirname(operating.__file__))
        f = open('.cfg','a')
        f.write(str(num))
        f.close()
    @classmethod
    def __init__(cls):
        print('Welcome to use intting')
        init.reload()

if __name__ == '__main__':
    init.reload()
