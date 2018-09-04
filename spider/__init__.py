import time

a = '1.0.0'
b = a.split('.')
print (b[1])
print(7//5)

number = int(962)
a = int(number)//100%10
b = int(number)//10%10
c = int(number)%10
str_version = str(a) + '.' + str(b) +'.' +str(c)
print(str_version)

t = time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(t)

with open('./dockerfile_rf/test','w+') as file:
    file.write("xxxxx")
    file.close()