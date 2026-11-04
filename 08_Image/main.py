import sys
import random
from pathlib import Path

import pygame

# CONFIG

SCREEN_W, SCREEN_H = 800, 600
FPS = 60
ASSETS_PATH = Path(__file__).parent

# velikost jedné tile:
TILE_W, TILE_H = 75, 50


# RESOURCE CACHE
# small helper:
class ResourceCache:
    _images: dict[str, pygame.Surface] = {}
    _sheets: dict[str, list[pygame.Surface]] = {}

    @classmethod
    def image(cls, filename: str, colorkey=None) -> pygame.Surface:
        if filename not in cls._images:
            full_path = ASSETS_PATH / filename
            img = pygame.image.load(full_path).convert_alpha()
            if colorkey is not None:
                img.set_colorkey(colorkey)
            cls._images[filename] = img
        return cls._images[filename]

    @classmethod
    def sheet(cls, filename: str, tile_w: int, tile_h: int) -> list[pygame.Surface]:
        key = f"{filename}:{tile_w}x{tile_h}"
        if key not in cls._sheets:
            sheet_img = cls.image(filename)
            w, h = sheet_img.get_size()
            cols, rows = w // tile_w, h // tile_h
            frames = [sheet_img.subsurface(pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h))
                      for y in range(rows) for x in range(cols)]
            cls._sheets[key] = frames
        return cls._sheets[key]

# SPRITES:
class MovingSprite(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, pos: tuple[int, int], velocity: tuple[int, int], layer: int = 0):
        super().__init__()
        self.image = image  # shared surface
        self.rect = self.image.get_rect(center=pos)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx, self.vy = velocity
        self._layer = layer  # for LayeredUpdates

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (round(self.x), round(self.y))

        # Bounce on window borders
        hit_x = self.rect.left < 0 or self.rect.right > SCREEN_W
        hit_y = self.rect.top < 0 or self.rect.bottom > SCREEN_H
        if hit_x:
            self.vx = -self.vx
        if hit_y:
            self.vy = -self.vy
        if hit_x or hit_y:
            self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_W, SCREEN_H))
            if hit_x:
                self.x = float(self.rect.x)
            if hit_y:
                self.y = float(self.rect.y)


def tint(surface: pygame.Surface, color: tuple[int, int, int]) -> pygame.Surface:
    copy = surface.copy()
    copy.fill(color, special_flags=pygame.BLEND_MULT)
    return copy

# herní smyčka:
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Sprites, sheets & cache demo")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.LayeredUpdates()


a_img = ResourceCache.image("A.png")
b_img = ResourceCache.image("B.png")

for _ in range(15):
    pos = random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)
    vel = random.choice([-80, 80]), random.choice([-80, 80])
    all_sprites.add(MovingSprite(a_img, pos, vel, layer=2))

for _ in range(15):
    pos = random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)
    vel = random.choice([-60, 60]), random.choice([-60, 60])
    all_sprites.add(MovingSprite(b_img, pos, vel, layer=2))


if "B_red" not in ResourceCache._images:
    ResourceCache._images["B_red"] = tint(b_img, (255, 100, 100))
red_b_img = ResourceCache.image("B_red")
all_sprites.add(MovingSprite(red_b_img, (SCREEN_W // 2, SCREEN_H // 2), (0, 0), layer=3))

# sprite sheet:
frames = ResourceCache.sheet("sprite_sheet.png", TILE_W, TILE_H)  # length 4
colors = [(200, 200, 200), (200, 0, 0), (0, 200, 0), (0, 0, 200)]
for idx, frame in enumerate(frames):
    # each frame gets unique velocity and layer, but they all share the *same* parent surface memory
    vel = (random.choice([-100, 100]), random.choice([-100, 100]))
    all_sprites.add(MovingSprite(frame, (random.randrange(100, SCREEN_W-100), random.randrange(100, SCREEN_H-100)), vel, layer=1))

# pozadí:
background = pygame.Surface((SCREEN_W, SCREEN_H))
background.fill((30, 30, 30))
all_sprites.add(MovingSprite(background, (SCREEN_W//2, SCREEN_H//2), (0, 0), layer=0))

# GAME LOOP

running = True
while running:
    dt = clock.tick(FPS) / 1000

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # UPDATE
    all_sprites.update(dt)

    # RENDER
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
