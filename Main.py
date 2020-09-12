import pygame
from pygametexting import pyg_text
import random, time

def draw_choices(windows, choices, choices_pos, rules):
    active_choice = random.choice(choices)
    color = random.choice(rules)
    random.shuffle(choices)
    bg_rect = pygame.Rect(0,0,150,150)
    bg_rect.center = (screen_range[0]//2,150)
    bg = pygame.Surface.fill(wind,color[0], rect = bg_rect)
    windows.blit(active_choice[1],bg)

    for i in range(len(choices)):

        windows.blit(choices[i][1], choices_pos[i])
        
    current_order = []
    
    for i in choices:
        current_order.append(i[0])
        
    return [active_choice[0],color[1],current_order]

def start_restart():
    
    global points, timer, remaining_time, secrets
    
    points = 0
    timer = time.time() + 60
    remaining_time = int(timer - time.time())
    wind.fill((0,0,0))
    secrets = draw_choices(wind, choices, choices_pos, rules)
    

pygame.init()

screen_range = (500,500)

wind = pygame.display.set_mode(screen_range)

pygame.display.set_caption("RPS - Jupyter")

pygtxt=pyg_text(20,(255,255,255),"comicsansms",wind)

clock = pygame.time.Clock()

clock_time = 60

run = True

neutral_choices = ["Rock","Paper","Scissors"]

choices = [["Rock",pygame.image.load("Images\Rock.png")],["Paper",pygame.image.load("Images\Paper.png")],
           ["Scissors",pygame.image.load("Images\Scissors.png")]]

choices_pos = []
clicks_pos = []

x_pos = 100
y_pos = 325

for i in range(len(choices)):
    pos = choices[i][1].get_rect()
    pos_size = pos.size
    clicks_pos.append([x_pos-pos_size[0]//2,y_pos-pos_size[1]//2,pos_size[0],pos_size[1]])
    pos.center = (x_pos,y_pos)
    choices_pos.append(pos)
    x_pos += 150
    
on_init_screen = True

rules = [[(255,0,0),-2], [(0,255,0),-1], [(0,0,255),0]]

start_game_pos = 50

while run:
    
    clock.tick(clock_time)
    
    keys = pygame.key.get_pressed()
            
    mouse = pygame.mouse.get_pressed()
    
    mouse_pos = pygame.mouse.get_pos()
    
    point_press = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            point_press = True

    # Quits
    if keys[pygame.K_ESCAPE]:
        run = False
    
    wind.fill((0,0,0),rect = (200,20,300,50))
    
    if on_init_screen:
        
        if pygtxt.screen_button_centerpos("Start",screen_range[0]//2,start_game_pos):
            on_init_screen = False
            start_restart()
            
    else:
        
        if mouse[2]:
            pygame.time.delay(150)
            start_restart()
            
        if remaining_time>0:
        
            remaining_time = round(timer - time.time(),2)
            pygtxt.screen_text_centerpos(remaining_time,screen_range[0]//2,start_game_pos)

            for i,j in zip(clicks_pos,range(len(clicks_pos))):
                if i[0]<mouse_pos[0]<i[0]+i[2] and i[1]<mouse_pos[1]<i[1]+i[3]:
                    if point_press:
                        check_index = neutral_choices.index(secrets[0])
                        if secrets[2][j] == neutral_choices[check_index+secrets[1]]:
                            points += 1
                            # timer += 1
                        else:
                            timer -= 3
                            
                        
                        wind.fill((0,0,0))
                        secrets = draw_choices(wind, choices, choices_pos, rules)
                        pygame.time.delay(150)
                        
        else:
            
            if pygtxt.screen_button_centerpos("Replay",screen_range[0]//2,start_game_pos):
                start_restart()

        wind.fill((0,0,0),rect = (200,420,300,450))   
        pygtxt.screen_text_centerpos("Points: {0}".format(points),screen_range[0]//2,450)
        #pygtxt.screen_text_centerpos(mouse_pos,screen_range[0]//2,450)

    pygame.display.update()

pygame.quit()
    
