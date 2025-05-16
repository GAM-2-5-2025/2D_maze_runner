# Uvozimo knjiznice
import pygame
import sys
import main
import os
import random  # Treba za generiranje labirinta i kretanje zombija

# Pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()

WIDTH, HEIGHT = 1366, 768
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2D maze runner - home')

#pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()

WIDTH, HEIGHT = 1366, 768
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2D maze runner - home')

# Fontovi
FONT = pygame.font.Font(None, 36) #Default

# Namjestanje buttona
buttons = [pygame.Rect(20, 20, 140, 50), pygame.Rect(180, 20, 140, 50)]
button_lables = ["Back", "Reset"]
button_colors = [main.RED, main.BLUE]

# Namjestanje labirinta
maze = []
brRedaka = 0
brStupaca = 0

# Učitavanje tekstura
gridSize = 64  # Veličina u pikselima jednog polja
wall = pygame.image.load(os.path.join(os.path.dirname(__file__), "wall.png")).convert_alpha()
jajko = pygame.image.load(os.path.join(os.path.dirname(__file__), "jajko.png")).convert_alpha()
zombi = pygame.image.load(os.path.join(os.path.dirname(__file__), "zombi.png")).convert_alpha()
floor = pygame.image.load(os.path.join(os.path.dirname(__file__), "floor.png")).convert_alpha()

# Mijenjanje veličina tekstura
wall = pygame.transform.scale(wall, (gridSize, gridSize))
floor = pygame.transform.scale(floor, (gridSize, gridSize))
jajko = pygame.transform.scale(jajko, (gridSize * 58/64, gridSize * 126/164))
zombi = pygame.transform.scale(zombi, (gridSize * 70/64, gridSize * 98/64))

# Stvaranje labirinta (0 su prazno, 1 su zidovi), zasad jos nije random generirano
def generateMaze(redak, stupac):
    global maze
    maze = [[0] * stupac] * redak

def draw():
    screen.fill(main.DARK_BLUE)
    
    # Crtanje labirinta
    for i in range(brRedaka):
        for j in range(brStupaca):
            screen.blit(wall, (100 + gridSize * j, 80 + gridSize * i)) if maze[i][j] == 1 else screen.blit(floor, (100 + gridSize * j, 80 + gridSize * i))

    # Crtanje buttona
    for i in range(len(buttons)):
        pygame.draw.rect(screen, button_colors[i], buttons[i])
        button_text = FONT.render(button_lables[i], True, main.WHITE)
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, text_rect)
        
    pygame.display.flip()


def main2(redak, stupac):
    global brRedaka
    global brStupaca
    brRedaka = redak
    brStupaca = stupac

    generateMaze(redak, stupac)
    
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(event.pos):
                        if(button_lables[i]=="Back"):
                            main.main()
                        elif(button_lables[i]=="Reset"):
                            main2(brRedaka,brStupaca)

            #Tipkanje u input boxove
            #if event.type == pygame.KEYDOWN:
        
        draw()
        clock.tick(30)
