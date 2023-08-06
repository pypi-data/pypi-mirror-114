#-------------------------------add-------------------------------------------
def add(*numbers):
    result = sum(numbers)
    if result == 0:
        print("\nThere values are not present in the function so the answer will be : ",0,"\n")
    else:
        print("\nThe sum of your numbers are : ",result,"\n")

#-------------------------------sub----------------------------------------

def sub(number1=0,number2=0):
    result = number1 - number2
    print("\nThe subtraction of",number1,"and",number2,"is : ",result,"\n")
    
#-------------------------------mult----------------------------------------

def mult(number1=0,number2=0):
    result = number1 * number2
    print("\nThe multiplication of",number1,"and",number2,"is : ",result,"\n")
    
#-------------------------------div----------------------------------------

    
def div(number1=0,number2=1):
    result = number1 / number2
    print("\nThe division of",number1,"and",number2,"is : ",result,"\n")
    
#-------------------------------sqr----------------------------------------

    
def sqr(number1=0):
    result = number1 ** 2   
    print("\nThe square of",number1,"is : ",result,"\n")
    
#-------------------------------sqrt----------------------------------------


def sqrt(number1=0):
    result = number1 ** 0.5   
    print("\nThe square root of",number1,"is : ",result,"\n")
    
#-------------------------------cube----------------------------------------


def cube(number1=0):
    result = number1 ** 3   
    print("\nThe cube of",number1,"is : ",result,"\n")
    
#-------------------------------cbrt----------------------------------------


def cbrt(number1=0):
    result = number1 ** 0.3   
    print("\nThe cube root of",number1,"is : ",result,"\n")
