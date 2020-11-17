import pygame
import sys

pygame.init()
scwidth = 500
scheight = 500
win = pygame.display.set_mode((scwidth, scheight))
pygame.display.set_caption("The Gurkhas")

x=50
y=300
upper_boundary=220
width=40
height=60
velocity=10

run = True
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
    
  pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
  pygame.display.update()