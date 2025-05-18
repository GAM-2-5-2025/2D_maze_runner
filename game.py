# Uvozimo knjiznice
import pygame
import sys
import os
import random
import math
import copy
import main


# Pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()

WIDTH, HEIGHT = main.WIDTH, main.HEIGHT
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2D maze runner - home')


# Fontovi
FONT = pygame.font.Font(None, 36) #Default

# Namjestanje buttona
buttons = [pygame.Rect(20, 20, 140, 50), pygame.Rect(180, 20, 140, 50)]
button_lables = ["Back", "Reset"]
button_colors = [main.RED, main.BLUE]
restart_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
home_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)

# Namjestanje labirinta
brRedaka = 5
brStupaca = 5
difficulty = 1
state = "maze"
clock = None
start_delay_active = True
start_time = pygame.time.get_ticks()

# Učitavanje tekstura
gridSize = 64  # Veličina u pikselima jednog polja
walls_png = []
for i in range(0,16):
    file_path = "walls/" + str(i) + ".png"
    walls_png.append(pygame.image.load(file_path).convert_alpha())
    walls_png[i] = pygame.transform.scale(walls_png[i], (gridSize, gridSize))
zombie_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "zombi.png")).convert_alpha()
player_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "jajko.png")).convert_alpha()
floor_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "floor2.png")).convert_alpha()

# Mijenjanje veličina tekstura
floor_png = pygame.transform.scale(floor_png, (gridSize, gridSize))
zombie_png = pygame.transform.scale(zombie_png, (gridSize * 60/64, gridSize * 86/64))
player_png = pygame.transform.scale(player_png, (gridSize * 45/64, gridSize * 90/64))

# Namjestanje playera
player_start = [pygame.Vector2(1,1), None, pygame.time.get_ticks(), pygame.Rect(100, 80, gridSize, gridSize)]
inputs = []
player = player_start.copy() # Player objekt (trenutna poz, trenutno micanje, vrijeme proslog micanja, input za smjer kretanja)

# Namjestanje zombija
zombies = [] # Sprema poziciju svih zombija i podatke o trenutnom kretanju (animacija)
maze_zombies_start = [[]]
maze_zombies = [[]]
zombies_start = []

# Ostale postavke
start_delay = 2
input_delay_time = 0.2
death_messages = ["Umro si ):", "Umro si (:", "Skill issue", "Nastavi igrat mozda postanes bolji",
                  "Crknuo si", "Krcnuo si", "You've been hit by... You've been struck by... A ZOMBIE!"
                 ]
