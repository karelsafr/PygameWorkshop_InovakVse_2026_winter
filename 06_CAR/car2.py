import pygame, sys, os
import math
from os import path

# Konstanty
BLACK = (0,0,0)
WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
FPS = 60  # Větší FPS pro hladší simulaci pohybu

folder = path.dirname(__file__)

# Konstanty pro barvu a šířku mantinelů
GREY = (100, 100, 100)
MANTINEL_WIDTH = 40 


# Inicializace Pygame
pygame.init()
pygame.mixer.init()

# Nastavení okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

ground  = pygame.image.load(path.join(folder, "dream_studio_background.png")).convert()
ground = pygame.transform.scale(ground, (WIDTH,HEIGHT))

# Třída Car
class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, "car1_spr.png")
        self.original_image = pygame.image.load(image_path).convert_alpha()# .convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 24) )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2([x, y])
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 0.5
        self.acceleration = 0.5
        self.braking = 0.1
        self.friction = 0.02
        self.max_speed = 5

    def update(self, dt, walls):
        previous_angle = self.angle
        # Ovládání auta
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.velocity -= (self.acceleration * dt * math.cos(math.radians(self.angle)),
                              self.acceleration * dt * math.sin(math.radians(self.angle)))
        elif keystate[pygame.K_DOWN]:
            self.velocity += (self.braking * dt * math.cos(math.radians(self.angle)),
                              self.braking * dt * math.sin(math.radians(self.angle)))
        if keystate[pygame.K_LEFT]:
            if self.velocity.length() > 0:  #otáčí jen pokud se pohybuje
                self.angle -= self.rotation_speed * self.velocity.length() * dt
        elif keystate[pygame.K_RIGHT]:
            if self.velocity.length() > 0:  #otáčí jen pokud se pohybuje
                self.angle += self.rotation_speed * self.velocity.length() * dt

        # Použítí tření
        movement_direction = math.atan2(-self.velocity.y, self.velocity.x) % (2 * math.pi)
        car_direction = math.radians(-self.angle) % (2 * math.pi)
        
        # Vypočet rozdílu úhlu a normalizace na rozsah [0, π]
        angle_difference = abs((car_direction - movement_direction + math.pi) % (2 * math.pi) - math.pi)
        self.angle_difference = angle_difference
        # výpočet tření založený na rozdílu úhlu (koeficient tření by měl být větší, když je rozdíl větší)
        max_additional_friction = 0.01
        friction_factor = (angle_difference / math.pi) * max_additional_friction
        friction_effect = self.friction + friction_factor
        self.velocity *= (1 - friction_effect)

        # aktualizace polohy
        self.position += self.velocity
        self.rect.center = self.position

        # omezení rychlosti !!
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # rotace
        delta_angle = self.angle - previous_angle
        #self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        #self.rect = self.image.get_rect(center=self.rect.center)
        # chybně:
        self.image = pygame.transform.rotozoom(self.image, -delta_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

        # ohraničení pohybu na obrazovce
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.centerx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.position.x = self.rect.centerx
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.centery
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.position.y = self.rect.centery

        hits = pygame.sprite.spritecollide(self, walls, False)
        if hits: 
            self.velocity = pygame.Vector2([i*j for i,j in zip(self.velocity, [-1.5, -1.5])]) 
        


# okraje:
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREY) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 

# Konstanty
MANTINEL_WIDTH = 10
GREY = (100, 100, 100)  # RGB barva šedé pro mantinely


# Skupina pro mantinely
walls = pygame.sprite.Group()

# přidání mantinelů do skupiny spritů
top_wall = Wall(0, 0, WIDTH, MANTINEL_WIDTH)
bottom_wall = Wall(0, HEIGHT - MANTINEL_WIDTH, WIDTH, MANTINEL_WIDTH)
left_wall = Wall(0, 0, MANTINEL_WIDTH, HEIGHT)
right_wall = Wall(WIDTH - MANTINEL_WIDTH, 0, MANTINEL_WIDTH, HEIGHT)
walls.add(top_wall, bottom_wall, left_wall, right_wall)


# cypočítejte střed obrazovky
center_x = WIDTH // 2
center_y = HEIGHT // 2

# nastavte rozměry ostrova z mantinelů
island_width = 300
island_height = 200

# yypočítejte počáteční pozici ostrova tak, aby byl ve středu obrazovky
island_start_x = center_x - island_width // 2
island_start_y = center_y - island_height // 2

# vytvořte mantinely pro ostrov
top_island_wall = Wall(island_start_x, island_start_y, island_width, MANTINEL_WIDTH)
bottom_island_wall = Wall(island_start_x, island_start_y + island_height - MANTINEL_WIDTH, island_width, MANTINEL_WIDTH)
left_island_wall = Wall(island_start_x, island_start_y, MANTINEL_WIDTH, island_height)
right_island_wall = Wall(island_start_x + island_width - MANTINEL_WIDTH, island_start_y, MANTINEL_WIDTH, island_height)

# přidejte mantinely ostrova do skupiny spritů
walls.add(top_island_wall, bottom_island_wall, left_island_wall, right_island_wall)



# Vytvoření skupiny spritů a přidání autíčka
my_sprites = pygame.sprite.Group()
car = Car(100, 100)
#car2 = Car(200, 100)
#car3 = Car(300, 100)
my_sprites.add(car, )

# Hlavní smyčka
running = True


# Hlavní smyčka
while running:
    # Delta time
    dt = clock.tick(FPS) / 10

    # Proces vstupů (eventy)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update - předejte 'walls' jako argument do metody 'update'
    my_sprites.update(dt, walls)  # Tady je opraveno


    # Vykreslení
    screen.fill(BLACK)
    screen.blit(ground, (0,0))
    walls.draw(screen)  # Vykreslete mantinely před autem
    my_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()

