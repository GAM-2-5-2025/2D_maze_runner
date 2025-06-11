# Uvozimo knjiznice
import pygame
import sys
import os
import random
import math
import copy
import main
import camera
from entities import *
from collections import deque


# Pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = main.WIDTH, main.HEIGHT
screen = main.screen
pygame.display.set_caption('2D maze runner - home')

# Za pravilno skaliranje veličina
screen_WIDTH, screen_HEIGHT = screen.get_size()
camera = main.camera

FPS = main.FPS

# Fontovi
FONT = main.FONT
FONT2 = main.FONT2

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

directions = [pygame.Vector2(0, -1),
              pygame.Vector2(-1, 0),
              pygame.Vector2(0, 1),
              pygame.Vector2(1, 0)
              ]

# Učitavanje tekstura
gridSize = 190  # Veličina u pikselima jednog polja

walls_png = []
for i in range(0,16):
    file_path = "walls/" + str(i) + ".png"
    walls_png.append(pygame.image.load(file_path).convert_alpha())
    walls_png[i] = pygame.transform.scale(walls_png[i], (gridSize, gridSize))
    
zombie_png = [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\NAZAD.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\LIJEVO.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\NAPRIJED.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\DESNO.png")).convert_alpha()
    ]

smarter_png = [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\SMARTER_U.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\SMARTER_L.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\SMARTER_D.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\SMARTER_R.png")).convert_alpha()
    ]
brain_png = [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\BRAIN_U.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\BRAIN_L.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\BRAIN_D.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\BRAIN_R.png")).convert_alpha()
    ]

player_png = [
    [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_U1.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_U2.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_U3.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_U4.png")).convert_alpha()
    ],
    [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_L1.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_L2.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_L3.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_L4.png")).convert_alpha()
    ],
    [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_D1.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_D2.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_D3.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_D4.png")).convert_alpha()
    ],
    [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_R1.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_R2.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_R3.png")).convert_alpha(),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "idle\\JAJKO_R4.png")).convert_alpha()
    ]
    ]

floor_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "floor2.png")).convert_alpha()
door_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "door.png")).convert_alpha()
no_zombies_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "no_zombies.png")).convert_alpha()
no_zombies2_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "no_zombies2.png")).convert_alpha()
punch_png = pygame.image.load(os.path.join(os.path.dirname(__file__), "Punch.png")).convert_alpha()


# Mijenjanje veličina tekstura
floor_png = pygame.transform.scale(floor_png, (gridSize, gridSize))
for i in range(len(zombie_png)): zombie_png[i] = pygame.transform.scale(zombie_png[i], (gridSize * 64/64, gridSize * 90/64))
for i in range(len(smarter_png)): smarter_png[i] = pygame.transform.scale(smarter_png[i], (gridSize * 64/64, gridSize * 90/64))
for i in range(len(brain_png)): brain_png[i] = pygame.transform.scale(brain_png[i], (gridSize * 64/64, gridSize * 90/64))
for i in range(4):
    for j in range(4): player_png[i][j] = pygame.transform.scale(player_png[i][j], (gridSize * 88/64, gridSize * 124/64))
door_png = pygame.transform.scale(door_png, (gridSize, gridSize))
punch_png = pygame.transform.scale(punch_png, (gridSize, gridSize))
no_zombies_png = pygame.transform.scale(no_zombies_png, (gridSize * 74/64, gridSize * 128/64))
no_zombies2_png = pygame.transform.scale(no_zombies2_png, (gridSize * 106/64, gridSize * 128/64))


# Namjestanje playera
player_start = Player(pygame.Vector2(1,1), gridSize * 32 / 64, gridSize * 40 / 64, [1, 1, 0, 0], player_png)
player = player_start.copy()

# Namjestanje zombija
zombies_start = []
zombies = []
maze_zombies = [[]]

# Namjestanje kamere
cam_tl = pygame.Vector2(50, 100)
cam_w = pygame.Vector2(1260, 900)
cam_size = pygame.Vector2(7,5)
cam_despos = pygame.Vector2(1,1)
cam_pos = pygame.Vector2(4,4)

