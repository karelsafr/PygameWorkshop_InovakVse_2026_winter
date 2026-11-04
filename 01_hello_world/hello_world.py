import pygame

pygame.init()
BLACK = (0,0,0)
PURPLE = (150, 10, 100)


screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ahoj svete!")
screen.fill(PURPLE)
clock = pygame.time.Clock()
myfont = pygame.font.Font(None, 50)



running = True

i = 1
# cyklus udrzujici okno v chodu
while running:
    # Event
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
    
    i+=1
    # Update
    textik = myfont.render(f"Ahoj Svete!{i}",True, (250,80,100))
    

    # Render
    screen.fill((0,0,0))
    screen.blit(textik,(0+i,0+i))
    

    pygame.display.update()
    clock.tick(60)
    



pygame.quit()
