import pygame
import sys
import random
from time import time, sleep

# Pygame initialization

pygame.init()

# Screen width
scwidth = 500

# Screen height
scheight = 500

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

win = pygame.display.set_mode((scwidth, scheight))
pygame.display.set_caption("The Gurkhas")
icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)

title_image_file = "Images/title.png"
title_image = pygame.image.load(title_image_file)

background1_image_file = "Images/map1.png"
background1_image = pygame.image.load(background1_image_file)
background2_image_file = "Images/map2.png"
background2_image = pygame.image.load(background2_image_file)
background3_image_file = "Images/map3.png"
background3_image = pygame.image.load(background3_image_file)

playground_file = "Images/playground.png"
playground = pygame.image.load(playground_file)

pillar_file = "Images/pillar.png"
pillar = pygame.image.load(pillar_file)

# For player
x = 50
y = 300
upper_boundary = 220 # Boundary upto which player can move on y axis
width = 40
height = 60
velocity = 10
move = 1 # To toggle legs position

player_image_file1 = "Images/right1.png"
player_image1 = pygame.image.load(player_image_file1)
player_image_file2 = "Images/right2.png"
player_image2 = pygame.image.load(player_image_file2)


player_image_kill = "Images/khukuri show.png"
player_kills = pygame.image.load(player_image_kill)

# For enemy
enemy_count = 0
enemies_list = []
enemy_speed = 10
e_width = 10
e_height = 10
en_list = []
move_enemy = 1
enemy_image_file1 = "Images/enemy1.png"
enemy_image1 = pygame.image.load(enemy_image_file1)
enemy_image_file2 = "Images/enemy2.png"
enemy_image2 = pygame.image.load(enemy_image_file2)

enemy_killed_file = "Images/killed.png"
enemy_killed = pygame.image.load(enemy_killed_file)

time_current = time() # Current time
score = 0
kill_range = 50 # Distance considered for killing
freeze = False # True when game over

# Sounds
background_sound = pygame.mixer.Sound("Sounds/Background.ogg")
killing_sound = pygame.mixer.Sound("Sounds/Enemy killed.wav")
game_over_sound = pygame.mixer.Sound("Sounds/Game over.wav")
pygame.mixer.Sound.play(background_sound)
pygame.mixer.Sound.set_volume(background_sound, 0.2)

color_light = (170, 170, 170)
color_dark = (100, 100, 100)

smallfont = pygame.font.SysFont('Corbel', 35)

new_game_text = smallfont.render('NEW GAME', True, white)
instructions_text = smallfont.render('INSTRUCTIONS', True, white)
about_us_text = smallfont.render('ABOUT US', True, white)
quit_text = smallfont.render('QUIT', True, white)

global run, menu, instructions
menu = True
run = False
instructions = False
about = False


def draw_forts():
  color = (73, 77, 82)
  fort_width = 20
  fort_height = 30

  x1_fort = 0
  y1_fort = scheight/3
  pygame.draw.rect(win, color, (x1_fort, y1_fort, fort_width, fort_height))

  x2_fort = scwidth/2
  y2_fort = scheight/3
  pygame.draw.rect(win, color, (x2_fort, y2_fort, fort_width, fort_height))

  x3_fort = scwidth-20
  y3_fort = scheight/3
  pygame.draw.rect(win, color, (x3_fort, y3_fort, fort_width, fort_height))

  x4_fort = 0
  y4_fort = scheight-20
  pygame.draw.rect(win, color, (x4_fort, y4_fort, fort_width, fort_height))

  x5_fort = scwidth/2
  y5_fort = scheight-20
  pygame.draw.rect(win, color, (x5_fort, y5_fort, fort_width, fort_height))

  x6_fort = scwidth-20
  y6_fort = scheight-20
  pygame.draw.rect(win, color, (x6_fort, y6_fort, fort_width, fort_height))


def player_blit(player_image):
    win.blit(player_image, (x, y))

