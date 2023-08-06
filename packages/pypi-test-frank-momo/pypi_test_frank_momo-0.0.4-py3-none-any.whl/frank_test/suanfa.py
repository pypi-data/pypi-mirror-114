import time


class sleeep():
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def sleep(self):
        i = 0
        while True:
            print(str(i)+self.name+str(self.age))
            i += 1 
            time.sleep(2)
a=sleeep("bo", 23)
print(a.sleep())