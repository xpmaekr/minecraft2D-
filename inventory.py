import pygame
import cfiles
import lev_load

inventory=None
inv_state=False
inv_store=[]
inv_n=0
items=[]
res_cache={}

def init_inventory():
    global inventory, grass, rock
    inventory=cfiles.loadimagesize('inventory.jpg',1468,713)
    inv_store.clear()
    items.clear()
    res_cache.clear()
    
    grass=pygame.image.load('editor/imgs/1 Tiles/Tile_18.png')
    grass=pygame.transform.scale(grass,[lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7])
    
    rock=pygame.image.load('editor/imgs/1 Tiles/Tile_30.png')
    rock=pygame.transform.scale(rock,[lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7])

    for i in range(36):
        inv_store.append({'type':'?', 'count':0})   
    for i in range(36):
        item=Item(i%9,i//9,None,0,pygame.display.get_surface())
        items.append(item)
W = 153 # ширина одного слота в инвентаре
H = 153 # высота одного слота в инвентаре
class Item:
    def __init__(self, xt, yt, name_res, count_res, screen):
        self.xt=xt
        self.yt=yt
        self.name_res=name_res
        self.screen=screen
        self.count_res=count_res
        self.font=pygame.font.Font(None, 24)
        self.moving = False


    def render(self):
        if self.count_res == 0 or self.name_res is None or self.name_res not in res_cache:
            return
        if self.moving:
            res_cache[self.name_res].set_alpha(100)
            mpos = pygame.mouse.get_pos()
            res_x = mpos[0] - res_cache[self.name_res].get_width() // 2
            res_y = mpos[1] - res_cache[self.name_res].get_height() // 2
            self.screen.blit(res_cache[self.name_res], (res_x, res_y))
            res_cache[self.name_res].set_alpha(255)
            text = self.font.render(str(self.count_res), True, (255, 255, 255))
            self.screen.blit(text, (res_x + 30, res_y + 62))
        else:    
            self.screen.blit(res_cache[self.name_res], self._get_pos())
            text = self.font.render(str(self.count_res), True, (255, 255, 255))
            self.screen.blit(text, [self.xt * W + 100, self.yt * H + 100])
    
    def _get_pos(self):
        if self.yt < 3:
            return 70+self.xt*W, 38+self.yt*H
        else:
            return 70+self.xt*W, 38+self.yt*H + 33

    def update(self):
        pass

    def clear(self):
        self.name_res=None
        self.count_res=0

    def set_resource(self, name_res, count_res):
        self.name_res=name_res
        self.count_res=count_res

    def get_hitbox(self):
#        if self.name_res is None or self.name_res not in res_cache:
#            return pygame.Rect(0,0,0,0)  # возращаем пустой хитбокс чтобы не было ошибки
        hitbox = pygame.Rect(70+self.xt*W, 38+self.yt*H,
                            rock.get_width(),
                            rock.get_height())
        return hitbox
    
def render(screen):
    if inv_state == True:
        screen.blit(inventory, [10, 10])
    
        for i in items:
            i.render()
            i.get_hitbox()

def get_item_at_pos(pos):
    for item in items:
        if item.get_hitbox().collidepoint(pos):
            return item
    return None

def move_item(source_item, target_item):
    if source_item is None or target_item is None:
        return False
    if source_item == target_item:
        return False
    if source_item.count_res <= 0 or source_item.name_res is None:
        return False
    if target_item.count_res != 0:
        return False

    target_item.set_resource(source_item.name_res, source_item.count_res)
    source_item.clear()
    return True

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
