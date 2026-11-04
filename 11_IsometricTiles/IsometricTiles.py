import pygame
import sys

# Inicializace Pygame
pygame.init()

# Parametry okna a dlaždic
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_WIDTH, TILE_HEIGHT = 64, 32  # Volitelná velikost dlaždic
GRID_WIDTH, GRID_HEIGHT = 10, 10  # Rozměry herní plochy (počet dlaždic)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometrická dlaždicová hra")

clock = pygame.time.Clock()

# Definice barev
GREEN = (50, 200, 50)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# Funkce pro převod mřížkových souřadnic (x, y) na isometrické souřadnice (screen_x, screen_y)
def grid_to_iso(x, y):
    screen_x = (x - y) * (TILE_WIDTH // 2) + SCREEN_WIDTH // 2
    screen_y = (x + y) * (TILE_HEIGHT // 2) + 50  # Posun dolů pro horní okraj
    return screen_x, screen_y


# Funkce pro vykreslení pozadí s isometrickými dlaždicemi
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            iso_x, iso_y = grid_to_iso(x, y)
            # Vypočítáme body pro vykreslení čtyřúhelníkové dlaždice
            points = [
                (iso_x, iso_y),
                (iso_x + TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2),
                (iso_x, iso_y + TILE_HEIGHT),
                (iso_x - TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2)
            ]
            pygame.draw.polygon(screen, GREEN, points)  # vyplněná dlaždice
            pygame.draw.polygon(screen, GRAY, points, 1)  # okraj dlaždice


# Startovní pozice hráče v mřížce
player_x, player_y = GRID_WIDTH // 2, GRID_HEIGHT // 2


# Funkce pro vykreslení hráče (jako jednoduchý kruh uprostřed dlaždice)
def draw_player(x, y):
    iso_x, iso_y = grid_to_iso(x, y)
    # Vypočítáme střed dlaždice, kde se hráč vykreslí
    center = (iso_x, iso_y + TILE_HEIGHT // 2)
    pygame.draw.circle(screen, RED, center, 10)


# Hlavní herní smyčka
running = True
while running:
    clock.tick(60)  # Horní limit 60 FPS, nikoli zaručená rychlost smyčky

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pohyb hráče pomocí šipek
    # Každý platný směr záměrně čeká 100 ms; při více směrech se čekání sčítají.
    # Během delay se nezpracovávají další události ani nekreslí další snímek.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= 1
            pygame.time.delay(100)  # Záměrné zpomalení tohoto platného kroku
    if keys[pygame.K_RIGHT]:
        if player_x < GRID_WIDTH - 1:
            player_x += 1
            pygame.time.delay(100)
    if keys[pygame.K_UP]:
        if player_y > 0:
            player_y -= 1
            pygame.time.delay(100)
    if keys[pygame.K_DOWN]:
        if player_y < GRID_HEIGHT - 1:
            player_y += 1
            pygame.time.delay(100)

    # Vyčištění obrazovky
    screen.fill(BLACK)

    # Vykreslení dlaždicového pozadí a hráče
    draw_grid()
    draw_player(player_x, player_y)

    pygame.display.flip()

pygame.quit()
sys.exit()
