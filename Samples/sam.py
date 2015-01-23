'''
Created on 2014/12/24

@author: Makoto
'''
from Person import Person

p1 = Person("Ichiro Suzuki", 37)
p2 = Person("Hanako Yamada", 35)

p1.showinfor()
p2.showinfor()

class Employee(Person):
    def __init__(self, name, age, company):
        print 'Emplogyee.__init__]'
        Person.__init__(self, name, age)
        self.company = company
    def showinfor(self):
        Person.showinfor(self)