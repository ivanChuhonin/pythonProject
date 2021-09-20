# Задача №1 вычислить сумму двух заданных чисел
def summ():
    a = int(input('Введите целое число : '))
    b = int(input('Введите ещё одно целое число : '))
    print(a+b)


# Задача №2 требуется вычислить a+b^2
def doublesumm():
    a = int(input('Введите целое число : '))
    b = int(input('Введите ещё одно целое число : '))
    print(a+b**2)


# Задача №3 пользуясь файлами, решить задачу a+b
def filesumm():
    f = open('input3.txt', 'r')
    line = f.readline()
    a,b = [int (x) for x in line.split()]
    f.close()
    f = open('output3.txt', 'w')
    f.write(str (a+b))
    f.close()


# Задача №4 пользуясь файлами, решить задачу a+b^2
def filedoublesumm():
    f = open('input4.txt', 'r')
    line = f.readline()
    a,b = [int (x) for x in line.split()]
    f.close()
    f = open('output4.txt', 'w')
    f.write(str (a+b**2))
    f.close()


# функция к заданию 2 вычисляет число Фиббоначи n
def Fibo(n):
    if n<0:
        return -1
    if n>45:
        return -1
    if n==0:
        return 0
    if n==1 or n==2:
        return 1
    firstf = 1
    secondf = 1
    for i in range(n-2):
        firstf,secondf = secondf, firstf+secondf
    return secondf
# Задание 2 пользуясь файлами, находит число Фиббоначи n
def Fib():
    f = open("input2.txt")
    a = int(f.readline())
    f.close()
    f = open("output2.txt","w")
    f.write(str(Fibo(a)))
    f.close()


# функция к заданию 2.2 определение последней цифры числа Фибоначчи
def Fibocheck(n):
    f=Fibo(n)
    return f%10
# Задание 2.2 пользуясь файлами, определение последней цифры числа Фибоначчи
def Fib2():
    f = open("input.txt")
    a = int(f.readline())
    f.close()
    f = open("output.txt","w")
    f.write(str(Fibocheck(a)))
    f.close()


import time
t_start = time.perf_counter()
#summ()
doublesumm()
#filesumm()
#filedoublesumm()
#Fib()
#Fib2()
print("Время работы: %s секунд " % (time.perf_counter() - t_start))