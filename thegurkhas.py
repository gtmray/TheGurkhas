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

# For player
x=50
y=300
upper_boundary=220
width=40
height=60
velocity=10

# For enemy
enemy_count = 0
enemies_list = []
enemy_speed = 10
e_width = 10
e_height = 10

time_current = time()
score = 0
kill_range = 50
run = True
freeze = False

# For pillar
x_pillar = 400
y_pillar = 300
w_pillar = 20
h_pillar = 20

# Sounds
killing_sound = pygame.mixer.Sound("Sounds/Enemy killed.wav")
game_over_sound = pygame.mixer.Sound("Sounds/Game over.wav")
play_once = True # For gameover sound

def draw_forts():
  fort_width = 20
  fort_height = 30

  x1_fort = 0
  y1_fort = scheight/3
  pygame.draw.rect(win, blue, (x1_fort, y1_fort, fort_width, fort_height))

  x2_fort = scwidth/2
  y2_fort = scheight/3
  pygame.draw.rect(win, blue, (x2_fort, y2_fort, fort_width, fort_height))

  x3_fort = scwidth
  y3_fort = scheight/3
  pygame.draw.rect(win, blue, (x3_fort, y3_fort, fort_width, fort_height))

  x4_fort = 0
  y4_fort = scheight
  pygame.draw.rect(win, blue, (x4_fort, y4_fort, fort_width, fort_height))

  x5_fort = scwidth/2
  y5_fort = scheight
  pygame.draw.rect(win, blue, (x5_fort, y5_fort, fort_width, fort_height))

  x6_fort = scwidth
  y6_fort = scheight
  pygame.draw.rect(win, blue, (x6_fort, y6_fort, fort_width, fort_height))

def random_enemies_create(width, height):
    global enemy_count
    range_a, range_b = 220, 500
    random_y = random.randint(range_a, range_b) # Randomize enemy position
    x, y = 490, random_y

    if enemy_count < 5:
      enemies_list.append([x, y, width, height])
      enemy_count += 1
    #print(enemies_list)
    return enemies_list

def enemies_movement(enemies_list, enemy_speed):
  global freeze
  if freeze==False:
    for items in enemies_list:
      items[0] = items[0] - enemy_speed # Enemies movement to left
    
  for co_x, co_y, co_w, co_h in enemies_list:
    pygame.draw.rect(win, (255, 255, 0), (co_x, co_y, co_w, co_h))

def enemy_crossing_score(enemies_list):
  global score
  global enemy_count
  for items in enemies_list:
    if items[0]<0:
      score -= 1
      enemies_list.remove(items)
      enemy_count -= 1

def kill_enemy(enemies_list, kill_range):
  global score
  global enemy_count

  for i in enemies_list:
      if((i[0] > (x-kill_range) and i[0] < (x+kill_range)) and (i[1] > (y-kill_range) and i[1] < (y+kill_range))):
        enemies_list.remove(i)
        score += 1
        enemy_count -= 1
  pygame.mixer.Sound.play(killing_sound)
  pygame.mixer.music.stop()

def show_score(score):
  font = pygame.font.Font('freesansbold.ttf', 20)
  Score = f"Score: {score}"
  text = font.render(Score, True, black, white)
  textRect = text.get_rect()
  textRect.center = (scwidth//2, scheight//5)
  win.blit(text, textRect)

def create_pillar(x, y, w, h):
  pygame.draw.rect(win, white, (x, y, w, h))

def carry_pillar(enemies_list, x_pillar, y_pillar):
  closeness = 20
  for i in enemies_list:
    if((i[0] > (x_pillar-closeness) and i[0] < (x_pillar+closeness)) and (i[1] > (y_pillar-closeness) and i[1] < (y_pillar+closeness))):
      x_pillar = i[0]
      y_pillar = i[1]
  return x_pillar, y_pillar

def game_over(x_pillar):
  global freeze
  font = pygame.font.Font('freesansbold.ttf', 15)
  Score = f"BORDER ENCROACHMENT | GAME OVER!!! | Score: {score}"
  text = font.render(Score, True, black, white)
  textRect = text.get_rect()
  textRect.center = (scwidth//2, scheight//5)
  win.blit(text, textRect)
  freeze = True

while run:

  pygame.time.delay(100)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      #run == False
      pygame.quit()
      sys.exit()

  keys = pygame.key.get_pressed()
  if freeze==False:
  
    if keys[pygame.K_LEFT] and x > velocity:
        x -= velocity
    
    if keys[pygame.K_RIGHT] and x < scwidth - width - velocity:
        x += velocity

    if keys[pygame.K_UP] and y > velocity:
        if(y>=upper_boundary): # Upper boundary for player
          y -= velocity

    if keys[pygame.K_DOWN] and y < scheight - height - velocity:
        y += velocity
    
    if keys[pygame.K_SPACE]:
        kill_enemy(enemies_list, kill_range)
  
  win.fill((0, 0, 0)) # Filling with black screen

  # Background create
  pygame.draw.rect(win, (0, 145, 0), (0, 0, scwidth, scheight/3))
  draw_forts()

  # Player create
  pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))

  if(round((time()-time_current))%5==0): # Creating enemies every 5 seconds
    en_list = random_enemies_create(e_width, e_height)
  
  enemies_movement(en_list, enemy_speed)
  enemy_crossing_score(en_list)
  create_pillar(x_pillar, y_pillar, w_pillar, h_pillar)
  x_pillar, y_pillar = carry_pillar(enemies_list, x_pillar, y_pillar)
  
  if x_pillar < 5: # Check if pillar reaches to left-most side
    game_over(x_pillar)
    if play_once == True:
      pygame.mixer.Sound.play(game_over_sound)
      pygame.mixer.music.stop()
      play_once = False

  else:
    show_score(score)  
  
  pygame.display.update()
