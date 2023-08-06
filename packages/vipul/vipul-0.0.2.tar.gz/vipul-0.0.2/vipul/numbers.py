def reversedigit():
    a = int(input("Enter The Number You Want To Reverse => "))  
    reversed_number = 0
    while (a > 0):  
        remainder = a % 10  
        reversed_number = (reversed_number * 10) + remainder  
        a = a // 10
    print("The Reversed Number is : {}".format(reversed_number))

def pronicnum():
    a = int(input("Enter The number => "))
    f = 0
    for i in range(a):
        if i * (i + 1) == a:
            f = 1
            break
    if f==1:
        print("The Number Is Pronic")
    else:
        print("The Number Is Not Pronic")

def infinitenum():
    x = 0
    while True:
        print (x)
        x+=1

def numbercheck():
    a=int(input("Enter the number you want to check ->"))
    if a>0:
        print("Number Is Positive")
    elif a==0:
        print("Zero")
    else:
        print("Number Is Negative")

def fibonacci():
    a = int(input("Enter The Level Upto Which You Want To Get The Fobonacci Series => "))
    b = 0
    c = 1
    d = 0
    print(b)
    print(c)
    for i in range(1 , a+1):
        d= b+c
        print(d)
        b = c
        c = d

def factorial():
    a = int(input("Enter The Number => "))
    b = 1
    for i in range(1 , a+1):
        b = b*i
    print(f"The Factorial Of {a} is :", b)

def buzznumber():
    a = int(input("Enter The Number Which You Want To Check => "))
    if a % 10 == 7 or a % 7 == 0:
        print("The Number Is a Buzz Number")
    else:
        print("The Number Is Not a Buzz Number")

def biggeroftwonum():
    a = input("Enter The First Number => ")
    b = input("Enter The Second Number => ")
    if a>b:
        print(a, "Is Greater Than", b)
    else:
        print(b, "Is Greater Than", a)

def passdigitverif4():
    a = int(input("Enter The Password => "))
    ab = str(a)
    if len(ab)==4:
        print("You have Entered a 4 Digit Password :", a)
        print("Access Granted")
    else:
        print("You have Entered a Password More Than 4 Digits :", a)
        print("Access Denied")

def swapthenums():
    a=int(input("Enter the first number :-"))
    b=int(input("Enter the second number :-"))
    print("The original value of a is :-" , a)
    print("The original value of b is :-" , b)
    a,b=b,a
    print("The swapped value of a is :-" , a)
    print("The swapped value of b is :-" , b)

def divisible2():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 2 == 0:
        print(f"The Number {a} is Divisible By 2")
    else:
        print(f"The Number {a} is Not Divisible By 2")

def divisible3():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 3 == 0:
        print(f"The Number {a} is Divisible By 3")
    else:
        print(f"The Number {a} is Not Divisible By 3")

def divisible5():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 5 == 0:
        print(f"The Number {a} is Divisible By 5")
    else:
        print(f"The Number {a} is Not Divisible By 5")

def divisible7():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 7 == 0:
        print(f"The Number {a} is Divisible By 7")
    else:
        print(f"The Number {a} is Not Divisible By 7")

def divisible11():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 11 == 0:
        print(f"The Number {a} is Divisible By 11")
    else:
        print(f"The Number {a} is Not Divisible By 11")

def divisible13():
    a = int(input("Enter The Number You Want To Check => "))
    if a % 13 == 0:
        print(f"The Number {a} is Divisible By 13")
    else:
        print(f"The Number {a} is Not Divisible By 13")

def palindrome():
    a = input("Enter The Number or Word To Check Whether It Is A Palindrome Number => ")
    palin = a[::-1]
    if palin == a:
        print("Yes, It Is a Palindrome Number")
    else:
        print("No, It Is Not a Palindrome Number")

def armstrong():
    a = int(input("Enter The Number You Want To Check => "))
    b = 0
    abc = a
    while abc > 0:
        abcd = abc % 10
        b += abcd**3
        abc //=10
    if a==b:
        print("Yes, It Is A Armstrong Number")
    else:
        print("No, It Is Not A Armstrong Number")

def leapyear():
    a = int(input("Enter The Year You Want To Check => "))
    if a % 400 == 0 or a % 4 == 0:
        print(f"The Year {a} Is A Leap Year")
    elif a % 100 == 0:
        print(f"The Year {a} Is Not A Leap Year")
    else:
        print(f"The Year {a} Is Not A Leap Year")

def primenum():
    a = int(input("Enter The Number You Want To Check => "))
    for i in range(2,a):
        if a % i == 0:
            print(f"The Number {a} Is Not a Prime Number")
            break
        else:
            print(f"The Number {a} Is a Prime Number")
            break

def primenumrange():
    a = int(input("Enter The Level Upto Which You Want To Print The Prime Number => "))
    for num in range(2,a+1):
        if num > 1:
            for i in range(2,num):
                if (num % i) == 0:
                    break
            else:
                print(num)

def reverse():
    a = input("Enter The Details You Want In The List, Just Enclose Everything and Put ',' comma between the items like :- [Hello,1,2,Bye] => ")
    print(a[::-1])

# if __name__ =="__main__":
#     reverse()