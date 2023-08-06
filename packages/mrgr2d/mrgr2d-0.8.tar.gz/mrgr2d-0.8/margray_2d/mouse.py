import pygame.mouse as pm

class Mouse():
    def __init__(self):
        pass
    def get_pos(self):
        return pm.get_pos()
    def hide(self):
        pm.set_visible(False)
    def unhide(self):
        pm.set_visible(True)
    def isHidden(self):
        return pm.get_visible()