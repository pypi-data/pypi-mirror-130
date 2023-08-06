import pygame as pg

class HealthBar():
    def __init__(self,mslf,position=(10,10),maxlenght=400,height=25,color=(255,0,0),max_health=1000,current_health=200,outer_rect_color="white",border_width=4):
        self.screen = mslf.screen
        self.ch = current_health
        self.mh = max_health
        self.mhbl = maxlenght
        self.height = height
        self.pos = position
        self.color = color
        self.orc = outer_rect_color
        self.bdwidth = border_width
        self.hr = self.mh / self.mhbl
    def draw(self):
        pg.draw.rect(self.screen,self.color,(*self.pos,self.ch/self.hr,self.height))
        pg.draw.rect(self.screen,self.orc,(*self.pos,self.mhbl,self.height),self.bdwidth)
    def setCurrentHealth(self, health):
        self.ch = health
    def drainHealthBy(self,by):
        if self.ch>0:
            self.ch-=by
        if self.ch<=0:
            self.ch=0
    def regenerateHealthBy(self,by):
        if self.ch<self.mh:    
            self.ch+=by
        if self.ch>=self.mh:
            self.ch=self.mh
    def regenerateHealth(self):
        self.ch = self.max_health
    def setMaxHealth(self,health):
        self.mh = health
    def get_health(self):
        return self.ch
    def get_damaged(self):
        return self.mh-self.ch