def enemy_killed_blit(killed_image, x_co, y_co):
    win.blit(killed_image, (x_co, y_co))

def background_blit(background_image):
    win.blit(background_image, (0, 0))

def playground_blit(playground):
    win.blit(playground, (0, 166))

def random_enemies_create(width, height):
    global enemy_count
    range_a, range_b = 220, 500 # Position of enemies in y axis
    random_y = random.randint(range_a, range_b)  # Randomize enemy position
    x, y = 490, random_y

    if enemy_count < 5:
      enemies_list.append([x, y, width, height]) # Create 5 enemies at a time
      enemy_count += 1
    # print(enemies_list)
    return enemies_list


def enemies_movement(enemies_list, enemy_speed):
  global freeze, move_enemy
  if freeze == False:
    for items in enemies_list:
      items[0] = items[0] - enemy_speed  # Enemies movement to left

  for co_x, co_y, co_w, co_h in enemies_list:
    #pygame.draw.rect(win, (255, 255, 0), (co_x, co_y, co_w, co_h))
    if freeze == False:
      if(move_enemy==1):
        move_enemy = 2
        win.blit(enemy_image1, (co_x, co_y))
      else:
        move_enemy = 1
        win.blit(enemy_image2, (co_x, co_y))
    else:
      win.blit(enemy_image1, (co_x, co_y))


def enemy_crossing_score(enemies_list):
  global score
  global enemy_count
  for items in enemies_list:
    if items[0] < 0: # When enemy reaches to the end(leftmost side)
      score -= 1
      enemies_list.remove(items)
      enemy_count -= 1


def kill_enemy(enemies_list, kill_range):
  global score
  global enemy_count

  killed = []
  for i in enemies_list:
      # Kill the enemies who are near to the player
      if((i[0] > (x-kill_range) and i[0] < (x+kill_range)) and (i[1] > (y-kill_range) and i[1] < (y+kill_range))):
        enemies_list.remove(i)
        score += 1
        enemy_count -= 1
        killed.append((i[0], i[1]))

  pygame.mixer.Sound.play(killing_sound)
  pygame.mixer.music.stop()
  return killed

