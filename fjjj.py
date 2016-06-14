#!/usr/bin/python
import sys

#ABC = []

#ABC[0] = list.append(float(raw_input("Please input C Current Price:")))
#ABC[1] = list.append(float(raw_input("Please input A Current Price:")))
#ABC[2] = list.append(float(raw_input("Please input B Current Price:")))


def get_price():
        
    a = float(raw_input("pls input a:\n"))
    b = float(raw_input("pls input b:\n"))
    c = float(raw_input("pls input c:\n"))

    result = lambda c,a,b:((c * 2 -a) - b) / b

    print result(c,a,b)

def combineMore():

    a = float(raw_input("pls input a:\n"))
    b = float(raw_input("pls input b:\n"))
    c = float(raw_input("pls input c:\n"))
    v = float(raw_input("pls input value:\n"))
    result = lambda a,b,c,v:(v / 2) * ( a + b - c * 2 )
    print result(a,b,c,v)
        

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            sys.exit(' you should input function name"b for b should increase % next day \n or c how much you will get from combine" and then input fund info: c a b current price')
        #abc = get_price(sys.argv[1:])
        elif sys.argv[1] == 'b':
            get_price()
        elif sys.argv[1] == 'c':
            combineMore()            
        
        
        

    finally:
        pass
