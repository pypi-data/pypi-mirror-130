import pymunk

class BaseDynamicBodyClass():
    def __init__(self):    
        self.body = pymunk.Body(self.mass,self.moment,pymunk.Body.DYNAMIC)
        self.body.position = self.position