# Uvozimo knjiznice
import pygame
import sys
import os
import random
import math
import copy
import main
import camera


# Pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()

WIDTH, HEIGHT = main.WIDTH, main.HEIGHT
screen = main.screen
pygame.display.set_caption('2D maze runner - home')

# Za pravilno skaliranje veličina
screen_WIDTH, screen_HEIGHT = screen.get_size()
camera = main.camera

# Fontovi
FONT = main.FONT

# Namjestanje buttona
buttons = [pygame.Rect(20, 20, 140, 50), pygame.Rect(180, 20, 140, 50)]
button_lables = ["Back", "Restart"]
button_colors = [main.RED, main.BLUE]
restart_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
home_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)

# Namjestanje labirinta
brRedaka = 5
brStupaca = 5
difficulty = 1   # Mijenja težinu labirinta i količiun zombija
state = "maze"   # Jesi li trenutni živ, mrtav, ili pobijedio
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
door_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "door.png")).convert_alpha()

# Mijenjanje veličina tekstura
floor_png = pygame.transform.scale(floor_png, (gridSize, gridSize))
zombie_png = pygame.transform.scale(zombie_png, (gridSize * 60/64, gridSize * 86/64))
player_png = pygame.transform.scale(player_png, (gridSize * 45/64, gridSize * 90/64))
door_png = pygame.transform.scale(door_png, (gridSize, gridSize))

# Namjestanje playera
player_Rect = pygame.Rect(0, 0, gridSize * 32 / 64, gridSize * 40 / 64) # Hitbox playera
player_Rect.center = (100 + gridSize * 1.5, 80 + gridSize * 1.5)
player_start = [pygame.Vector2(1,1), None, pygame.time.get_ticks(), player_Rect.copy()]
inputs = []
player = copy.deepcopy(player_start) # Player objekt (trenutna poz, trenutno micanje, vrijeme proslog micanja, input za smjer kretanja)

# Namjestanje zombija
zombies_Rect = pygame.Rect(0, 0, gridSize * 32 / 64, gridSize * 40 / 64) # Hitbox zombija
zombies = [] # Sprema poziciju svih zombija i podatke o trenutnom kretanju (animacija)
maze_zombies_start = [[]]
maze_zombies = [[]]
zombies_start = []

# Namjestanje izlaza (vrata)
door_pos = pygame.Vector2(4,4)
door_rect = pygame.Rect(0,0, gridSize * 32 / 64, gridSize * 32 / 64)
door_rect_center = (100 + 4.5 * gridSize, 80 + 4.5 * gridSize)

# Ostale postavke
start_delay = 2
input_delay_time = 0.05
death_messages = ["Umro si ):", "Umro si (:", "Skill issue", "Nastavi igrat mozda postanes bolji",
                  "Crknuo si", "Krcnuo si", "You've been hit by... You've been struck by... A ZOMBIE!"
                 ]
win_messages = ["Ti si tako dobar u ovoj igrici O:", "Ti si pravi maher za ovo (;",
                "Ovo je svetska razina gaminga!", "Bolji si u igranju od Ninje!",
                "Uspio si (:", "Uspjela si (;", "GG ez, jelda?", "Tko je najbolji? TI si majbolji!",
                "Ma, posrećilo ti se", "Prešao si igricu! Sada probaj još jednom, ali brže.",
                "Poštovani igraču, moje iskrene čestitke na prelasku ove igrice *gives you a handshake*",
                "Nije loše, nije loše... Može bolje, al nije loše...", "Iskreno, presporo si prešao.",
                "I, šta misliš o igrici? Jel dobra? ostavi neki dobar rejting pls uwu",
                "Braavoooo! Čestitke i pohvale!! (Nije kao da je super lagano, al' ok)",
                "Dobar posao :D", "Prešao si igricu. Sada si vrlo kul osoba :D",
                "Čestitke! Prešao si - oh, da, možda nisi Hrvat... Congratulations! You have beaten the game!",
                "Tako je! Pokaži tim zombijima tko je gazda!", "Zombie?? More like: Zom-bye bye (Kužiš jer si kao pobijedio i otišao ća pa kao govoriš bye bye)"
                ]


