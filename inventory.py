import pygame
import cfiles
import lev_load
import player_data

inventory=None
craft_table=None
inv_state=False
inv_store=[]
inv_n=0
items=[]
res_cache={}

tree=pygame.image.load('tree_tex.jpg')
tree=cfiles.loadimagesize('tree_tex.jpg',lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7)   

leaf=pygame.image.load('leaf_tex.png')
leaf=cfiles.loadimagesize('leaf_tex.png',lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7)

craft_table=pygame.image.load('crafting table.png')
craft_table=cfiles.loadimagesize('crafting table.png',lev_load.tile_sizes*1.7,lev_load.tile_sizes*1.7)   

pygame.image.load('down_panel.png')
down_inventory=cfiles.loadimagesize('down_panel.png',598,66)

detailed_block=pygame.image.load("detailed_block.png")
detailed_block=cfiles.loadimagesize('detailed_block.png', 110, 110)

idle=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Idle_4.png',4,3)
gidle=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Idle_4.png',4,3)

def init_inventory():
    global inventory,grass,rock,items,craft_table_big,down_inventory
    craft_table_big=cfiles.loadimagesize('crafting table.png',200,200)   
    inventory=cfiles.loadimagesize('inventory.jpg',1468,713)
    down_inventory=cfiles.loadimagesize('down_panel.png',598,66)
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
        item=Item(i%9,i//9,None,0,pygame.display.get_surface(),i)
        items.append(item)
        
W = 153 # ширина одного слота в инвентаре
H = 153 # высота одного слота в инвентаре

# Константы для нижней панели
down_panel_slot_width = 66  # ширина слота в нижней панели
down_panel_slot_height = 66  # высота слота в нижней панели
down_panel_slots = 9  # количество слотов в нижней панели

selected_slot=1


class Item:
    def __init__(self, xt, yt, name_res, count_res, screen,index):
        self.xt=xt
        self.yt=yt
        self.name_res=name_res
        self.screen=screen
        self.count_res=count_res
        self.font=pygame.font.Font('minecraft_font.ttf', 24)
        self.moving = False
        self.index = index


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
    
    def __repr__(self):
        return(f'count= {self.count_res} name= {self.name_res} index= {self.index}')

def get_down_panel_pos():
    """Возвращает позицию нижней панели"""
    return (player_data.desk_sizes[0]/2-down_inventory.get_width()/2, player_data.desk_sizes[1]-down_inventory.get_height())

def get_down_panel_slot_at_pos(pos):
    #получаем слот по позиции мыши
    if inv_state:  #не работаем с нижней панелью если открыт основной инвентарь
        return None
    
    panel_x, panel_y = get_down_panel_pos()
    
    #проверяем, находится мышь над нижней панелью или нет
    if not (panel_x <= pos[0] <= panel_x + down_inventory.get_width() and 
            panel_y <= pos[1] <= panel_y + down_inventory.get_height()):
        return None
    
    #вычисляем
    slot_x = int((pos[0] - panel_x) / down_panel_slot_width)
    
    if 0 <= slot_x < down_panel_slots:
        return slot_x
    
    return None

def render_down_panel_items(screen):
    #рендер нижней панели
    panel_x, panel_y = get_down_panel_pos()
    
    for i in range(down_panel_slots):
        item = items[27+i]
        if item.count_res == 0 or item.name_res is None or item.name_res not in res_cache:
            continue
        
        slot_x = panel_x + i * down_panel_slot_width + 5
        slot_y = panel_y + 5
        
        if item.moving:
            res_cache[item.name_res].set_alpha(100)
            mpos = pygame.mouse.get_pos()
            res_x = mpos[0] - res_cache[item.name_res].get_width() // 2
            res_y = mpos[1] - res_cache[item.name_res].get_height() // 2
            screen.blit(pygame.transform.scale(res_cache[item.name_res],[56,56],), (res_x, res_y))
            res_cache[item.name_res].set_alpha(255)
            text = item.font.render(str(item.count_res), True, (255, 255, 255))
            screen.blit(text, (res_x + 10, res_y + 30))
        else:
            screen.blit(pygame.transform.scale(res_cache[item.name_res],[56,56],), (slot_x, slot_y))
            text = item.font.render(str(item.count_res), True, (255, 255, 255))
            screen.blit(text, (slot_x + 15, slot_y + 35))

    screen.blit(detailed_block,(panel_x+66*(selected_slot-1)-20,panel_y-21))
    
def render(screen):
    if inv_state == True:
        screen.blit(inventory, [10, 10])
        screen.blit(craft_table_big, [1400, 780])
    
        for i in items:
            i.render()
            i.get_hitbox()
    
    else:
        panel_pos = get_down_panel_pos()
        screen.blit(down_inventory, panel_pos)
        render_down_panel_items(screen)

table_box=pygame.Rect(1478,200,
                    200,
                    200)

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

def add_type(res_type,count):

    for i in items:
        if i.name_res == res_type and i.index>26:
            i.count_res += count
            
            print(1)
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return
        
    for i in items:
        if i.count_res == 0 and i.index>26:
            i.count_res += count
            i.name_res = res_type
            
            print(1)
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return
        

    for i in items:
        if i.name_res == res_type and i.index<=26:
            i.count_res += count
            
            print(1)
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return

    for i in items:
        if i.count_res==0 and i.index<=26:
            i.count_res += count
            i.name_res = res_type    
            
            print(1)
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            return
    
    for i in items:
        if i.count_res == 0:
            i.name_res = res_type
            i.count_res += count
            res_cache[res_type] = globals()[res_type]  #кешируем 1 раз
            
            print(1)
            return