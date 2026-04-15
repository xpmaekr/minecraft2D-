import pygame
import time
import random
import cfiles
import animation
import lev_load
import inventory

pygame.init()
screen=pygame.display.set_mode([0,0],pygame.FULLSCREEN)
lev_load.load()
inventory.init_inventory()

clock=pygame.time.Clock()

# кеш для стадий разрушения
block_stages_cache={}
block_stage1=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 1.png',80,80)
block_stage2=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 2.png',80,80)
block_stage3=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 3 .png',80,80)
block_stage4=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 4.png',80,80)

block_stages_cache[20]=block_stage4
block_stages_cache[40]=block_stage3
block_stages_cache[60]=block_stage2
block_stages_cache[80]=block_stage1

idle=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Idle_4.png', 4, 3)
walk=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Walk_6.png', 6, 3)
run=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_run_6.png', 6, 3)
jump=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Jump_8.png', 8, 3)
onground=True

background=cfiles.loadimagesize('background.jpg', screen.get_width(), screen.get_height())

gidle=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Idle_4.png',4,3)
gwalk=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Walk_6.png',6,3)
grun=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Run_6.png',6,3)
gjump=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Jump_8.png',8,3)
pix=cfiles.getcutpic('pixare.png',1,0.1)

# все сразу
tile_sizes=80
gravity=0.5
groundy=20
damage=20
screen_width=screen.get_width()
screen_height=screen.get_height()
drag_item=None