# Namjestanje izlaza (vrata)
door_pos = pygame.Vector2(4,4)
door_rect = pygame.Rect(0,0, gridSize * 32 / 64, gridSize * 32 / 64)
door_rect_center = (4.5 * gridSize, 4.5 * gridSize)

# Player WALLPUNCH
wallpunch_empty = pygame.Rect(1850, 100, 50, 600)
last_wallpunch = -settings.wallpunch_time * 1000
punch_active = False


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

def bfs(start, end):
    q = deque()
    q.append((start, -1))
    
    bio = []
    for i in range(0, brRedaka):
        bio.append([])
        for j in range(0,brStupaca):
            bio[i].append(0)

    bio[int(start.y)][int(start.x)] = 1

    while q:
        pos, temp = q.popleft()
        r,s = int(pos.y), int(pos.x)

        if(pos == end):
            return temp
        
        for j,i in enumerate(directions):
            x = int(r + i.y)
            y = int(s + i.x)
            if (0 <= x < brRedaka and 0 <= y < brStupaca):
                if maze[x][y] == -1 and bio[x][y] == 0:
                    bio[x][y] = 1
                    if temp == -1:
                        q.append((pygame.Vector2(y,x), j))
                    else:
                        q.append((pygame.Vector2(y,x), temp))

    return -1
        


# Stvaranje labirinta (0 su prazno, 1 su zidovi), zasad jos nije random generirano
def generateMaze(stupac, redak):
    global door_pos, door_rect

    # Namještavanje težine labirinta (koliko loopova ima u labirintu, no zombie zona...)
    extra_loops = (stupac - 2) * (redak - 2) // settings.maze_simpleness[difficulty]
    safezone_chance = settings.maze_safezone_chance[difficulty]
    
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
                door_rect.center = ((ny + 0.5) * gridSize, (nx + 0.5) * gridSize)
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
    while removed < extra_loops and attempts < 5000:
        x = random.randrange(1, redak - 1)
        y = random.randrange(1, stupac - 1)

        if maze[x][y] == 0:
            # Must be between two paths (either vertical or horizontal)
            if (maze[x-1][y] == -1 and maze[x+1][y] == -1 and maze[x][y-1] >= 0 and maze[x][y+1] >= 0):
                maze[x][y] = -3
                removed += 1
            elif (maze[x][y-1] == -1 and maze[x][y+1] == -1 and maze[x-1][y] >= 0 and maze[x+1][y] >= 0):
                maze[x][y] = -2
                removed += 1

            if maze[x][y] <= -2 and random.random() > safezone_chance:
                maze[x][y] = -1
            
                
        attempts += 1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    values = [1,2,4,8]

    for i in range(redak):
       for j in range(stupac):
           if maze[i][j] < 0: continue
           for k in range(4):
                x = i + directions[k][0]
                y = j + directions[k][1]
                if x >=0 and x < redak and y >= 0 and y < stupac and maze[x][y]>=0:
                    maze[i][j] += values[k]

    return maze


def spawn_zombies():
    global maze_zombies_start, maze_zombies

    zombies2 = []
    maze_zombies_start = [[0 for _ in range(brStupaca)] for _ in range(brRedaka)]
    smarter_chance = settings.smarter_chance[difficulty]
    brain_chance = settings.brain_chance[difficulty]
    
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

        if maze[x][y] == -1 and maze_zombies_start[x][y] == 0 and min(abs(x - player.pos.y), abs(y - player.pos.x)) > 1:
            added += 1
            rand = random.random()
            if rand <= smarter_chance:
                zombies2.append(Smarter(pygame.Vector2(y,x), gridSize * 32 / 64, gridSize * 40 / 64, [0, 0, 0, 0], smarter_png)) # Stvoren novi zombi (pozicija, hitbox height i width, sta je oko njega)
            elif rand <= smarter_chance + brain_chance:
                zombies2.append(Brain(pygame.Vector2(y,x), gridSize * 32 / 64, gridSize * 40 / 64, brain_png)) # Stvoren novi zombi (pozicija, hitbox height i width, sta je oko njega)
            else:
                zombies2.append(Zombie(pygame.Vector2(y,x), gridSize * 32 / 64, gridSize * 40 / 64, [0, 0, 0, 0], zombie_png)) # Stvoren novi zombi (pozicija, hitbox height i width, sta je oko njega)
            zombies2[-1].rect = pygame.Rect(gridSize * zombies2[-1].pos.x + x, gridSize * zombies2[-1].pos.y + y, zombies2[-1].width, zombies2[-1].height)
            maze_zombies_start[x][y] = 1
        attempts += 1

    maze_zombies = copy.deepcopy(maze_zombies_start)
    return zombies2

