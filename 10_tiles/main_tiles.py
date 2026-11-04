import pygame
from pathlib import Path
pygame.init()

# sastavení obrazovky
screen_width = 320
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# načtení sprite sheetu
sprite_sheet_path = Path(__file__).with_name("DungeonCrawl_ProjectUtumnoTileset_0.png")
sprite_sheet = pygame.image.load(sprite_sheet_path)
tile_size = 32  # Předpokládejme, že všechny dlaždice mají velikost 32x32 pixelů

# funkce pro vystřihnutí konkrétní dlaždice z sprite sheetu
# x a y jsou indexy sloupce a řádku od nuly, násobením získáme pixely
def get_tile(x, y):
    return sprite_sheet.subsurface(x * tile_size, y * tile_size, tile_size, tile_size)

# vystřihnutí trávy (1,13), vody (19,19) a pouště (19,13)
# souřadnice jsou (sloupec, řádek) v atlasu
grass_tile = get_tile(1, 13)
water_tile = get_tile(19, 19)
desert_tile = get_tile(19, 13)

# definice mapy dlaždic (0 = tráva, 1 = voda, 2 = poušť)
tile_map = [
    [2, 2, 2, 0, 0, 0, 1, 1, 0, 0],
    [2, 2, 2, 0, 0, 1, 1, 0, 0, 2],
    [2, 2, 0, 0, 1, 1, 1, 0, 0, 2],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 2],
    [0, 0, 1, 1, 1, 1, 0, 0, 2, 2],
    [0, 0, 1, 1, 1, 1, 0, 0, 2, 2],
    [0, 1, 1, 1, 1, 1, 0, 0, 2, 2],
    [0, 1, 1, 1, 1, 1, 0, 0, 2, 2],
    [1, 1, 1, 1, 1, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 1, 0, 0, 0, 2, 2]
]

# Funkce pro vykreslení mapy
def draw_map():
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == 0:
                screen.blit(grass_tile, (x * tile_size, y * tile_size))
            elif tile == 1:
                screen.blit(water_tile, (x * tile_size, y * tile_size))
            elif tile == 2:
                screen.blit(desert_tile, (x * tile_size, y * tile_size))

# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
