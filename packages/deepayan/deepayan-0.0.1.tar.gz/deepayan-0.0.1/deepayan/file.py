def new(file_name):
    
    f = open(file_name,"a")
    print("Your file"+file_name+"has been created successfully...")
    n = input("Please tell me do you want to write any thing inside you file or not (y/n)")
    
    while n == "Y" or n == "y":
        print("please write below....")
        a = input(">>>")
        n = input("Please tell me do you want to write any thing inside you file or not (y/n)")
        f.write(a)

    if n != "Y" or n != "y":
        print("You are all set....")
    
    f.close()

def write(file_name):

    f=open(file_name,"a")
    n = input("Please tell me do you want to write any thing inside you file or not (y/n)")

    while n == "Y" or n == "y":    
        print("please write below....")
        a = input(">>>")
        n = input("Please tell me do you want to write any thing inside you file or not (y/n)")
        f.write(a)
    
    f.close()
