# Uvozimo knjiznice
import pygame
import sys
import main
import os
import random  # Treba za generiranje labirinta i kretanje zombija
import math


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
brRedaka = 0
brStupaca = 0
difficulty = 1

# Namjestanje playera
player_start_pos = pygame.Vector2(1,1)
player_pos = player_start_pos
movement_dir = []
current_movement = None

# Učitavanje tekstura
gridSize = 64  # Veličina u pikselima jednog polja
walls = []
for i in range(0,16):
    file_path = "walls/" + str(i) + ".png"
    walls.append(pygame.image.load(file_path).convert_alpha())
    walls[i] = pygame.transform.scale(walls[i], (gridSize, gridSize))
#wall = pygame.image.load(os.path.join(os.path.dirname(__file__), "wall2.png")).convert_alpha()
player = pygame.image.load(os.path.join(os.path.dirname(__file__), "jajko.png")).convert_alpha()
zombi = pygame.image.load(os.path.join(os.path.dirname(__file__), "zombi.png")).convert_alpha()
floor = pygame.image.load(os.path.join(os.path.dirname(__file__), "floor2.png")).convert_alpha()

# Mijenjanje veličina tekstura
#wall = pygame.transform.scale(wall, (gridSize, gridSize))
floor = pygame.transform.scale(floor, (gridSize, gridSize))
player = pygame.transform.scale(player, (gridSize * 45/64, gridSize * 90/64))
zombi = pygame.transform.scale(zombi, (gridSize * 70/64, gridSize * 98/64))



# Stvaranje labirinta (0 su prazno, 1 su zidovi), zasad jos nije random generirano
def generateMaze(stupac, redak):

    # Namještavanje težine labirinta (koliko loopova ima u labirintu)
    extra_loops = 0
    
    if difficulty == 0:
        extra_loops = (stupac - 2) * (redak - 2) // 15
    elif difficulty == 1:
        extra_loops = (stupac - 2) * (redak - 2) // 30
    else:
        extra_loops = (stupac - 2) * (redak - 2) // 50
    
    # Start with all walls
    maze = [[0 for _ in range(stupac)] for _ in range(redak)]

    # Generacija labirinta
    start_x = 1
    start_y = 1
    stack = [(start_x, start_y)]
    maze[start_x][start_y] = -1

    while stack:
        x, y = stack[-1]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < redak and 0 < ny < stupac and maze[nx][ny] == 0:
                mx, my = x + dx // 2, y + dy // 2
                maze[mx][my] = -1
                maze[nx][ny] = -1
                stack.append((nx, ny))
                found = True
                break  # Only go one direction at a time like real DFS

        if not found:
            stack.pop()  # backtrack if no valid moves
    
    # Carefully remove walls to create loops
    removed = 0
    attempts = 0
    while removed < extra_loops and attempts < 2000:
        x = random.randrange(1, redak - 1)
        y = random.randrange(1, stupac - 1)

        if maze[x][y] == 0:
            # Must be between two paths (either vertical or horizontal)
            if (maze[x-1][y] == -1 and maze[x+1][y] == -1 and maze[x][y-1] == 0 and maze[x][y+1] == 0) or \
               (maze[x][y-1] == -1 and maze[x][y+1] == -1 and maze[x-1][y] == 0 and maze[x+1][y] == 0):
                maze[x][y] = -1
                removed += 1
        attempts += 1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    values = [1,2,4,8]

    for i in range(redak):
       for j in range(stupac):
           if maze[i][j] == -1: continue
           for k in range(4):
                x = i + directions[k][0]
                y = j + directions[k][1]
                if x >=0 and x < redak and y >= 0 and y < stupac and maze[x][y]!=-1:
                    maze[i][j] += values[k]
    
    return maze


# Za smooth kretanje
def ease_in_out(start_pos, end_pos, duration):
    
    frame_number = int(duration * 30)

    for i in range(frame_number):
       t = (i+1) / frame_number
       t = - (math.cos(math.pi * t) - 1) / 2
       yield start_pos.lerp(end_pos, t)

# Pomicanje igrača
def move_player():
    global current_movement
    
    directions = [
        pygame.Vector2(0,-1),
        pygame.Vector2(-1,0),
        pygame.Vector2(0,1),
        pygame.Vector2(1,0)
        ]
    for i in range(len(movement_dir)-1,-1,-1):
        direction = directions[movement_dir[i]]
        target_pos = (player_pos + direction)
        target_pos = pygame.Vector2(int(target_pos.x), int(target_pos.y))

        if(maze[int(target_pos.y)][int(target_pos.x)] == -1):
            current_movement = ease_in_out(player_pos.copy(), target_pos, 0.5)
            break

def draw():
    global maze
    global brRedaka
    global brStupaca
    
    screen.fill(main.DARK_BLUE)
    
    # Crtanje labirinta
    for i in range(brRedaka):
        for j in range(brStupaca):
            screen.blit(walls[maze[i][j]], (100 + gridSize * j, 80 + gridSize * i)) if maze[i][j] != -1 else screen.blit(floor, (100 + gridSize * j, 80 + gridSize * i))

    #Crtanje playera
    screen.blit(player, (100 + gridSize * player_pos.x, 80 + gridSize * player_pos.y - 40))
    
    # Crtanje buttona
    for i in range(len(buttons)):
        pygame.draw.rect(screen, button_colors[i], buttons[i])
        button_text = FONT.render(button_lables[i], True, main.WHITE)
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, text_rect)
        
    pygame.display.flip()


def main2(redak, stupac, active_difficulty):
    global brRedaka
    global brStupaca
    global maze
    global difficulty
    global current_movement
    global movement_dir
    global player_pos
    global player_start_pos
    
    last_move_time = -1000
    
    # Ensure dimensions are odd because it doesn't work otherwise (jer nez drugi algoritam za labi)
    if stupac % 2 == 0:
        stupac += 1
    if redak % 2 == 0:
        redak += 1
    
    brRedaka = redak
    brStupaca = stupac
    difficulty = active_difficulty

    maze = generateMaze(stupac, redak)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Provjera je li kliknut neki od gumba
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(event.pos):
                        if(button_lables[i]=="Back"):
                            player_pos = player_start_pos
                            main.main()
                        elif(button_lables[i]=="Reset"):
                            player_pos = player_start_pos
                            

            # Kretanje igrača tako da se tipke mogu držat, i ako je pritisnuto više tipka uzima se ona novija
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w: movement_dir.append(0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: movement_dir.append(1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: movement_dir.append(2)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: movement_dir.append(3)
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w: movement_dir.remove(0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: movement_dir.remove(1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: movement_dir.remove(2)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: movement_dir.remove(3)

        
        if movement_dir and (pygame.time.get_ticks() - last_move_time) / 1000 >= 0.5 + 0.2:
            last_move_time = pygame.time.get_ticks()
            move_player()

        if current_movement:
            try:
                player_pos = next(current_movement)
            except StopIteration:
                current_movement = None
        
        draw()
        clock.tick(30)
