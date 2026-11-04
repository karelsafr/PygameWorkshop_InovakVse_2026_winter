import pygame

# inicializace pygame
pygame.init()

# velikost okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Posouvání mapy s dlaždicemi")

# barvy
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# hráč (kulička)
player_radius = 10
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5.0

# velikost mapy (větší než obrazovka)
MAP_WIDTH = 2600
MAP_HEIGHT = 2200

# posun obrazovky (počáteční hodnoty)
camera_x = 0
camera_y = 0

# Hlavní smyčka
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Získání vstupu od uživatele
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_speed >= player_radius:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_speed <= MAP_WIDTH - player_radius:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y - player_speed >= player_radius:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + player_speed <= MAP_HEIGHT - player_radius:
        player_y += player_speed

    # Kamera sleduje hráče a zastaví se na hranicích mapy
    camera_x = max(0, min(player_x - WIDTH // 2, MAP_WIDTH - WIDTH))
    camera_y = max(0, min(player_y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))

    # vymazání obrazovky
    screen.fill(WHITE)

    # vykreslení jednoduché dlaždicové mapy (pro ukázku)
    for x in range(0, MAP_WIDTH, 100):
        for y in range(0, MAP_HEIGHT, 100):
            pygame.draw.rect(screen, GREEN, (x - camera_x, y - camera_y, 100, 100), 1)

    # vykreslení hráče
    pygame.draw.circle(screen, RED, (player_x - camera_x, player_y - camera_y), player_radius)

    # aktualizace obrazovky
    pygame.display.flip()
    clock.tick(60)

# ukončení pygame
pygame.quit()