# Funkcija za nacrtat text u gumbu ili input boxu
def draw_text(text, rect, normal_color, hover_color, hover=False):
    color = hover_color if hover else normal_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = main.FONT.render(text, True, main.WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


# Stvaranje labirinta (0 su prazno, 1 su zidovi), zasad jos nije random generirano
def generateMaze(stupac, redak):
    global door_pos, door_rect

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

    # Pomoću DFS-a radimo rupe u zidovima
    while stack:
        x, y = stack[-1]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < redak and 0 < ny < stupac and maze[nx][ny] == 0:
                door_pos = pygame.Vector2(nx,ny)
                door_rect.center = (100 + (ny + 0.5) * gridSize, 80 + (nx + 0.5) * gridSize)
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
            zombies_pos.append([pygame.Vector2(x,y), None, pygame.time.get_ticks(), zombies_Rect.copy(), pygame.Vector2(-1,-1)]) # Stvoren novi zombi (pozicija, trenutno micanje, vrijeme_proslog_micanja, prosla_pozicija)
            zombies_pos[-1][3].center = (100 + (y + 0.5) * gridSize, 80 + (x + 0.5) * gridSize)
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
            screen.blit(walls_png[maze[i][j]], camera.apply(((100 + gridSize * j, 80 + gridSize * i)))) if maze[i][j] != -1 else screen.blit(floor_png, camera.apply((100 + gridSize * j, 80 + gridSize * i)))

    # Crtanje vrata
    screen.blit(door_png, camera.apply((100 + door_pos.y * gridSize, 80 + door_pos.x * gridSize)))
  
    # Crtanje objekata
    for entity in entities:
        screen.blit(entity[1], camera.apply((100 + gridSize * entity[0][0].y, 80 + gridSize * entity[0][0].x - 40)))

    # Crtanje hitboxova za debugging
    #for entity in entities:
    #    pygame.draw.rect(screen, (main.RED), entity[0][3])

    # Crtanje buttona
    for i in range(len(buttons)):
        pygame.draw.rect(screen, button_colors[i], buttons[i])
        button_text = FONT.render(button_lables[i], True, main.WHITE)
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, text_rect)

    pygame.display.flip()


# Resetiranje labirinta i svih gluposti
def restart():
    global player, zombies, maze_zombies, start_delay_active, start_time, state, inputs
    
    player = copy.deepcopy(player_start)
    zombies = copy.deepcopy(zombies_start)
    maze_zombies = copy.deepcopy(maze_zombies_start)
    start_delay_active = True
    start_time = pygame.time.get_ticks()
    state = "maze"
    inputs = []


# Funkcija za otvaranje UI-a za death screen  
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
        

# Funkcija za otvaranje UI-a za win screen
def win_screen(start_time):
    global clock, state

    state = "win"

    win_message = random.choice(win_messages)
    time_played = round((pygame.time.get_ticks() - start_time) / 1000, 2)
    time_message = "The time it took: " + str(time_played) + " seconds."
    
    while state == "win":
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

        # Vrijeme igranja
        time_played = main.FONT.render(time_message, True, main.WHITE)
        time_rect = time_played.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(time_played, time_rect)
        
        # Naslov
        title = main.FONT.render(win_message, True, main.WHITE)
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
    
    # Dimenzije moraju bit neparne za algoritam (jer nez drugi algoritam za labirint)
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
                            print("Back to home screen!")
                            restart()
                            return
                        elif(button_lables[i]=="Restart"):
                            restart()
                            print("Restart the game!")

            # Kretanje igrača tako da se tipke mogu držat, i ako je pritisnuto više tipka uzima se ona novija
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w: inputs.append(0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: inputs.append(1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: inputs.append(2)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: inputs.append(3)

                # Privremena tipka za ubit se
                elif event.key == pygame.K_k:
                    action = death_screen()
                    if(action == "restart"):
                        restart()
                        print("Restart the game!")
                    elif(action == "home"):
                        print("Back to home screen!")
                        restart()
                        return main.main()
                    
                # Privremena tipka za pobijedu
                elif event.key == pygame.K_j:
                    action = win_screen(start_time)
                    if(action == "restart"):
                        restart()
                        print("Restart the game!")
                    elif(action == "home"):
                        print("Back to home screen!")
                        restart()
                        return main.main()

            # Detekcija otpuštanja tipke da znamo ako se tipka drži
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and 0 in inputs: input_delay[0] = current_time
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and 1 in inputs: input_delay[1] = current_time
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and 2 in inputs: input_delay[2] = current_time
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and 3 in inputs: input_delay[3] = current_time

            # Mijenjanje veličine ekrana
            elif event.type == pygame.VIDEORESIZE:
                main.resize_screen(screen.get_size()[0], screen.get_size()[1], False)
            
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
                player[3].center = (100 + (player[0].y + 0.5) * gridSize, 80 + (player[0].x + 0.5) * gridSize)
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
                    zombie[3].center = (100 + (zombie[0].y + 0.5) * gridSize, 80 + (zombie[0].x + 0.5) * gridSize)
                except StopIteration:
                    zombie[1] = None

            # Provjera collisiona sa playerom
            if (zombie[1] or player[1]) and zombie[3].colliderect(player[3]):
                action = death_screen()
                if(action == "restart"):
                    restart()
                    print("Restart the game!")
                elif(action == "home"):
                    restart()
                    return

        # Provjera collisiona igrača i exita
        if (player[1]) and player[3].colliderect(door_rect):
            action = win_screen(start_time)
            if(action == "restart"):
                restart()
                print("Restart the game!")
            elif(action == "home"):
                restart()
                return
        draw()
        clock.tick(30)

    # Stanje je mrtvost pa biti pokrenuti UI za death_screen ooga booga
    
