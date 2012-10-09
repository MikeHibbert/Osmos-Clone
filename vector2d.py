from math import sqrt

VECTOR2D_ZERO_THRESHOLD = 0.001

class Vector2d:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Vector2d = (%s, %s) length = %s" % ( self.x, self.y, self.length() )
        
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self    
        
    def __mul__(self, other):
        self.x *= other.x
        self.y *= other.y
        return self    
        
    def __div__(self, other):
        self.x /= other.x
        self.y /= other.y
        return self  
      
    def scale(self, scale):
        self.x *= scale
        self.y *= scale
        
    def length(self):
        return sqrt((self.x * self.x) + (self.y * self.y))            

    def normalise(self):
        length = self.length()
        if not length == 0:
            self.x = self.x / length
            self.y = self.y / length
        
    def copy(self):
        return Vector2d(self.x, self.y)
    
    def x_is_zero(self):
        retVal = False
        if self.x > -VECTOR2D_ZERO_THRESHOLD and self.x < VECTOR2D_ZERO_THRESHOLD:
            retVal = True
        
        return retVal
    
    def y_is_zero(self):
        retVal = False
        if self.y > -VECTOR2D_ZERO_THRESHOLD and self.y < VECTOR2D_ZERO_THRESHOLD:
            retVal = True
        
        return retVal  
      
    def is_zero(self):
        retVal = False
        if self.x_is_zero() and self.y_is_zero():
            retVal = True
            
        return retVal
        
    