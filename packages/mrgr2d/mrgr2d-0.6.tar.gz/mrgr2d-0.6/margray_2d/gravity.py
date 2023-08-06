import pymunk

class Gravity():
    STATICBODY = pymunk.Body.STATIC
    DYNAMICBODY = pymunk.Body.DYNAMIC
    def __init__(self,gravity=(0,500)):
        self.space = pymunk.Space()
        self.space.gravity = gravity
    def add(self,gravitySprite):
        self.space.add(gravitySprite.body)    
    def update(self,frameRate=1/50):
        self.space.step(frameRate)    