# Za smooth kretanje
def ease_in_out(start_pos, end_pos, duration):
    
    frame_number = int(duration * FPS)

    for i in range(frame_number):
       t = (i+1) / frame_number
       t = - (math.cos(math.pi * t) - 1) / 2
       yield start_pos.lerp(end_pos, t)


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
            zombie[1] = ease_in_out(zombie[0].copy(), target_pos, zombie[5])
            zombie[4] = zombie[0].copy()
            zombie[5] = zombie[5] - settings.zombie_acceleration
            break

    return zombie


# Crtanje stvari na screen
def draw():
    global zombies
    
    screen.fill(main.DARK_BLUE)

    # Stavljanje svih entityja u istu listu
    entities = []

    for i in zombies: entities.append(i)
    entities.append(player)
    
    # Sortiranje da su pravilno posloženi jedan iza drugog zbog perspektive
    entities = sorted(entities, key = lambda entity: entity.pos.y)

    game_w = pygame.Surface(((cam_size.x + 1) * gridSize, (cam_size.y + 1) * gridSize))
    
    # Crtanje labirinta
    ystart,yend = round(cam_pos.y) - (int(cam_size.y) + 1) // 2, round(cam_pos.y) + (int(cam_size.y) + 1) // 2
    xstart, xend = round(cam_pos.x) - (int(cam_size.x) + 1) // 2, round(cam_pos.x) + (int(cam_size.x) + 1) // 2
    
    for i in range(ystart, yend):
        for j in range(xstart, xend):
            if(i < 0 or i >= brRedaka or j < 0 or j >= brStupaca): continue
            if maze[i][j] >= 0: game_w.blit(walls_png[maze[i][j]], ((gridSize * (j - xstart), gridSize * (i - ystart))))
            else: game_w.blit(floor_png, (gridSize * (j - xstart), gridSize * (i- ystart)))

    # Crtanje prepreka
    for i in range(brRedaka):
        for j in range(brStupaca):
            if maze[i][j] == -2: game_w.blit(no_zombies_png, (gridSize * (j- xstart), gridSize * (i- ystart) - 60 / 64 * gridSize))
            elif maze[i][j] == -3: game_w.blit(no_zombies2_png, (gridSize * (j - xstart) - 21 / 64 * gridSize, gridSize * (i - ystart) - 60 / 64 * gridSize))

    # Crtanje vrata
    game_w.blit(door_png, ((door_pos.y - xstart) * gridSize, (door_pos.x - ystart) * gridSize))
  
    # Crtanje entitija
    for entity in entities:
        if isinstance(entity, Player):
            game_w.blit(entity.skin, (gridSize * (entity.pos.x - xstart) - 18 / 64 * gridSize, gridSize * (entity.pos.y - ystart) - 64 / 64 * gridSize))
        else:
            game_w.blit(entity.skin, (gridSize * (entity.pos.x - xstart), gridSize * (entity.pos.y - ystart) - 40 / 64 * gridSize))

    # Crtanje hitboxova za debugging
    """for zombie in zombies:
        pygame.draw.rect(game_w, (main.RED), zombie.rect.move(-xstart * gridSize, -ystart * gridSize))
    pygame.draw.rect(game_w, (main.RED), player.rect.move(-xstart * gridSize, -ystart * gridSize))
    """

    # Crtanje buttona
    for i in range(len(buttons)):
        pygame.draw.rect(screen, button_colors[i], camera.apply(buttons[i]))
        button_text = FONT.render(button_lables[i], True, main.WHITE)
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, camera.apply(text_rect))

    # Timer
    time = round((pygame.time.get_ticks() - start_time) / 1000, 2)
    time_m = time // 60
    time_s = round(time - time_m * 60,2)
    m = str(time_m)
    s = str(time_s)
    if s[-1] == ".": s += "00"
    elif s[-2] == ".": s += "0"
    if s[0] == ".": s = "00" + s
    elif s[1] == ".": s = "0" + s
    text = ""
    
    if(time_m != 0):
        text = FONT2.render(m + ":" + s, True, (255, 255, 255))
    else:
        text = FONT2.render(s, True, (255, 255, 255))

    text_rect = text.get_rect()
    text_rect.topright = (1900, 20)

    screen.blit(text, camera.apply(text_rect))

    # WALLPUNCH
    pygame.draw.rect(screen, (145, 35, 11), camera.apply(wallpunch_empty))
    height = ((pygame.time.get_ticks() - last_wallpunch) / 1000 ) / settings.wallpunch_time
    if height > 1: height = 1
    fill = pygame.Rect(0, 0, 50, 600 * height)
    fill.bottomleft = (1850, 700)
    pygame.draw.rect(screen, (241, 193, 10), camera.apply(fill))
    text = FONT2.render("WALLPUNCH", True, (255, 255, 255))
    text_surface = pygame.Surface(wallpunch_empty.size)
    text_surface.blit(text, text_surface.get_rect())
    pygame.transform.rotate(text_surface, 270)

    if punch_active:
        game_w.blit(punch_png, (gridSize * (player.pos.x - xstart) - 18 / 64 * gridSize, gridSize * (player.pos.y - ystart) - 64 / 64 * gridSize))
    
    #screen.blit(text_surface, (1850, 100))

    # Game windown crtanje
    game_rect = pygame.Rect(0, 0, cam_size.x * gridSize, cam_size.y * gridSize)
    game_rect.center = ((cam_pos.x - xstart) * gridSize, (cam_pos.y - ystart) * gridSize)

    screen.blit(camera.apply(game_w), camera.apply((cam_tl.x, cam_tl.y)), area = camera.apply(game_rect))
    
    pygame.display.flip()


