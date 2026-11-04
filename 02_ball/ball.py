print("start")
import pygame, sys
from pygame.locals import *
import os

def getFileAdd(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file_name)


pygame.init()

size = width, height = 800, 600
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load(getFileAdd("./intro_ball.gif"))
ballrect = ball.get_rect()
clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]*1.2
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]*1.1

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(60)
