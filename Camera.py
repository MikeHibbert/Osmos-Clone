from vector2d import Vector2d

class Camera2d(Vector2d):
    def __init__(self, x, y, screen):
        Vector2d.__init__(self, x, y)
        self.screen = screen
        self.screenHalfWidth = screen.get_width() / 2
        self.screenHalfHeight = screen.get_height() / 2
        self.entity = None
        
    def follow(self, entity):
        self.entity = entity
        
    def process(self):
        if self.entity:
            self.x = self.entity.position.x - self.screenHalfWidth
            self.y = self.entity.position.y - self.screenHalfHeight