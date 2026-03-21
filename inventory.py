import pygame
import random
import cfiles
import animation
import lev_load

inventory=None
inv_state='off'
inv_store=[]
inv_n=0

def init_inventory():
    global inventory, grass, rock, items 
    inventory=cfiles.loadimagesize('D:\history\game\Airbrush-IMAGE-ENHANCER-1772650006987-1772650006987.jpg', 1468, 713)
    
    grass=pygame.image.load('D:/history/game/editor/imgs/1 Tiles/Tile_18.png')
    grass=pygame.transform.scale(grass, [lev_load.tile_sizes*1.7, lev_load.tile_sizes*1.7])
    
    rock=pygame.image.load('D:/history/game/editor/imgs/1 Tiles/Tile_30.png')
    rock=pygame.transform.scale(rock, [lev_load.tile_sizes*1.7, lev_load.tile_sizes*1.7])

    for i in range(36):
        inv_store.append({'type': '?', 'count': 0})   
    for i in range(36):
        item=Item(i%9, i//9, None, 0, pygame.display.get_surface())
        items.append(item)

items = []
res_cache = {}

class Item:
    def __init__(self, xt, yt, name_res, count_res, screen):
        self.xt=xt
        self.yt=yt
        self.name_res=name_res
        self.screen=screen
        self.count_res=count_res
        self.font=pygame.font.Font(None, 24)

    def render(self):
        if self.count_res == 0:
            return

        if self.name_res and self.name_res in res_cache:
            self.screen.blit(res_cache[self.name_res], [70+self.xt*153, 38+self.yt*120])
            
            text = self.font.render(str(self.count_res), True, (255, 255, 255))
            self.screen.blit(text, [self.xt + 100, self.yt + 100])
    
    def update(self):
        pass

def render(screen):
    if inv_state == 'on':
        screen.blit(inventory, [10, 10])
    
    for i in items:
        i.render()

def add_type(res_type):
    for i in items:
        if i.name_res == res_type:
            i.count_res += 1
            return
    
    for i in items:
        if i.count_res == 0:
            i.name_res = res_type
            i.count_res += 1
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return