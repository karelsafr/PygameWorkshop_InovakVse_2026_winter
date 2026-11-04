import pygame

# konstanty a fce které neinteragují s pygame!
BLACK = (0,0,0)
PURPLE = (150, 10, 100)
RED = (255, 0, 0)
GREEN = (0,255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
FPS = 45



## Start pygame + start modulů! 
pygame.init()


# Definice spritu
class kostka(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
    def update(self):
        self.rect.x -=5
        self.rect.y +=1

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

        

# Nastaveni okna aj.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My caption of the game")


# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()
kosticka = kostka()
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
    

    # Update
    my_sprites.update()
    

    # Render
    screen.fill(BLACK)
    my_sprites.draw(screen)
    pygame.display.flip()
    


pygame.quit()
