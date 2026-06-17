import pygame
import time
import random
import cfiles
import math
import animation
import pickle
import os



def load():
    global blocks,camerax,cameray,pix
    f=open('editor/levels/level1','rb')
    load_game=pickle.load(f)
    blocks=load_game[0]
    camerax=load_game[1][0]
    cameray=load_game[1][1]
    f.close()
    pix=pygame.image.load('pixare.png')
    pix=pygame.transform.flip(pix,True,False)
    pygame.mouse.set_visible(False) 

resourses=[]
tile_sizes=80
for i in sorted(os.listdir('editor/imgs/1 Tiles')):
    image=pygame.image.load('editor/imgs/1 Tiles/'+i)
    image=pygame.transform.scale(image,[tile_sizes,tile_sizes])
    
    resourses.append(image)

tree=pygame.image.load('tree_tex.jpg')
tree=cfiles.loadimagesize('tree_tex.jpg',80,80)   

leaf=pygame.image.load('leaf_tex.png')
leaf=cfiles.loadimagesize('leaf_tex.png',80,80)

craft_table=pygame.image.load('crafting table.png')
craft_table=cfiles.loadimagesize('crafting table.png',80,80)   

idle=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Idle_4.png',4,3)
gidle=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Idle_4.png',4,3)

resourses.append(idle[0])
resourses.append(gidle[0])
resourses.append(tree)
resourses.append(leaf)
resourses.append(craft_table)

print(resourses)

#для превращения типа блока в номер в resourses
type_to_number = {
    'tree': len(resourses) - 3,
    'leaf': len(resourses) - 2,
    'craft_table': len(resourses) - 1,
    'grass' : 4,
    'rock' : 29
}

def place_block(x, y, block_type,player):
    #ставит блоки на координаты
    if (x, y) not in blocks:

        # проверяем, не стоит ли игрок на месте блока

        if player.get_hitbox().colliderect(pygame.Rect([x * tile_sizes,y * tile_sizes] , [tile_sizes ,tile_sizes ])) :
            return False
        

        if block_type in type_to_number:
            blocks[(x, y)] = {
                'number': type_to_number[block_type],
                'x': x,
                'y': y,
                'hp': 100,
                'type': block_type
            }
            return True
    return False

def render_blocks(screen):
    global camerax , cameray

    for i in blocks.values():
        screen.blit(resourses[i['number']],[i['x']*tile_sizes-camerax,i['y']*tile_sizes-cameray])
    pos=pygame.mouse.get_pos()

    x=(pos[0]+camerax)//tile_sizes
    y=(pos[1]+cameray)//tile_sizes

    if (x,y) in blocks:
        pygame.draw.rect(screen,[0,0,0],[x*tile_sizes-camerax,y*tile_sizes-cameray,tile_sizes,tile_sizes],2)

    else:
        # рисуем зелёный прямоугольник если можно блок поставить
        pygame.draw.rect(screen,[0,255,0],[x*tile_sizes-camerax,y*tile_sizes-cameray,tile_sizes,tile_sizes],2)