# Funkcija za nacrtat text i gumb ili input box
def draw_text(text, rect, normal_color, hover_color, hover=False):
    color = hover_color if hover else normal_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = main.FONT.render(text, True, main.WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


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


def spawn_zombies():
    global maze_zombies_start, maze_zombies

    zombies_pos = []
    maze_zombies_start = [[0 for _ in range(brStupaca)] for _ in range(brRedaka)]
    
    amount = 0
        
    if difficulty == 0:
        amount = (brStupaca - 2) * (brRedaka - 2) // 35
    elif difficulty == 1:
        amount = (brStupaca - 2) * (brRedaka - 2) // 25
    else:
        amount = (brStupaca - 2) * (brRedaka - 2) // 15

    added = 0
    attempts = 0
    while added < amount and attempts < 2000:
        x = random.randrange(1, brRedaka - 1)
        y = random.randrange(1, brStupaca - 1)

        if maze[x][y] == -1 and maze_zombies_start[x][y] == 0 and pygame.Vector2(x,y) != player_start[0]:
            added += 1
            zombies_pos.append([pygame.Vector2(x,y), None, pygame.time.get_ticks(), pygame.Rect(100 + gridSize * x, 80 + gridSize * y, gridSize, gridSize), pygame.Vector2(-1,-1)]) # Stvoren novi zombi (pozicija, trenutno micanje, vrijeme_proslog_micanja, prosla_pozicija)
            maze_zombies_start[x][y] = 1
        attempts += 1

    maze_zombies = copy.deepcopy(maze_zombies_start)
    return zombies_pos

# Za smooth kretanje
def ease_in_out(start_pos, end_pos, duration):
    
    frame_number = int(duration * 30)

    for i in range(frame_number):
       t = (i+1) / frame_number
       t = - (math.cos(math.pi * t) - 1) / 2
       yield start_pos.lerp(end_pos, t)

# Pomicanje igrača
def move_player():
    global player, inputs
    
    directions = [
        pygame.Vector2(-1,0),
        pygame.Vector2(0,-1),
        pygame.Vector2(1,0),
        pygame.Vector2(0,1)
        ]
    
    for i in range(len(inputs)-1,-1,-1):
        direction = directions[inputs[i]]
        target_pos = (player[0] + direction)

        if(maze[int(target_pos.x)][int(target_pos.y)] == -1):
            player[1] = ease_in_out(player[0].copy(), target_pos, 0.5)
            break


# Pomicanje zombija
def move_zombie(zombie):
    global zombies, maze_zombies 
    
    directions = [
        pygame.Vector2(-1,0),
        pygame.Vector2(0,-1),
        pygame.Vector2(1,0),
        pygame.Vector2(0,1)
        ]
    
    random.shuffle(directions)

    # Ovo je da zombi ne želi ić otkuda je već došao da ne ide naprijed nazad stalno
    non_prefered_dir = zombie[4] - zombie[0]
    if non_prefered_dir in directions:
        directions.remove(non_prefered_dir)
        directions.append(non_prefered_dir)
    
    for direction in directions:
        target_pos = zombie[0] + direction
        x = int(target_pos.x)
        y = int(target_pos.y)
        if(0 <= x < brRedaka and 0 <= y < brStupaca and maze[x][y] == -1 and maze_zombies[x][y] == 0):
            x2,y2 = int(zombie[0].x), int(zombie[0].y)
            maze_zombies[x][y] = 1
            maze_zombies[x2][y2] = 0
            zombie[1] = ease_in_out(zombie[0].copy(), target_pos, 0.5)
            zombie[4] = zombie[0].copy()
            break

    return zombie


# Crtanje stvari na screen
def draw():
    
    screen.fill(main.DARK_BLUE)

    # Stavljanje svih entityja u istu listu
    entities = []
    # Zombiji
    for zombie in zombies:
        entities.append((zombie, zombie_png, "Zombie"))
    # Player
    entities.append((player, player_png, "Player"))
    
    # Sortiranje da su pravilno posloženi jedan iza drugog zbog perspektive
    entities = sorted(entities, key = lambda entity: entity[0][0].x)
    
    # Crtanje labirinta
    for i in range(brRedaka):
        for j in range(brStupaca):
            screen.blit(walls_png[maze[i][j]], (100 + gridSize * j, 80 + gridSize * i)) if maze[i][j] != -1 else screen.blit(floor_png, (100 + gridSize * j, 80 + gridSize * i))

    # Crtanje objekata
    for entity in entities:
        screen.blit(entity[1], (100 + gridSize * entity[0][0].y, 80 + gridSize * entity[0][0].x - 40))
    
    # Crtanje buttona
    for i in range(len(buttons)):
        pygame.draw.rect(screen, button_colors[i], buttons[i])
        button_text = FONT.render(button_lables[i], True, main.WHITE)
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, text_rect)

    pygame.display.flip()


def restart():
    global player, zombies, maze_zombies, start_delay_active, start_time, state, inputs
    
    player = player_start.copy()
    zombies = copy.deepcopy(zombies_start)
    maze_zombies = copy.deepcopy(maze_zombies_start)
    start_delay_active = True
    start_time = pygame.time.get_ticks()
    state = "maze"
    inputs = []

    
