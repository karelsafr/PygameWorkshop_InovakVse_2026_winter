import pygame, random, sys

pygame.init()
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (220, 30, 30)
BG = (30, 30, 30)

ROWS, COLS = 10, 10
BOMBS = 15
TILE = 40
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miny – jednoduchá verze bez obrázků")

font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# -----------------------------
# Pomocné funkce
# -----------------------------

def generate_board():
    """Vytvoří hrací desku a rozmístí miny."""
    board = [[{"bomb": False, "revealed": False, "flag": False, "adj": 0} for _ in range(COLS)] for _ in range(ROWS)]
    placed = 0
    while placed < BOMBS:
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        if not board[r][c]["bomb"]:
            board[r][c]["bomb"] = True
            placed += 1
    # spočítat sousední miny
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c]["bomb"]:
                continue
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc]["bomb"]:
                        count += 1
            board[r][c]["adj"] = count
    return board


def flood_fill(r, c):
    """Pomocí zásobníku odhalí bezpečné pole a z prázdných polí pokračuje k sousedům."""
    stack = [(r, c)]
    while stack:
        r, c = stack.pop()
        cell = board[r][c]
        if cell["revealed"] or cell["flag"]:
            continue
        cell["revealed"] = True
        if cell["adj"] == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if not board[nr][nc]["revealed"]:
                            stack.append((nr, nc))


def reveal(r, c):
    global game_over
    cell = board[r][c]
    if cell["flag"] or cell["revealed"]:
        return
    if cell["bomb"]:
        cell["revealed"] = True
        game_over = True
    else:
        flood_fill(r, c)


def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]
            if not cell["bomb"] and not cell["revealed"]:
                return False
    return True


# -----------------------------
# Herní cyklus
# -----------------------------

board = generate_board()
game_over = False
win = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not win:
            mx, my = event.pos
            col = mx // TILE
            row = my // TILE
            if 0 <= row < ROWS and 0 <= col < COLS:
                if event.button == 1:  # levé tlačítko – odhal
                    reveal(row, col)
                    if not game_over:
                        win = check_win()
                elif event.button == 3:  # pravé tlačítko – vlajka
                    cell = board[row][col]
                    if not cell["revealed"]:
                        cell["flag"] = not cell["flag"]

    # -------------------------
    # Render
    # -------------------------
    screen.fill(BG)

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * TILE, r * TILE, TILE - 1, TILE - 1)
            cell = board[r][c]

            if cell["revealed"]:
                pygame.draw.rect(screen, LIGHT_GRAY, rect)
                if cell["bomb"]:
                    pygame.draw.circle(screen, RED, rect.center, TILE // 4)
                elif cell["adj"] > 0:
                    text = font.render(str(cell["adj"]), True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if cell["flag"]:
                    text = font.render("F", True, RED)
                    screen.blit(text, text.get_rect(center=rect.center))

    if game_over or win:
        msg = "Vyhrál jsi! :-)" if win else "Game Over!"
        overlay = big_font.render(msg, True, WHITE)
        screen.blit(overlay, overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()