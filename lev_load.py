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

def render_blocks(screen):
    for i in blocks.values():
        screen.blit(resourses[i['number']],[i['x']*tile_sizes-camerax,i['y']*tile_sizes-cameray])
    pos=pygame.mouse.get_pos()

    x=(pos[0]+camerax)//tile_sizes
    y=(pos[1]+cameray)//tile_sizes

    if (x,y) in blocks:
        pygame.draw.rect(screen,[0,0,0],[x*tile_sizes-camerax,y*tile_sizes-cameray,tile_sizes,tile_sizes],2)