# оптимизация(берем не все блоки, а только рядом)
def get_colliding_blocks(player_rect):
    global camerax, cameray
    
    min_x=int((player_rect.left)//tile_sizes-2)
    max_x=int((player_rect.right)//tile_sizes+2)

    # ставим границу для блоков рядом(их обозначения)
    # -2 и +2 это буфер на всякий
    # -camerax это для преобразования в др координаты(блочные)

    min_y=int((player_rect.top)//tile_sizes-2)
    max_y=int((player_rect.bottom)//tile_sizes+2)
    
    colliding=[]
    # проверка на наличие блока
    for x in range(min_x,max_x+1):  
        for y in range(min_y,max_y+1):
            if (x,y) in lev_load.blocks:
                colliding.append((x,y))
    return colliding

# оптиизация(рисуем ток поврежденные блоки)
def render_damaged_blocks(screen, camerax, cameray):
    for i in lev_load.blocks.values():
        if 0<i['hp']<100:
            if i['hp'] in block_stages_cache:
                screen.blit(block_stages_cache[i['hp']], 
                           [i['x']*tile_sizes-camerax, i['y']*tile_sizes-cameray])

# проверяем видно ли врага
def is_enemy_visible(enemy,player):
    distance=abs(enemy.x-player.x) #abs чтоб минус убрать(типо если enemy x будет меньше player.x)
    return distance<screen_width

enemies=[]
camerax=cameray=0

class Ghost:
    def __init__(self, x, y, speed):
        self.vy=0
        self.x=x
        self.y=y
        self.speed=speed
        self.state_flip='right'
        self.state='idle'
        self.walktimer=0
        self.randomwalk=0
        self.ka=self.kd=False
        self.animations={
            'idle': animation.Animation(gidle, 8),
            'walk': animation.Animation(gwalk, 8),
            'run': animation.Animation(grun, 8),
            'jump': animation.Animation(gjump, 8)
        }

    def ai(self):
        rwt=random.randint(450, 1000)
        if self.walktimer>rwt-1:
            self.walktimer=0
            if self.state=='idle':
                self.state='walk'
                kaorkd=random.randint(0, 1)
                if kaorkd==1:
                    self.ka=True
                else:
                    self.kd=True
            else:
                self.state='idle'
                self.ka=self.kd=False

        self.walktimer+=1

    def render(self):
        self.animations[self.state].render(screen, self.x-camerax, self.y, self.state_flip)        

    def update(self):
        global onground
        self.vy+=gravity
        self.y+=self.vy
        if self.y>groundy-gidle[0].get_height():
            self.y=groundy-gidle[0].get_height()
            self.vy=0

        if self.ka==True:
            self.state_flip='left'
            self.x-=1
        if self.kd==True:
            self.state_flip='right'
            self.x+=1

        self.animations[self.state].update()

class Player:
    def __init__(self,x,y,speed):
        self.vy=0
        self.x=x
        self.y=y
        self.speed=speed
        self.state_flip='right'
        self.state='idle'
        self.ka=False
        self.kd=False

        self.ntimer_run=0
        self.jump_index=0
        self.timer_jump=0
        self.animations={
            'idle': animation.Animation(idle, 8),
            'walk': animation.Animation(walk, 8),
            'run': animation.Animation(run, 8),
            'jump': animation.Animation(jump, 8)
        }

    def render(self):
        self.animations[self.state].render(screen, self.x-camerax, self.y-cameray, self.state_flip)

    def update(self):
        global onground
        self.vy+=gravity
        self.y+=self.vy
        self.collisiony()

        if self.ka:
            self.state_flip='left'
            self.x-=self.speed
        if self.kd:
            self.state_flip='right'
            self.x+=self.speed
        self.collisionx()

        self.ntimer_run+=1

        if onground==False:          
            if self.state!='jump':
                self.jump_index=0
                self.timer_jump=0
            self.state='jump'

        elif self.ka==True and self.kd==True:
            self.state='idle'
            self.ntimer_run=0          
        elif self.ka==True or self.kd==True:
            self.state='walk'
            if self.ntimer_run>=40:
                self.state='run'
        else:
            self.state='idle'
            self.ntimer_run=0
            
        self.animations[self.state].update()
    
    def collisionx(self):
        nowanim=self.animations[self.state]
        size=nowanim.get_size()
        htplayer=pygame.Rect([self.x,self.y],size)
        htplayer=htplayer.inflate(-30,0)

        for block_coords in get_colliding_blocks(htplayer):
            x=block_coords[0]*tile_sizes
            y=block_coords[1]*tile_sizes
            tilehit=pygame.Rect(x, y, tile_sizes, tile_sizes)

            if tilehit.colliderect(htplayer):
                if self.ka:
                    htplayer.left=tilehit.right
                else:
                    htplayer.right=tilehit.left

        self.x=htplayer.x-15

    def collisiony(self):
        nowanim=self.animations[self.state]
        size=nowanim.get_size()
        global onground
        #onground=False  #сброс
        
        htplayer=pygame.Rect([self.x,self.y],size)
        htplayer=htplayer.inflate(-30,0)      
         
        for block_coords in get_colliding_blocks(pygame.Rect([self.x,self.y],size).inflate(-30,0)):
            #block_coords это x и y в координатах сетки
            x_pixel=block_coords[0]*tile_sizes
            y_pixel=block_coords[1]*tile_sizes
            tilehit=pygame.Rect(x_pixel, y_pixel, tile_sizes, tile_sizes)

            
            
            if tilehit.colliderect(htplayer):
                if self.vy>0:  #падаем
                    onground=True
                    htplayer.bottom=tilehit.top
                    self.vy=0
                    self.y=htplayer.y
                elif self.vy<0:  #прыгаем
                    htplayer.top=tilehit.bottom
                    self.vy=0
                    self.y=htplayer.y
                    
        
        self.y=htplayer.y

    def damage_area(self):
        nowanim=self.animations[self.state]
        size=nowanim.get_size()
        htplayer=pygame.Rect([self.x, self.y], size)
        htplayer=htplayer.inflate(tile_sizes*2, tile_sizes*2)
        return htplayer

realplayer=Player(100, 100, 4)
realplayer2=Player(200, 200, 4)

for i in range(0, 1):
    g=Ghost(random.randint(-1000000, 1000000), 0, 4)
    enemies.append(g)

timestart=time.time()
count=0

while True:
    if time.time()-timestart>=1:
        pygame.display.set_caption(str(count))
        timestart=time.time()
        count=0
    count+=1
    clock.tick(60)
    screen.fill([0, 0, 0])

    # оптимизация(берем 1 раз pos вместо нескольких)
    pos=pygame.mouse.get_pos()
    x_ts=(pos[0]+camerax)//tile_sizes
    y_ts=(pos[1]+cameray)//tile_sizes

    screen.blit(background, [0, 0])

    lev_load.camerax=camerax
    lev_load.cameray=cameray
    lev_load.render_blocks(screen)

    realplayer.render()
    realplayer.update()

    inventory.render(screen)

    # оптимизация проверки врага
    for i in enemies:    
        if is_enemy_visible(i, realplayer):
            i.update() 
            i.render()
            i.ai()                      

    camerax+=(realplayer.x-screen_width/2-camerax)/50
    cameray+=(realplayer.y-screen_height/2-cameray)/10
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit() 
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_SPACE:
                if onground==True:
                    onground=False
                    realplayer.vy=-10          
                
            if event.key==pygame.K_a:
                realplayer.ka=True

            if event.key==pygame.K_d:
                realplayer.kd=True

            if event.key==pygame.K_e:
                if inventory.inv_state==True:
                    inventory.inv_state=False
                else:
                    inventory.inv_state=True

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                realplayer.ka=False
            
            if event.key==pygame.K_d:
                realplayer.kd=False

        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if inventory.inv_state==False:
                if (x_ts,y_ts) in lev_load.blocks:
                    rd=realplayer.damage_area()
                    if rd.collidepoint([pos[0]+camerax,pos[1]+cameray]):
                        lev_load.blocks[(x_ts,y_ts)]['hp']-=damage
                        if lev_load.blocks[(x_ts,y_ts)]['hp']<1:
                            lev_load.blocks[(x_ts,y_ts)]['hp']-=damage
                            inventory.add_type(lev_load.blocks[(x_ts,y_ts)]['type'])
                            del lev_load.blocks[(x_ts,y_ts)]
            else:           #перемещение блоков в инв
                selected_item=inventory.get_item_at_pos(pos)
                if selected_item is not None and selected_item.count_res>0:
                    drag_item=selected_item
                    drag_item.moving = True

        if event.type==pygame.MOUSEBUTTONUP and event.button==1:
            if inventory.inv_state and drag_item is not None:
                target_item=inventory.get_item_at_pos(pos)
                inventory.move_item(drag_item, target_item)
                drag_item.moving = False
                drag_item=None

    # юзание оптимизации
    render_damaged_blocks(screen,camerax,cameray)
    
    screen.blit(pix[0],pos)       
    pygame.display.update()
