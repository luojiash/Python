# coding: utf8
''' 发现一个感觉很酷的设计模式：访问者模式。
它将对象结构和算法实现分离，能够在不改变对象结构的前提下增加新的操作。
关于是否影响了类的封闭性，还有待研究。
'''
class Wheel:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        visitor.visitWheel(self)

class Engine:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        visitor.visitEngine(self)

class Body:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        visitor.visitBody(self)

class Car:
    def __init__(self):
        self.wheels = [Wheel('wheel1'), Wheel('wheel2'),
                       Wheel('wheel3'), Wheel('wheel4'),]
        self.engine = Engine('car_engine')
        self.body = Body('car_body')
    def accept(self, visitor):
        visitor.visitCar(self)
        self.engine.accept(visitor)
        self.body.accept(visitor)
        for wheel in self.wheels:
            wheel.accept(visitor)

class PrintVisitor:
    def visitWheel(self, wheel):
        print 'visit', wheel.name
    def visitEngine(self, engine):
        print 'visit', engine.name
    def visitBody(self, body):
        print 'visit', body.name
    def visitCar(self, body):
        print 'visit car'

car = Car()
car.accept(PrintVisitor())
        
