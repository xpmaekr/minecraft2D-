import pygame

class Image_button():
    def __init__(self,position,image,screen):
        self.position=position
        self.image=image
        self.hitbox=pygame.Rect(self.position,self.image.get_size())
        self.slot=None
        self.screen=screen

    def render(self,click):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if click and self.slot!=None:
                self.slot()

        

        self.screen.blit(self.image,self.position)

