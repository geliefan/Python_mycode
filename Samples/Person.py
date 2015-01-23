'''
Created on 2014/12/24

@author: Makoto
'''

class Person:
    def __init__(self, name, age):
        print '[Person.__init__]'
        self.name = name
        self.age = age
    def showinfor(self):
        print '[Person.showinfo]'
        print '%s (%d)' % (self.name, self.age)