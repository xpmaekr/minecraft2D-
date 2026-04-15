import pygame
import cfiles
import lev_load

inventory=None
crafting_table=None
inv_state=False
inv_store=[]
inv_n=0

def init_inventory():
    global inventory,grass,rock,items 
    inventory=cfiles.loadimagesize('D:/history/minecraft2D/inventory.jpg',1468,713)
    crafting_table=cfiles.loadimagesize('D:/history/minecraft2D/crafting table.png',50,50)   
    grass=pygame.image.load('D:/history/minecraft2D/editor/imgs/1 Tiles/Tile_18.png')
    grass=pygame.transform.scale(grass,[lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7])
    
    rock=pygame.image.load('D:/history/minecraft2D/editor/imgs/1 Tiles/Tile_30.png')
    rock=pygame.transform.scale(rock,[lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7])

    for i in range(36):
        inv_store.append({'type':'?', 'count':0})   
    for i in range(36):
        item=Item(i%9,i//9,None,0,pygame.display.get_surface())
        items.append(item)

items=[]
res_cache={}

class Item:
    def __init__(self, xt, yt, name_res, count_res, screen):
        self.xt=xt
        self.yt=yt
        self.name_res=name_res
        self.screen=screen
        self.count_res=count_res
        self.font=pygame.font.Font(None, 24)

    def render(self):
        if self.count_res == 0 or self.name_res is None or self.name_res not in res_cache:
            return
        self.screen.blit(res_cache[self.name_res], [70+self.xt*153, 38+self.yt*120])
        text = self.font.render(str(self.count_res), True, (255, 255, 255))
        self.screen.blit(text, [self.xt + 100, self.yt + 100])
    
    def update(self):
        pass

    def get_hitbox(self):
#        if self.name_res is None or self.name_res not in res_cache:
#            return pygame.Rect(0,0,0,0)  # возращаем пустой хитбокс чтобы не было ошибки
        hitbox = pygame.Rect(70+self.xt*153, 38+self.yt*120,
                            rock.get_width(),
                            rock.get_height())
        return hitbox

def render(screen):
    if inv_state == True:
        screen.blit(inventory, [10, 10])
        screen.blit(crafting_table, [1478, 20])
    
        for i in items:
            i.render()
            i.get_hitbox()

table_box=pygame.Rect(1478,20,
                    50,
                    50)

def add_type(res_type,count):
    for i in items:
        if i.name_res == res_type:
            i.count_res += count
            return
    
    for i in items:
        if i.count_res == 0:
            i.name_res = res_type
            i.count_res += count
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return