def death_screen():
    global clock, state

    state = "dead"

    death_message = random.choice(death_messages)
    
    while state == "dead":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if restart_btn.collidepoint(mouse_pos):
                    print("Restart the game!")
                    return "restart"
                if home_btn.collidepoint(mouse_pos):
                    print("Back to home screen!")
                    return "home"
            
        # Prozirna pozadina
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 60))
        screen.blit(overlay, (0,0))

        # Naslov
        title = main.FONT.render(death_message, True, main.WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, title_rect)

        # Gumbići
        mouse_pos = pygame.mouse.get_pos()
        draw_text("Restart", restart_btn, (51, 153, 255), (0, 102, 204), restart_btn.collidepoint(mouse_pos))
        draw_text("Back to home", home_btn, (255, 51, 51), (204, 0, 0), home_btn.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(30)


def main2(redak, stupac, active_difficulty):
    global brRedaka, brStupaca, difficulty
    global maze, start_time, start_delay_active
    global player, zombies, zombies_start, maze_zombies, inputs, state
    global clock
    
    # Ensure dimensions are odd because it doesn't work otherwise (jer nez drugi algoritam za labi)
    if stupac % 2 == 0:
        stupac += 1
    if redak % 2 == 0:
        redak += 1
    
    brRedaka = redak
    brStupaca = stupac
    difficulty = active_difficulty

    # Generiranje labirinta i stvaranje zombija
    maze = generateMaze(stupac, redak)
    zombies_start = spawn_zombies()
    zombies = copy.deepcopy(zombies_start)

    # Delay da kad se krećeš i pustiš strelicu još uvijek detektira malo da ju držiš, sprema vrijeme otpuštanja tipke
    input_delay = [None for _ in range(4)]
    start_delay_active = True
    start_time = pygame.time.get_ticks()
    
    clock = pygame.time.Clock()
    
    while state == "maze":
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Provjera je li kliknut neki od gumba
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(event.pos):
                        if(button_lables[i]=="Back"):
                            return
                        elif(button_lables[i]=="Reset"):
                            player = player_start.copy()
                            zombies = copy.deepcopy(zombies_start)
                            maze_zombies = copy.deepcopy(maze_zombies_start)
                            start_delay_active = True
                            start_time = current_time
                            

            # Kretanje igrača tako da se tipke mogu držat, i ako je pritisnuto više tipka uzima se ona novija
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w: inputs.append(0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: inputs.append(1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: inputs.append(2)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: inputs.append(3)
                elif event.key == pygame.K_k:
                    action = death_screen()
                    if(action == "restart"):
                        restart()
                    elif(action == "home"):
                        return main.main()

            # Detekcija otpuštanja tipke da znamo ako se tipka drži
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w: input_delay[0] = current_time
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: input_delay[1] = current_time
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: input_delay[2] = current_time
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: input_delay[3] = current_time

        # Uračunava input delay u otpuštanje tipke
        for i,last in enumerate(input_delay):
            if last != None:
                if (current_time - last) / 1000 >= input_delay_time:
                    input_delay[i] = None
                    inputs.remove(i)
        
        # Provjera moze li se igrač kretati
        if inputs and start_delay_active:
                if (current_time - start_time) / 1000 >= start_delay:
                    player[2] = current_time
                    move_player()
                    start_delay_active = False
        elif inputs and (current_time - player[2]) / 1000 >= 0.5 + 0.1:
            player[2] = current_time
            move_player()

        # Smooth animacije, provjerava ako se igrac jos krece i namjesta novu poziciju
        if player[1]:
            try:
                player[0] = next(player[1])
                player[3].x = 100 + player[0].x * gridSize
                player[3].y = 80 + player[0].y * gridSize
            except StopIteration:
                player[1] = None

        # Provjera mogu li se zombiji kretati i smooth kretanje te PROVJERA COLLISIONA sa playerom
        for i,zombie in enumerate(zombies):
            
            # Provjera kad su se prošli put kretali i dal mogu sad
            if start_delay_active:
                if (current_time - start_time) / 1000 >= start_delay:
                    zombie[2] = current_time
                    zombie = move_zombie(zombie)
                    start_delay_active = False
            elif (current_time - zombie[2]) / 1000 >= 0.5 + 0.7:
                zombie[2] = current_time
                zombie = move_zombie(zombie)

            # Ako se kreću postavlja poziciju na željeno mjesto za smooth animacije
            if zombie[1]:
                try:
                    zombie[0] = next(zombie[1])
                    zombie[3].x = 100 + zombie[0].x * gridSize
                    zombie[3].y = 80 + zombie[0].y * gridSize
                except StopIteration:
                    zombie[1] = None

            # Provjera collisiona sa playerom
            if (zombie[1] or player[1]) and zombie[3].colliderect(player[3]):
                action = death_screen()
                if(action == "restart"):
                    restart()
                elif(action == "home"):
                    return
        
        draw()
        clock.tick(30)

    # Stanje je mrtvost pa biti pokrenuti UI za death_screen ooga booga
    