# Resetiranje labirinta i svih gluposti
def restart():
    global player, zombies, maze_zombies, start_delay_active, start_time, state, inputs
    global cam_despos, cam_pos

    pygame.mixer.music.load("Music\\Dummy.mp3")
    pygame.mixer.music.play(loops=-1)

    cam_despos = pygame.Vector2(1,1)
    cam_pos = pygame.Vector2(4,4)
    
    player = player_start.copy()
    zombies = []
    for i in zombies_start:
        zombies.append(i.copy())
    maze_zombies = []
    for i in maze_zombies_start:
        maze_zombies.append(i.copy())
    start_delay_active = True
    start_time = pygame.time.get_ticks()
    state = "maze"
    inputs = []


# Funkcija za otvaranje UI-a za death screen  
def death_screen():
    global clock, state
    
    state = "dead"

    pygame.mixer.music.load("Music\\Lose.mp3")
    
    pygame.mixer.Sound("Music\\Death.wav").play()

    pygame.time.delay(2000)
    
    pygame.mixer.Sound("Music\\Drumroll.wav").play()

    pygame.time.delay(2000)
    
    pygame.mixer.Sound("Music\\Ploop.mp3").play()

    death_message = random.choice(death_messages)
    
    while state == "dead":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = camera.unscale(pygame.mouse.get_pos())
                
                if restart_btn.collidepoint(mouse_pos):
                    print("Restart the game!")
                    return "restart"
                if home_btn.collidepoint(mouse_pos):
                    print("Back to home screen!")
                    return "home"
                
            
        # Prozirna pozadina
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 60))
        screen.blit(camera.apply(overlay), (0,0))

        # Naslov
        title = main.FONT.render(death_message, True, main.WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, camera.apply(title_rect))

        # Gumbići
        mouse_pos = camera.unscale(pygame.mouse.get_pos())
        draw_text("Restart", camera.apply(restart_btn), (51, 153, 255), (0, 102, 204), restart_btn.collidepoint(mouse_pos))
        draw_text("Back to home", camera.apply(home_btn), (255, 51, 51), (204, 0, 0), home_btn.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(FPS)
    

# Funkcija za otvaranje UI-a za win screen
def win_screen(start_time):
    global clock, state

    state = "win"

    pygame.mixer.music.load("Music\\Win.mp3")
    
    pygame.mixer.Sound("Music\\Door.wav").play()

    pygame.time.delay(2000)
    
    pygame.mixer.Sound("Music\\Drumroll.wav").play()

    pygame.time.delay(2000)
    
    pygame.mixer.Sound("Music\\DumbVictory.wav").play()

    win_message = random.choice(win_messages)
    time_played = round((pygame.time.get_ticks() - start_time) / 1000, 2)
    time_message = "The time it took: " + str(time_played) + " seconds."
    
    while state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = camera.unscale(pygame.mouse.get_pos())
                
                if restart_btn.collidepoint(mouse_pos):
                    print("Restart the game!")
                    return "restart"
                if home_btn.collidepoint(mouse_pos):
                    print("Back to home screen!")
                    return "home"
            
        # Prozirna pozadina
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 60))
        screen.blit(camera.apply(overlay), (0,0))

        # Vrijeme igranja
        time_played = main.FONT.render(time_message, True, main.WHITE)
        time_rect = time_played.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(time_played, camera.apply(time_rect))
        
        # Naslov
        title = main.FONT.render(win_message, True, main.WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, camera.apply(title_rect))

        # Gumbići
        mouse_pos = camera.unscale(pygame.mouse.get_pos())
        draw_text("Restart", camera.apply(restart_btn), (51, 153, 255), (0, 102, 204), restart_btn.collidepoint(mouse_pos))
        draw_text("Back to home", camera.apply(home_btn), (255, 51, 51), (204, 0, 0), home_btn.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(FPS)


def main2(redak, stupac, active_difficulty):
    global brRedaka, brStupaca, difficulty
    global maze, start_time, start_delay_active
    global player, zombies, zombies_start, maze_zombies, inputs, state
    global clock
    global cam_pos, cam_despos
    global punch_active, last_wallpunch

    # Muzikica :D
    pygame.mixer.music.load("Music\\Dummy.mp3")
    pygame.mixer.music.play(loops=-1)
    
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
    zombies = []
    for i in zombies_start:
        zombies.append(i.copy())
    
    clock = pygame.time.Clock()
    
    while state == "maze":
        current_time = pygame.time.get_ticks()

        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Provjera je li kliknut neki od gumba
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = camera.unscale(event.pos)
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(mouse_pos):
                        if(button_lables[i]=="Back"):
                            print("Back to home screen!")
                            restart()
                            return
                        elif(button_lables[i]=="Restart"):
                            restart()
                            print("Restart the game!")

            # Kretanje igrača tako da se tipke mogu držat, i ako je pritisnuto više tipka uzima se ona novija
            elif event.type == pygame.KEYDOWN:
            
                # Privremena tipka za ubit se
                if event.key == pygame.K_k:
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

                # WALLPUNCH tipka
                elif event.key == pygame.K_e and ((pygame.time.get_ticks() - last_wallpunch) / 1000 ) >= settings.wallpunch_time:
                    punch_active = True
            
            # Mijenjanje veličine ekrana
            elif event.type == pygame.VIDEORESIZE:
                main.resize_screen(screen.get_size()[0], screen.get_size()[1], False)

        for i in range(len(directions)):
            check_pos = directions[i]+ player.pos
            
            if 0 <= check_pos.x < brStupaca and 0 <= check_pos.y < brRedaka:
                
                if (maze[int(check_pos.y)][int(check_pos.x)] < 0) or punch_active == True:
                    player.around[i] = 0
                    
                else: player.around[i] = 1

            else: player.around[i] = 1
                
        
        if(player.move(settings.player_move_time, events) == "Started" and punch_active == True):
            punch_active = False
            last_wallpunch = pygame.time.get_ticks()
            pygame.mixer.Sound("Music\\Damage.wav").play()
            x,y = int(player.move_pos.y), int(player.move_pos.x)
            if maze[x][y] >= 0:
                maze[x][y]=-1
                for i in range(4):
                    r,s = int(x + directions[i].y), int(y + directions[i].x)
                    if 0<=r<brRedaka  and 0<=s<brStupaca:
                        if maze[r][s]>=0:
                            if i == 0:
                                maze[r][s] -= 2
                            elif i == 1:
                                maze[r][s] -= 1
                            elif i == 2:
                                maze[r][s] -= 8
                            else:
                                maze[r][s] -= 4
                                
                                
        
        # Camera positioning
        cam_despos = player.pos.copy()
        cam_pos = cam_despos.copy()
        
        if(cam_despos.x < (cam_size.x - 1) // 2): cam_pos.x = (cam_size.x - 1) // 2
        if(cam_despos.x > brStupaca - (cam_size.x + 1) // 2): cam_pos.x = brStupaca - (cam_size.x + 1) // 2
        if(cam_despos.y < (cam_size.y - 1) // 2): cam_pos.y = (cam_size.y - 1) // 2
        if(cam_despos.y > brRedaka - (cam_size.y + 1) // 2): cam_pos.y = brRedaka - (cam_size.y + 1) // 2

        cam_pos.x += 0.5
        cam_pos.y += 0.5
        
        # Provjera mogu li se zombiji kretati i smooth kretanje te PROVJERA COLLISIONA sa playerom
        for i,zombie in enumerate(zombies):

            if isinstance(zombie, Brain):
                
                if (pygame.time.get_ticks() - zombie.last_move_time) / 1000 >= zombie.move_time + zombie.pause_time:
                    zombie.move(bfs(zombie.pos, player.move_pos))
                    maze_zombies[int(zombie.last_pos.y)][int(zombie.last_pos.x)] = 0
                    maze_zombies[int(zombie.move_pos.y)][int(zombie.move_pos.x)] = 1
                else:
                    zombie.move(-1)
    
            else:
                for i in range(len(directions)):
                            check_pos = directions[i]+ zombie.pos
                            
                            if 0 <= check_pos.x < brStupaca and 0 <= check_pos.y < brRedaka:
                                
                                if maze[int(check_pos.y)][int(check_pos.x)] == -1 and maze_zombies[int(check_pos.y)][int(check_pos.x)] == 0:
                                    zombie.around[i] = 0
                                    
                                else: zombie.around[i] = 1

                            else: zombie.around[i] = 1

            
                # Pomicanje zombija
                if zombie.move() == "Started":
                    maze_zombies[int(zombie.last_pos.y)][int(zombie.last_pos.x)] = 0
                    maze_zombies[int(zombie.move_pos.y)][int(zombie.move_pos.x)] = 1

            # Provjera collisiona sa playerom
            if (zombie.moving or player.moving) and zombie.rect.colliderect(player.rect):
                action = death_screen()
                if(action == "restart"):
                    restart()
                    print("Restart the game!")
                elif(action == "home"):
                    restart()
                    return

        # Provjera collisiona igrača i exita
        if (player.moving) and player.rect.colliderect(door_rect):
            action = win_screen(start_time)
            if(action == "restart"):
                restart()
                print("Restart the game!")
            elif(action == "home"):
                restart()
                return

        draw()
        clock.tick(FPS)

    # Stanje je mrtvost pa biti pokrenuti UI za death_screen ooga booga
    
