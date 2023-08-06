import pymunk,pygame
from .baseBodyClasses import BaseDynamicBodyClass as BDBC

class GCircle(BDBC):
    def __init__(self,mass=1,moment=100,position=(50,50),radius=85,offset=(0,0),mslf=None):
        self.mass = mass
        self.moment = moment
        self.position = position
        self.circle = pymunk.Circle(BDBC.body,radius,offset)    
        self.mslf = mslf 
        self.radius = radius
    def draw(self,color=(255,255,255)):
        pygame.draw.circle(self.mslf.screen,color,self.circle.body.position,self.radius)       