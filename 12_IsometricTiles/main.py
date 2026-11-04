from __future__ import annotations
import os
import random
import sys
from pathlib import Path

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720          # rozlišení okna
TILE_WIDTH, TILE_HEIGHT = 80, 40              #  2:1 poměr
GRID_WIDTH, GRID_HEIGHT = 40, 40                 # rozměr mapy v dlaždicích
ORIGIN_Y = 60                                    # posun mapy dolů od horního okraje
ASSET_DIR = Path(__file__).with_name("roadTiles_v2") / "png"  # cesta k dlaždicím
BG_COLOR = (25, 25, 25)
FPS = 60


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric random map – drag to scroll")
clock = pygame.time.Clock()

#  LOAD TILES ──────────────────────────────

def load_tiles(directory: Path) -> list[pygame.Surface]:
    # nactení vsech png
    if not directory.exists():
        raise FileNotFoundError(f"{directory} not found – check ASSET_DIR path")

    tiles: list[pygame.Surface] = []
    for fname in sorted(directory.iterdir()):
        if fname.suffix.lower() == ".png":
            surf = pygame.image.load(fname).convert_alpha()  # convert → rychlejší blit
            tiles.append(surf)
    if not tiles:
        raise RuntimeError(f"No PNG tiles found in {directory}")
    return tiles

TILES = load_tiles(ASSET_DIR)
TILE_COUNT = len(TILES)
print(f"Loaded {TILE_COUNT} tiles from {ASSET_DIR}")

#  MAP GENERATION (RANDOM) ────────────────────────
random_map = [[random.randrange(TILE_COUNT) for _ in range(GRID_WIDTH)]
              for _ in range(GRID_HEIGHT)]

# ISOMETRIC HELPERS ──────────────────────────

def grid_to_iso(x: int, y: int) -> tuple[int, int]:
    # konverze gridu do diamant gridu pro isometric:
    screen_x = (x - y) * (TILE_WIDTH // 2)
    screen_y = (x + y) * (TILE_HEIGHT // 2)
    return screen_x, screen_y

# RENDERING ──────────────────────────────

def draw_map(offset_x: int, offset_y: int) -> None:
    # snaha kreslit i jen ty vyditelné
    half_w = TILE_WIDTH // 2
    max_h = max(tile.get_height() for tile in TILES)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = TILES[random_map[y][x]]
            iso_x, iso_y = grid_to_iso(x, y)
            draw_x = iso_x + offset_x + (SCREEN_WIDTH // 2) - half_w
            draw_y = iso_y + offset_y + ORIGIN_Y - (tile.get_height() - TILE_HEIGHT)

            # jednoduché ořezání mimo obrazovku (vylepší FPS u velké mapy)
            if draw_x < -tile.get_width() or draw_x > SCREEN_WIDTH + TILE_WIDTH:
                continue
            if draw_y < -max_h or draw_y > SCREEN_HEIGHT + max_h:
                continue

            screen.blit(tile, (draw_x, draw_y))

# GAME LOOP ──────────────────────────────

def main() -> None:
    offset_x = 0
    offset_y = 0
    dragging = False
    last_mouse = (0, 0)

    while True:
        # — event handling —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # LMB
                dragging = True
                last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx, dy = event.rel  # relativní pohyb myši od minulé události
                offset_x += dx
                offset_y += dy

        # — render —
        screen.fill(BG_COLOR)
        draw_map(offset_x, offset_y)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
