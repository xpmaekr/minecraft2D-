import pygame
import time
import random
import math
import os
import pickle
import cfiles

d=w=a=s=False

block_stages={}
block_stage1=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 1.png',80,80)
block_stage2=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 2.png',80,80)
block_stage3=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 3 .png',80,80)
block_stage4=cfiles.loadimagesize('break_blocks/блоки-removebg-preview 4.png',80,80)

block_stages['20']=block_stage4
block_stages['40']=block_stage3
block_stages['60']=block_stage2
block_stages['80']=block_stage1

idle=cfiles.getcutpic('craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Idle_4.png',4,3)
gidle=cfiles.getcutpic('2plan/2 Owlet_Monster/Owlet_Monster_Idle_4.png',4,3)


pygame.init()
screen=pygame.display.set_mode([800,600])   #рамки экрана
tile_sizes=80
clock=pygame.time.Clock()

camerax=cameray=0

resourses=[]
state_res=17

tree_tex=pygame.image.load('tree_tex.jpg')
leaf_tex=pygame.image.load('leaf_tex.png')

blocks={}

for i in sorted(os.listdir('editor/imgs/1 Tiles')):
    image=pygame.image.load('editor/imgs/1 Tiles/'+i)
    image=pygame.transform.scale(image,[tile_sizes,tile_sizes])
    resourses.append(image)

resourses.append(idle[0])
resourses.append(gidle[0])
resourses.append(tree_tex)
resourses.append(leaf_tex)

def render_blocks():
    for i in blocks.values():
        screen.blit(resourses[i['number']],[i['x']*tile_sizes-camerax,i['y']*tile_sizes-cameray])

def render_resourses():
    mx=pygame.mouse.get_pos()[0]
    my=pygame.mouse.get_pos()[1]
    print(state_res,len(resourses))
    res_image=resourses[state_res]
    xpos_box=(mx+camerax)//tile_sizes*tile_sizes
    ypos_box=(my+cameray)//tile_sizes*tile_sizes
    res_image.set_alpha(100)
    screen.blit(res_image,[xpos_box-camerax,ypos_box-cameray])
    res_image.set_alpha(255)


