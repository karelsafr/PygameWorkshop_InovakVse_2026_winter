import pygame,sys
import random # není soucástí stan. template ale pro nasi ilustraci.

# konstanty a fce které neinteragují s pygame!
BLACK = (0,0,0)
PURPLE = (150, 10, 100)
RED = (255, 0, 0)
GREEN = (0,255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
FPS = 60



## Start pygame + start modulů! 
pygame.init()

# Grafika!


# Definice spritu
class kostka(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.speedx = 0
        self.speedy = 0
        self.delta = 10

        
    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx -= self.delta
        if keystate[pygame.K_RIGHT]:
            self.speedx += self.delta
        if keystate[pygame.K_UP]:
            self.speedy -= self.delta
        if keystate[pygame.K_DOWN]:
            self.speedy += self.delta

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

# Nastaveni okna aj.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My caption of the game")


# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()
kosticka = kostka(WIDTH/2, HEIGHT/2)
my_sprites.add(kosticka)
# start:
running = True

# cyklus udrzujici okno v chodu
while running:
    # FPS kontrola / jeslti bezi dle rychlosti!
    clock.tick(FPS)

    # Event
    for event in pygame.event.get():
        # print(event) - pokud potrebujete info co se zmacklo.
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            k = kostka(event.pos[0],event.pos[1])
            my_sprites.add(k)
            #print(event)
    

    # Update
    my_sprites.update()
    

    # Render
    screen.fill(BLACK)
    my_sprites.draw(screen)
    pygame.display.flip()
    


pygame.quit()
