import pygame
import sys
import random
from time import time, sleep

pygame.init()
scwidth = 500
scheight = 500
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
win = pygame.display.set_mode((scwidth, scheight))
pygame.display.set_caption("The Gurkhas")

x=50
y=300
upper_boundary=220
width=40
height=60
velocity=10
run = True

enemy_count = 0
enemies_list = []
enemy_speed = 10
e_width = 10
e_height = 10

time_current = time()

def random_enemies_create(width, height):
    global enemy_count
    range_a, range_b = 220, 500
    random_y = random.randint(range_a, range_b) # Randomize enemy position
    x, y = 490, random_y

    if enemy_count < 5:
      enemies_list.append([x, y, width, height])
      enemy_count += 1
    print(enemies_list)
    return enemies_list

def draw_forts():
  fort_width = 20
  fort_height = 30
  
  x1_fort= 0
  y1_fort=scheight/3
  pygame.draw.rect(win, blue, (x1_fort, y1_fort, fort_width, fort_height))
  
  x2_fort= scwidth/2
  y2_fort=scheight/3
  pygame.draw.rect(win, blue, (x2_fort, y2_fort, fort_width, fort_height))
  
  x3_fort=scwidth
  y3_fort=scheight/3
  pygame.draw.rect(win, blue, (x3_fort, y3_fort, fort_width, fort_height))
  
  x4_fort= 0
  y4_fort=scheight
  pygame.draw.rect(win, blue, (x4_fort, y4_fort, fort_width, fort_height))
  
  x5_fort= scwidth/2
  y5_fort=scheight
  pygame.draw.rect(win, blue, (x5_fort, y5_fort, fort_width, fort_height))
  
  x6_fort=scwidth
  y6_fort=scheight
  pygame.draw.rect(win, blue, (x6_fort, y6_fort, fort_width, fort_height))
  
def enemies_movement(enemies_list, enemy_speed):
  for items in enemies_list:
    items[0] = items[0] - enemy_speed # Enemies movement to left
    
  for co_x, co_y, co_w, co_h in enemies_list:
    pygame.draw.rect(win, (255, 255, 0), (co_x, co_y, co_w, co_h))

while run:

  pygame.time.delay(100)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      #run == False
      pygame.quit()
      sys.exit()
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and x > velocity:
      x -= velocity
  
  if keys[pygame.K_RIGHT] and x < scwidth - width - velocity:
      x += velocity

  if keys[pygame.K_UP] and y > velocity:
      if(y>=upper_boundary): # Upper boundary for player
        y -= velocity

  if keys[pygame.K_DOWN] and y < scheight - height - velocity:
      y += velocity
  
  win.fill((0, 0, 0))  
  
  #background create
  pygame.draw.rect(win, (0, 145, 0), (0,0, scwidth, scheight/3))
  #player create
  pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
  draw_forts()
  if(round((time()-time_current))%5==0): # Creating enemies every 5 seconds
    en_list = random_enemies_create(e_width, e_height)
  
  enemies_movement(en_list, enemy_speed)
  pygame.display.update()