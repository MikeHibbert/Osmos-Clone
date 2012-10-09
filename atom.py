from vector2d import Vector2d
import random, sys, time, math, pygame
from pygame.locals import *


ATOM_ENERGY_TRANSFER_RATE = 0.5
ATOM_MASS_PER_PER_PIXEL = 0.3
ATOM_MASS_ABSORBTION_RATE = 4.0
FRICTION = 0.001
ATTRACTION_THRESHOLD = 5000
ATTRACTION_ACCELERATION = 0.001
ATOM_MAX_SPEED = 30.0
ATOM_RADIUS_THRESHOLD = 4.0

ATOM_DEBUG = False

class Atom:
    def __init__(self, x, y, width, hieght, image, isPlayer=False):
        self.position = Vector2d(x, y)
        self.sprite = image
        self.velocity = Vector2d(0, 0)
        self.isPlayer = isPlayer
        self.width = width
        self.height = hieght
        self.radius = width / 2
        self.mass = self.radius * ATOM_MASS_PER_PER_PIXEL
        self.isVisible = True
        self.font = pygame.font.Font('freesansbold.ttf', 10) 
        self.colliding = False
        
    def __repr__(self):
        return "Atom radius:%s mass:%s velocity: %s" % (self.radius, self.mass, self.velocity.length())
    
    def move(self, delta):        
        # cap the velocity
        if self.velocity.length() > ATOM_MAX_SPEED:
            self.velocity.normalise()
            self.velocity.scale(ATOM_MAX_SPEED)
            
        velocity = self.velocity.copy()
        scale = (velocity.length() / 1000.0) * float(delta)
        velocity.normalise()
        velocity.scale(scale)
        
        self.position += velocity

        
    
    def draw(self, camera):
        if self.isVisible:
            rect = pygame.Rect(self.position.x - camera.x - (self.radius * 2),
                               self.position.y - camera.y - (self.radius * 2),
                               int(self.radius * 2),
                               int(self.radius * 2) )
            
            currentImage = pygame.transform.scale( self.sprite, ( int(self.radius * 2), int(self.radius * 2) ) )
            
            camera.screen.blit(currentImage, rect)
            
            if ATOM_DEBUG:
                pygame.draw.circle(camera.screen, (255, 255, 0), 
                                   (int(self.position.x - camera.x - self.radius), 
                                    int(self.position.y - camera.y - self.radius)),
                                   int(self.radius), 3)
                                   
                
                text = self.font.render(self.__repr__(), True, (255,255,255), (20,20,20))
                textRect = text.get_rect()
                textRect.centerx = self.position.x
                textRect.centery = self.position.y
                
                camera.screen.blit(text, textRect)
        
    def is_larger_than(self, other):
        retVal = False
        if self.radius > other.radius:
            retVal = True
            
        return retVal
    
    def is_attracted_to(self, other):
        retVal = None
        
        if self.isVisible and other.isVisible:
            toVector = self.position - other.position
            
            if toVector.length() < ATTRACTION_THRESHOLD:
                toVector.normalise()
                toVector.scale(ATTRACTION_ACCELERATION)
                retVal = toVector
            
            
        return retVal
            
    def collides_with(self, entity):
        retVal = False
        if self.isVisible and entity.isVisible:
            myPosition = Vector2d( self.position.x - self.radius, 
                                   self.position.y - self.radius)
            entityPosition = Vector2d( entity.position.x - entity.radius, 
                                           entity.position.y - entity.radius)   
            
            totalRadiuses = self.radius + entity.radius
            distance = myPosition - entityPosition
            
            if distance.length() < totalRadiuses:
                retVal = True
                self.colliding = True
            
        return retVal
        
    def process(self, delta, entities):
        # perform AI and responses to happenings
        for entity in entities:
            #if not self.isPlayer: # if its not the player controlled atom
                #if entity.isVisible: # and its not dead
                    #if not entity == self: # and its not the current atom we are processing for
                        #acceleration = self.is_attracted_to(entity) # see if we're attracted to this atom
                        #if not acceleration == None: # if we have to accelerate to the atom
                            #velocity = self.velocity.copy()
                            #velocity += acceleration 
                            #if velocity > ATOM_MAX_SPEED:
                                #velocity.normalise()
                                #velocity.scale( ATOM_MAX_SPEED )
                                
                            #self.velocity = velocity # add to the current velocity
                            
            # collision responses                
            if not entity == self:
                if self.isVisible and entity.isVisible:
                    if self.collides_with(entity): #did we come into contact?
                        # yes we did
                        if self.is_larger_than(entity): # is it larger than us?
                            # nope! so lets drain it of some mass and make us bigger
                            entity.lessen_mass(delta) 
                            self.increase_mass(delta)
                        else:
                            # Yep! so let it drain us of some mass and make itself bigger
                            self.lessen_mass(delta)
                            entity.increase_mass(delta)                    
                        
        if self.radius <= ATOM_RADIUS_THRESHOLD:
            self.isVisible = False  
            self.velocity.x = 0.0
            self.velocity.y = 0.0
        
        
    def lessen_mass(self, delta):
        amount = (ATOM_MASS_ABSORBTION_RATE / 1000.0) * float(delta)
        self.mass -= amount
        if self.mass > 0:
            self.set_radius_with_new_mass()
    
    def increase_mass(self, delta):
        amount = (ATOM_MASS_ABSORBTION_RATE / 1000.0) * float(delta)
        self.mass += amount
        self.set_radius_with_new_mass()
    
    def set_radius_with_new_mass(self):
        self.radius = self.mass / ATOM_MASS_PER_PER_PIXEL
                 
    def reset_with_values(self, x, y, mass):
        self.position.x = x
        self.position.y = y
        self.mass = mass
        self.set_radius_with_new_mass()
        
        self.velocity.x = 0.0
        self.velocity.y = 0.0
        
        self.isVisible = True