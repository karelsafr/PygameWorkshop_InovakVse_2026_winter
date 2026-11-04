import pygame,sys
import random # není soucástí stan. template ale pro nasi ilustraci.
from os import path


# konstanty a fce které neinteragují s pygame!
BLACK = (0,0,0)
PURPLE = (150, 10, 100)
RED = (255, 0, 0)
GREEN = (0,255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 480
FPS = 45

folder = path.dirname(__file__)

#fce které interagují s pygame!


## Start pygame + start modulů! 
pygame.init()
pygame.mixer.init()



# Nastaveni okna aj.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My caption of the game")

# obecnou tridu:
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def one_image(self, x, y, w, h):
        image = pygame.Surface((w,h))
        image.blit(self.spritesheet, (0,0), (x, y, w , h))
        return image

player = Spritesheet(path.join(folder, "player_blue.png"))

# Grafika a hudba!
ground = pygame.image.load(path.join(folder, "pozadi.png")).convert()
punch = pygame.mixer.Sound(path.join(folder, "sfx_punch.wav"))

# Definice spritu

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player.one_image(0,0,46,50)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.bottom = 372
        self.rect.x = WIDTH /2 - 46
        self.x = float(self.rect.x)

        self.orient = True
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.x += 5
            self.orient = True
        if keystate[pygame.K_LEFT]:
            self.x -= 5
            self.orient = False
        self.rect.x = round(self.x)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_LEFT]:
            now = pygame.time.get_ticks()
            if now - self.last_update > 25:
                self.frame = (self.frame + 1) % 8
                self.last_update = now
            self.image = player.one_image(self.frame * 46, 150, 46, 50)
        else:
            self.image = player.one_image(0, 0, 46, 50)

        if not self.orient:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        if keystate[pygame.K_SPACE]:
            punch.play()

            center = self.rect.center
            
            if self.orient:
                self.image = player.one_image(3*46,0, 46,50)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.image.set_colorkey(BLACK)
                box = boxik(self.rect.midright[0],self.rect.midright[1])
                my_sprites.add(box)
            else:
                self.image = pygame.transform.flip(player.one_image(3*46,0, 46,50),True, False)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.image.set_colorkey(BLACK)
                box = boxik(self.rect.midleft[0],self.rect.midleft[1])
                my_sprites.add(box)



class boxik(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center =(x,y-7)
        self.start = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.start > 250:
            self.kill()

# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()
fighter = Fighter()
my_sprites.add(fighter)

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
    

    # Update
    my_sprites.update()
    

    # Render
    screen.fill(BLACK)
    screen.blit(ground, (0,0))
    my_sprites.draw(screen)
    pygame.display.flip()
    


pygame.quit()
