import random, sys, time, math, pygame
from pygame.locals import *
from Camera import Camera2d
from atom import Atom, ATOM_ENERGY_TRANSFER_RATE
from vector2d import Vector2d

ENEMY_COUNT = 10
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

PLAYER_ACCELERATION = 0.5 # pixels per second
PLAYER_STARTING_MASS = 8.0

class Game:
    def __init__(self):
        # game evironment variables
        self.windowWidth = SCREEN_WIDTH
        self.windowHeight = SCREEN_HEIGHT
        self.running = False
        self.worldWidth = self.windowWidth #* 3
        self.worldHeight = self.windowHeight #* 4
        self.totalEnemyAtomMass = 0
        self.playerWon = False
        self.playerLost = False
        self.musicVolume = 0.5
        

        # movement flags
        self.moveUP = False
        self.moveLEFT = False
        self.moveDOWN = False
        self.moveRIGHT = False
        
        # init the game systems
        self.setup_pygame()
  
        self.setup_camera()
        
        self.setup_atoms()
        
    def setup_pygame(self):      
        pygame.init()
        self.oldTime = self.newTicks = pygame.time.get_ticks()
        
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), 
                                              pygame.DOUBLEBUF|pygame.HWSURFACE)
        
        pygame.display.set_caption('Osmos Clone')
        self.font = pygame.font.Font('freesansbold.ttf', 32)  
        pygame.display.set_icon(pygame.image.load('images/osmos.png'))  
  
        pygame.mixer.music.load('sound/MOONDARK_PROJECT.mp3')
        pygame.mixer.music.play(-1,0.0)
        
    def setup_camera(self):
        self.camera = Camera2d(self.worldWidth/2 - (SCREEN_WIDTH / 2), 
                               self.worldHeight/2 - (SCREEN_HEIGHT / 2),
                               self.screen)        
        
            
    def setup_atoms(self):
        # Load atom images
        self.atomImage = pygame.image.load('images/osmos.png')
        self.enemyImage = pygame.image.load('images/osmos-enemy.png')        

        self.atoms = []; add = self.atoms.append
                
        self.playerAtom = Atom(self.worldWidth/2, 
                               self.worldHeight/2,
                               self.atomImage.get_width() / 4,
                               self.atomImage.get_height() / 4,
                               self.atomImage,
                               True)
         
        add(self.playerAtom)
        self.camera.follow(self.playerAtom)
        
        for x in xrange(ENEMY_COUNT):
            generalSize = random.randint(20, 45)
            multiplier = random.randint(1, 3)     
            
            x = random.randint(1, self.worldWidth)
            y = random.randint(1, self.worldHeight)
            
            width  = (generalSize + random.randint(5, 10)) * multiplier
            height = (generalSize + random.randint(5, 10)) * multiplier  
            
            atom = Atom(x, 
                        y,
                        width,
                        height,
                        self.enemyImage)
            
            self.totalEnemyAtomMass += atom.mass
            
            add(atom)        
            
    def run(self):
        self.running = True
        
        while(self.running):
            self.get_input()
            self.process()
            self.render()
            
        
    def get_input(self):
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                self.running = False       
                
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    self.moveDOWN = False
                    self.moveUP = True
                elif event.key in (K_DOWN, K_s):
                    self.moveUP = False
                    self.moveDOWN = True
                elif event.key in (K_LEFT, K_a):
                    self.moveRIGHT = False
                    self.moveLEFT = True
                elif event.key in (K_RIGHT, K_d):  
                    self.moveLEFT = False
                    self.moveRIGHT = True   
                elif event.key == K_ESCAPE:
                    self.running = False 
                elif event.key == K_r:
                    self.reset_game()
                elif event.key == K_PLUS:
                    self.musicVolume += 0.01
                    if self.musicVolume > 1.0:
                        self.musicVolume = 1.0
                    pygame.mixer.music.set_volume(self.musicVolume)
                elif event.key == K_MINUS:
                    self.musicVolume -= 0.01
                    if self.musicVolume < 0.0:
                        self.musicVolume = 0.0
                    pygame.mixer.music.set_volume(self.musicVolume)                
                    
            elif event.type == KEYUP:
                # stop moving the player
                if event.key in (K_LEFT, K_a):
                    self.moveLEFT = False
                elif event.key in (K_RIGHT, K_d):
                    self.moveRIGHT = False
                elif event.key in (K_UP, K_w):
                    self.moveUP = False
                elif event.key in (K_DOWN, K_s):
                    self.moveDOWN = False            
                    
    def apply_player_direction(self, delta):
        direction = Vector2d(0,0)
        
        if self.moveDOWN:
            direction += Vector2d(0, PLAYER_ACCELERATION)
        if self.moveUP:
            direction += Vector2d(0, -PLAYER_ACCELERATION)        
        if self.moveRIGHT:
            direction += Vector2d(PLAYER_ACCELERATION, 0) 
        if self.moveLEFT:
            direction += Vector2d(-PLAYER_ACCELERATION, 0)  
        
        self.playerAtom.velocity += direction
        
            
    def process(self):
        # get the number of clock ticks since last render
        self.oldTime = self.newTicks
        self.newTicks = pygame.time.get_ticks()
        delta = self.newTicks - self.oldTime
        
        # react to player inputs
        if not self.playerWon:
            if not self.playerLost:
                self.apply_player_direction(delta)
        
        # perform all atoms processes
        largestAtom = None
        smallestAtom = None
        for atom in self.atoms:
            if largestAtom == None:
                largestAtom = atom
                smallestAtom = atom
                
            # process atom behaviours    
            atom.process(delta, self.atoms)
            atom.move(delta)
            
            # find the largest atom to see if the player has won
            if atom.radius > largestAtom.radius:
                largestAtom = atom
                
            # find out if the player is the smallest atom
            if atom.radius < smallestAtom.radius:
                smallestAtom = atom
            
        if largestAtom == self.playerAtom:
            self.playerWon = True
            
        if smallestAtom == self.playerAtom:
            self.playerLost = True        
            
        # update the cameras status
        self.camera.process()
        
    def render(self):
        # draw a black background
        self.screen.fill((0,0,0))
        
        # draw all atoms
        for atom in self.atoms:
            atom.draw(self.camera)
           
        # the player has become the largest atom!
        if self.playerWon:
            self.display_player_won()
            
        # the player has become the largest atom!
        if self.playerLost:
            self.display_player_lost()        
            
        # push the rendered scene to the screen 
        pygame.display.flip()
    
    def display_player_won(self):
        text = self.font.render('OWNASAURUS REX!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.centerx = self.windowWidth / 2
        textRect.centery = self.windowHeight / 2
        
        self.screen.blit(text, textRect)
        
        self.display_reset_message()
        
    def display_player_lost(self):
        text = self.font.render('You Lost!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.centerx = self.windowWidth / 2
        textRect.centery = self.windowHeight / 2
        
        self.screen.blit(text, textRect)   
        
        self.display_reset_message()
            
    def display_reset_message(self):
        text = self.font.render("Press 'r' to reset.", True, (255,255,255))
        textRect = text.get_rect()
        textRect.centerx = self.windowWidth / 2
        textRect.centery = (self.windowHeight / 2) + 40
        
        self.screen.blit(text, textRect)          

    def reset_game(self):
        for atom in self.atoms:
            x = random.randint(1, self.worldWidth)
            y = random.randint(1, self.worldHeight)            
            mass = random.randint(1, 20)
            
            atom.reset_with_values(x, y, mass)
            
        self.camera.x = self.windowWidth / 2
        self.camera.y = self.windowHeight / 2
        
        self.playerAtom.reset_with_values(self.camera.x, 
                                           self.camera.y,
                                           PLAYER_STARTING_MASS)
        self.playerWon = False
        self.playerLost = False
            
            