def render_grid():
    xstart=(camerax//tile_sizes*tile_sizes)-camerax
    for i in range(xstart,800+tile_sizes,tile_sizes):
        pygame.draw.line(screen,[90,90,90],[i,0],[i,600])

    ystart=(cameray//tile_sizes*tile_sizes)-cameray
    for i in range(ystart,600+tile_sizes,tile_sizes):
        pygame.draw.line(screen,[90,90,90],[0,i],[800,i])

grid_mode=True

def change_size():
    global resourses
    resourses=[]

    image1=idle[0]
    image1=pygame.transform.scale(image1,[tile_sizes,tile_sizes])     
    image2=gidle[0]
    image2=pygame.transform.scale(image2,[tile_sizes,tile_sizes])   
    image3=tree_tex
    image3=pygame.transform.scale(image3,[tile_sizes,tile_sizes])  
    image4=leaf_tex
    image4=pygame.transform.scale(image4,[tile_sizes,tile_sizes])  


    for i in sorted(os.listdir('editor/imgs/1 Tiles')):
        image=pygame.image.load('editor/imgs/1 Tiles/'+i)
        image=pygame.transform.scale(image,[tile_sizes,tile_sizes])
        resourses.append(image)
    resourses.append(image1)
    resourses.append(image2)
    resourses.append(image3)
    resourses.append(image4)


def transform():
    for i in blocks.values():
        x=i['x']
        y=i['y']
        state=i['type']

        if state=='idle':
            continue

        topn=False
        downn=False
        rightn=False
        leftn=False

        if (x,y-1) in blocks:
            if state==blocks[(x,y-1)]['type']:
                topn=True    
        if (x+1,y) in blocks:
            if state==blocks[(x+1,y)]['type']:
                rightn=True  
        if (x,y+1) in blocks:
            if state==blocks[(x,y+1)]['type']:
                downn=True
        if (x-1,y) in blocks:
            if state==blocks[(x-1,y)]['type']:
                leftn=True

        if state=='rock':
            if rightn==False and topn==False and leftn==False and downn==False:
                i['number']=29
            if rightn==True and topn==False and leftn==False:
                i['number']=8
            if rightn==True and topn==False and leftn==True:
                i['number']=9
            if rightn==False and topn==False and leftn==True:
                i['number']=11 
    
            

        if state=='grass':
            if rightn==False and topn==False and leftn==False and downn==False:
                i['number']=17
            if rightn==True and topn==False and leftn==False:
                i['number']=0
            if rightn==True and topn==False and leftn==True:
                i['number']=1
            if rightn==False and topn==False and leftn==True:
                i['number']=2

        if state=='tree':
            i['number']==96
        
        else:
            if state=='leaf':
                i['number']==97
            
            else:
        
                if topn==True and rightn==True and leftn==False and downn==False:
                    i['number']=24
                if topn==True and leftn==True and downn==False and rightn==False:
                    i['number']=27
                if topn==True and leftn==True and rightn==True and downn==False:
                    i['number']=25
                if topn==True and leftn==False and rightn==False and downn==False:
                    i['number']=28
                if topn==True and downn==True and leftn==False and rightn==False:
                    i['number']=59
                if topn==True and downn==True and leftn==False and rightn==True:
                    i['number']=60
                if topn==True and downn==True and leftn==True and rightn==True:
                    i['number']=72
                if topn==True and downn==True and leftn==True and rightn==False:
                    i['number']=61

def get_type(number):
    if number<9 or number==17:
        type='grass'
    else: 
        type='rock'
        if number in range(42,48) or number in range(74,97) or number in range(54,60):
            type='strange'
        if number==95:
            type='idle'
        if number==97:
            type='tree'
        if number==98:
            type='leaf'
    return(type)

def save():
    f=open('editor/levels/level1','wb')
    pickle.dump([blocks,[camerax,cameray]],f)
    f.close()
def load():
    global blocks,camerax,cameray
    f=open('editor/levels/level1','rb')
    load_game=pickle.load(f)
    blocks=load_game[0]
    camerax=load_game[1][0]
    cameray=load_game[1][1]
    f.close()

while True:
    pygame.display.set_caption(str((camerax,cameray)))
    clock.tick(60)
    screen.fill([0,0,0])

    render_resourses()
    render_blocks()
    
    if grid_mode==True:
        render_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type==pygame.MOUSEWHEEL:
            tile_sizes+=5*event.y
            if tile_sizes<25:
                tile_sizes=25
            if tile_sizes>200:
                tile_sizes=200
            change_size()
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1:
                state_res=0
            if event.key==pygame.K_2:
                state_res=10
            if event.key==pygame.K_3:
                state_res=97
                change_size()
            if event.key==pygame.K_4:
                state_res=98
                change_size()
            if event.key==pygame.K_5:
                state_res=95
            if event.key==pygame.K_6:
                state_res=96
                change_size()

            if event.key==pygame.K_w:
                w=True
            if event.key==pygame.K_a:
                a=True
            if event.key==pygame.K_s:
                s=True
            if event.key==pygame.K_d:
                d=True
            if event.key==pygame.K_c:
                blocks={}
            if event.key==pygame.K_g:           
                if grid_mode==False:
                    grid_mode=True
                else:
                    grid_mode=False
        
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                w=False
            if event.key==pygame.K_a:
                a=False
            if event.key==pygame.K_s:
                s=False
            if event.key==pygame.K_d:
                d=False
            if event.key==pygame.K_v:
                save()
            if event.key==pygame.K_l:
                load()
            if event.key==pygame.K_r:
                blocks={}
    
    if d:
        camerax=camerax+10
    if a:
        camerax=camerax-10
    if s:
        cameray=cameray+10
    if w:
        cameray=cameray-10

    if pygame.mouse.get_pressed()[0]:
            mx=pygame.mouse.get_pos()[0]
            my=pygame.mouse.get_pos()[1]
            xpos_box=(mx+camerax)//tile_sizes*tile_sizes
            ypos_box=(my+cameray)//tile_sizes*tile_sizes
            for i in blocks.values():
                if i['x']==xpos_box and i['y']==ypos_box:
                    blocks.remove(i)
            block={
                'x': xpos_box//tile_sizes,
                'y': ypos_box//tile_sizes,
                'number': state_res,
                'type': get_type(state_res),
                'hp': 100
                
            }
            print(block)
            blocks[(block['x'],block['y'])]=block
            transform()

    pygame.display.update()