
import pygame, sys, os
from pathlib import Path


BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600
FPS = 60

SPRITE_SHEET = Path(__file__).with_name("animace.png")
FRAME_COUNT = 6
ANIM_FPS = 8                     # FPS animace


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gift Explosion Demo – press ENTER")
clock = pygame.time.Clock()


class Gift(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        cls = self.__class__
        if not hasattr(cls, "frames"):
            sheet = pygame.image.load(SPRITE_SHEET).convert_alpha()
            w, h = sheet.get_size()
            frame_w = w // FRAME_COUNT
            cls.frames = [sheet.subsurface(x * frame_w, 0, frame_w, h) for x in range(FRAME_COUNT)]
        # initial state
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.anim_index = 0
        self.timer = 0.0
        self.exploding = False
        self.frame_duration = 1 / ANIM_FPS

    def explode(self):
        if not self.exploding:
            self.exploding = True
            self.anim_index = 0
            self.image = self.frames[0]
            self.timer = 0.0

    def update(self, dt):
        if self.exploding:
            self.timer += dt
            while self.exploding and self.timer >= self.frame_duration:
                self.timer -= self.frame_duration
                self.anim_index += 1
                if self.anim_index >= FRAME_COUNT:
                    # keep last frame visible; stop animation
                    self.anim_index = FRAME_COUNT - 1
                    self.exploding = False
                self.image = self.frames[self.anim_index]


all_sprites = pygame.sprite.Group()
gift = Gift((WIDTH // 2, HEIGHT // 2 + 100))
all_sprites.add(gift)

# ────────── HERNÍ SMYČKA ──────────
running = True
while running:
    dt = clock.tick(FPS) / 1000  # delta‑time v sekundách

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            gift.explode()

    all_sprites.update(dt)

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
