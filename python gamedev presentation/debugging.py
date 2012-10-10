#!/usr/bin/env python

class MyClass:
    def __init__(self, something):
        self.something = something
        
    def __repr__(self):
        return "MyClass containing %s with value %s" % (self.something.__class__, self.something)
        
    
if __name__ == "__main__":
    mc = MyClass("Cheese")
    nmc = MyClass(300)
    
    print mc
    print nmc