def show_score(score):
  font = pygame.font.Font('freesansbold.ttf', 20)
  Score = f"Score: {score}"
  text = font.render(Score, True, black, white)
  textRect = text.get_rect()
  textRect.center = (scwidth//2, scheight//5)
  win.blit(text, textRect)


def create_pillar(x, y, w, h):
  #pygame.draw.rect(win, white, (x, y, w, h))
  win.blit(pillar, (x, y))


def carry_pillar(enemies_list, x_pillar, y_pillar, closeness):
  for i in enemies_list:
    # Carry the pillar if it is near enemy
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
  # Freeze player, enemy movement
  freeze = True

def main_menu(run, menu, instructions, about):
  while menu:
      mouse = pygame.mouse.get_pos()
      for ev in pygame.event.get():

          if ev.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

          if ev.type == pygame.MOUSEBUTTONDOWN:
              # New game 
              if 172 <= mouse[0] <= 338 and 85 <= mouse[1] <= 105:
                  run = True
                  menu = False
                  instructions = False

              # Instructions 
              if 172 <= mouse[0] <= 392 and 153 <= mouse[1] <= 177:
                  instructions = True
                  menu = False

              # About us 
              if 172 <= mouse[0] <= 324 and 223 <= mouse[1] <= 246:
                  about = True
                  menu = False
              
              # Quit
              if 172 <= mouse[0] <= 243 and 296 <= mouse[1] <= 318:
                  pygame.quit()
                  sys.exit()

      win.fill((60, 25, 60))
      # Draw a rectangle when hovered to the menu

      # New game
      if 172 <= mouse[0] <= 338 and 85 <= mouse[1] <= 105:
          pygame.draw.rect(win, color_light, [172, 80, 166, 40])

      # Instructions
      elif 172 <= mouse[0] <= 392 and 153 <= mouse[1] <= 177:
          pygame.draw.rect(win, color_light, [172, 145, 220, 40])

      # About us
      elif 172 <= mouse[0] <= 324 and 223 <= mouse[1] <= 246:
          pygame.draw.rect(win, color_light, [172, 220, 152, 40])

      # Quit
      elif 172 <= mouse[0] <= 243 and 296 <= mouse[1] <= 318:
          pygame.draw.rect(win, color_light, [172, 290, 71, 40])

      win.blit(new_game_text, (scwidth/2-80, scheight/2-170))
      win.blit(instructions_text, (scwidth/2-80, scheight/2-100))
      win.blit(about_us_text, (scwidth/2-80, scheight/2-30))
      win.blit(quit_text, (scwidth/2-80, scheight/2+40))
      win.blit(title_image, (80, 10))
      pygame.display.update()
  return run, menu, instructions, about

def instruct(instructions):
  global menu
  win.fill((60, 25, 60))
  while instructions:
    font = pygame.font.Font('freesansbold.ttf', 30)
    list_text = ["Press space bar ", "to kill the enemies",
        "and save our border.", " ", "AAYO GORKHALI!!!"]
    change = 0
    for i in list_text:
      # To display the text, changing the y axis line by 40 
      change += 40
      text = font.render(i, False, white)
      text_rect = (40, 40+change)
      win.blit(text, text_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    keys = pygame.key.get_pressed()
    
    # Return to main menu
    if keys[pygame.K_BACKSPACE]:
      instructions = False
      menu = True
      return menu, instructions
    pygame.display.update()
  return menu, instructions


def about_us(about):
  global menu
  win.fill((60, 25, 60))
  while about:
    font = pygame.font.Font('freesansbold.ttf', 30)
    list_text = ["We, the game developers", "are the students", "of IOE Thapathali Campus.", " ",
        "Rewan Gautam", "Bishwa Prakash Subedi", "Anjal Bam", "Bishwash Gurung", " ", "BEI 075"]
    change = 0
    for i in list_text:
      # To display the text, changing the y axis line by 40
      change += 40
      text = font.render(i, False, white)
      text_rect = (40, 40+change)
      win.blit(text, text_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
      about = False
      menu = True
      return menu, about
    pygame.display.update()
  return menu, about

def start_game(run):
  limpiyadhura = smallfont.render('Limpiyadhura', True, white)
  lipulekh = smallfont.render('Lipulekh', True, white)
  kalapani = smallfont.render('Kalapani', True, white)

  global menu, instructions, about, x, y, width, height, en_list, move

  # For pillar
  x_pillar = 400
  y_pillar = 300
  w_pillar = 20
  h_pillar = 20
  closeness = 30
  pillar_threshold = 5

  play_once = True  # For gameover sound
  kill_state = False # When set to true, player changes shape to killing position
  move_pressed = False # True when arrow keys pressed

  map1 = map2 = map3 = game_loop = False 
  while run:
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
            
        if ev.type == pygame.MOUSEBUTTONDOWN:

              # Limpiyadhura
              if 172 <= mouse[0] <= 338 and 85 <= mouse[1] <= 105:
                  map1 = True
                  game_loop = True
                  run = False

              # Kalapani
              if 172 <= mouse[0] <= 392 and 153 <= mouse[1] <= 177:
                  map2 = True
                  game_loop = True
                  run = False

              # Lipulekh
              if 172 <= mouse[0] <= 324 and 223 <= mouse[1] <= 246:
                  map3 = True
                  game_loop = True
                  run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        instructions = False
        menu = True
        run = False
        return run, menu, instructions, about
    win.fill((60, 25, 60))

    # For hovering
    # Map 1
    if 172 <= mouse[0] <= 338 and 85 <= mouse[1] <= 105:
      pygame.draw.rect(win, color_light, [172, 80, 190, 40])

    # Map 2
    elif 172 <= mouse[0] <= 392 and 153 <= mouse[1] <= 177:
      pygame.draw.rect(win, color_light, [172, 145, 130, 40])

    # Map 3
    elif 172 <= mouse[0] <= 324 and 223 <= mouse[1] <= 246:
      pygame.draw.rect(win, color_light, [172, 220, 130, 40])

    win.blit(limpiyadhura, (scwidth/2-80, scheight/2-170))
    win.blit(lipulekh, (scwidth/2-80, scheight/2-100))
    win.blit(kalapani, (scwidth/2-80, scheight/2-30))

    pygame.display.update()

  while game_loop:
    # Reset arrow keys movement flag
    move_pressed = False

    # To avoid drastic change of co-ordinates
    pygame.time.delay(100)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    keys = pygame.key.get_pressed()
    if freeze == False:

      if keys[pygame.K_LEFT] and x > velocity:
          x -= velocity
          move_pressed = True

      if keys[pygame.K_RIGHT] and x < scwidth - width - velocity:
          x += velocity
          move_pressed = True

      if keys[pygame.K_UP] and y > velocity:
          if(y >= upper_boundary):  # Upper boundary for player
            y -= velocity
            move_pressed = True

      if keys[pygame.K_DOWN] and y < scheight - height - velocity:
          y += velocity
          move_pressed = True

      if keys[pygame.K_SPACE]:
          kill_state = True
          killed = kill_enemy(enemies_list, kill_range)

      if keys[pygame.K_BACKSPACE]:
          instructions = False
          menu = True
          run = False
          return run, menu, instructions, about

    # To fill playing area
    win.fill((89, 89, 36))  
    #win.fill((92, 42, 16))
    #win.fill((48, 100, 115))
    #win.fill((181, 173, 136))
    #playground_blit(playground)

    # Background create
    #pygame.draw.rect(win, (0, 145, 0), (0, 0, scwidth, scheight/3))
    draw_forts()
  
    # Player create

    # If space bar not pressed check if any keys pressed
    # If pressed change blit images
    # Else don't change
    if kill_state==False:
      if(move_pressed == True):
        if move==1:
          move = 2
          player_blit(player_image1)
        else:
          move = 1
          player_blit(player_image2)
      else:
        player_blit(player_image1)
    else:
      for i in killed:
          enemy_killed_blit(enemy_killed, i[0], i[1])
      player_blit(player_kills)

      kill_state = False
    if(round((time()-time_current)) % 5 == 0):  # Creating enemies every 5 seconds
      en_list = random_enemies_create(e_width, e_height)

    if map1 == True:
      background_blit(background1_image)
      enemies_movement(en_list, enemy_speed)
    elif map2 == True:
      background_blit(background2_image)
      closeness = 40
      pillar_threshold = 20
      # Increased enemy speed for map2
      enemies_movement(en_list, enemy_speed+10)
    elif map3 == True:
      background_blit(background3_image)
      closeness = 40
      pillar_threshold = 20
      # Increased enemy speed for map3
      enemies_movement(en_list, enemy_speed+15)
      
    enemy_crossing_score(en_list)
    create_pillar(x_pillar, y_pillar, w_pillar, h_pillar)
    x_pillar, y_pillar = carry_pillar(enemies_list, x_pillar, y_pillar, closeness)

    if x_pillar < pillar_threshold:  # Check if pillar reaches to left-most side
      game_over(x_pillar)

      # To avoid game over looping sound
      if play_once == True:
        pygame.mixer.Sound.play(game_over_sound)
        pygame.mixer.music.stop()
        play_once = False
      # pygame.mixer.music.pause

    else:
      show_score(score)

    pygame.display.update()
  return run, menu, instructions, about

condition = True
while condition:
  run, menu, instructions, about = main_menu(run, menu, instructions, about)
  menu, instructions = instruct(instructions)
  menu, about = about_us(about)
  run, menu, instructions, about = start_game(run)

