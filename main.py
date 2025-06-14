# Uvozimo knjiznice
import pygame
import sys
import game
from camera import Camera
import settings
from network import Network

# Pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT
screen=pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('2D maze runner - home')

# Muzikica :D
pygame.mixer.music.load("Music\\Menu.mp3")
pygame.mixer.music.play(loops=-1)

# Za pravilno skaliranje veličina
screen_WIDTH, screen_HEIGHT = screen.get_size()
camera = Camera(scale=max(screen_WIDTH / WIDTH, screen_HEIGHT / HEIGHT))

fullscreen = False

FPS = settings.FPS

# Fontovi
fonts = {"FONT": (None, 36),
         "ERROR_FONT": (None, 36),
         "FONT2": (None, 54)
    }
FONT = camera.applyFont(fonts["FONT"][0], fonts["FONT"][1])
ERROR_FONT = camera.applyFont(fonts["ERROR_FONT"][0], fonts["ERROR_FONT"][1])
FONT2 = camera.applyFont(fonts["FONT2"][0], fonts["FONT2"][1])

# Boje osnovne za koristit
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
DARK_BLUE = (0, 0, 153)
RED = (255, 0, 0)

# Namjestanje input boxesa
inWidth = 140
inHeight = 40
input_boxes = [
    pygame.Rect(100, 80, inWidth, inHeight),
    pygame.Rect(100, 140, inWidth, inHeight)
]
inputs = ["", ""]
active_box = [True, False]

# Namjestanje buttona
start_buttons = [
    pygame.Rect(100, 200, 140, 50),
    pygame.Rect(100, 260, 140, 50)
    ]
difficulty_buttons = [
    pygame.Rect(340, 80, 140, 50),
    pygame.Rect(340, 140, 140, 50),
    pygame.Rect(340, 200, 140, 50)
]
active_difficulty = 1
active_difficulty_button = [False, True, False]
name_start_button = ["Play local", "Play online",]
name_difficulty_button = ["Easy", "Normal", "Hard"]

# Poruka za grešku premalih inputa i ostalog
error_message = ""


def resize_screen(x, y, is_fullscreen):
    global fonts, FONT, ERROR_FONT
    
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_WIDTH, screen_HEIGHT = screen.get_size()
    else:
        screen_WIDTH, screen_HEIGHT = x, y
        screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)

    camera.scale = max(screen_WIDTH / WIDTH, screen_HEIGHT / HEIGHT)

    # Namjestavanje nove velicine fontova jer su glupi i ne mogu drugacije ):
    FONT = camera.applyFont(fonts["FONT"][0], fonts["FONT"][1])
    ERROR_FONT = camera.applyFont(fonts["ERROR_FONT"][0], fonts["ERROR_FONT"][1])
    FONT2 = camera.applyFont(fonts["FONT2"][0], fonts["FONT2"][1])    


def draw():
    
    screen.fill(WHITE)

    middle = screen.get_rect().center

    labels = ["Width", "Height"]
    
    # Crtanje input boxova
    for i, box in enumerate(input_boxes):
        # Crtanje texta
        box = camera.apply(box).copy()
        label_surface = FONT.render(labels[i], True, BLACK)
        screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + 5))

        # Input boxovi
        color = BLUE if active_box[i] else GRAY
        pygame.draw.rect(screen, color, box, 2)
        text_surface = FONT.render(inputs[i], True, BLACK)
        screen.blit(text_surface, (box.x + 5, box.y + 5))
        box.w = max(140, text_surface.get_width() + 10)

    # Crtanje start buttona
    for i, button in enumerate(start_buttons):
        button = camera.apply(button)
        pygame.draw.rect(screen, GREEN, button)
        button_text = FONT.render(name_start_button[i], True, WHITE)
        text_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, text_rect)

    # Crtanje difficulty buttona
    for i,box in enumerate(difficulty_buttons):
        box = camera.apply(box)
        if i == active_difficulty:
            pygame.draw.rect(screen, BLUE, box)
            button_text = FONT.render(name_difficulty_button[i], True, DARK_BLUE)
        else:
            pygame.draw.rect(screen, GRAY, box)
            button_text = FONT.render(name_difficulty_button[i], True, BLACK)
        text_rect = button_text.get_rect(center=box.center)
        screen.blit(button_text, text_rect)

    # Prikaz poruke za grešku
    if error_message:
        error_surface = ERROR_FONT.render(error_message, True, (200, 0, 0))
        screen.blit(error_surface, camera.apply((340, 270)))
    
    pygame.display.flip()

def main():
    global error_message
    global active_difficulty
    global fullscreen
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = camera.unscale(event.pos)
                
                # Aktivacija input boxova
                for i in range(len(input_boxes)):
                    active_box[i] = input_boxes[i].collidepoint(mouse_pos)

                # Klikanje start gumba
                if start_buttons[0].collidepoint(mouse_pos):
                    try:
                        width = int(inputs[0])
                        height = int(inputs[1])
                        if width < settings.minimum_maze_width or height < settings.minimum_maze_height:
                            error_message = "Visina i širina moraju biti veći od 5"
                        else:
                            error_message = ""
                            game.main2(height, width, active_difficulty)
                            pygame.mixer.music.load("Music\\Menu.mp3")
                            pygame.mixer.music.play(loops=-1)
                    except ValueError:
                        error_message = "Unesite brojeve u oba polja"
                elif start_buttons[1].collidepoint(mouse_pos):
                    error_message = "Ovo još ne radi |:"

                
                
                # Odabir difficultyja
                for i in range(len(difficulty_buttons)):
                    if difficulty_buttons[i].collidepoint(mouse_pos):
                        active_difficulty_button[active_difficulty] = False
                        active_difficulty = i
                        active_difficulty_button[active_difficulty] = True
                        
                                                 
            #Tipkanje u input boxove
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_F11:
                    
                    fullscreen = not fullscreen
                    
                    if fullscreen:
                        resize_screen(0, 0, True)
                    else:
                        resize_screen(WIDTH, HEIGHT, False)
                        
                for i in range(len(input_boxes)):
                    if active_box[i]:
                        if event.key == pygame.K_BACKSPACE:
                            inputs[i] = inputs[i][:-1]
                        elif event.unicode.isdigit():
                            inputs[i] += event.unicode


            # Mijenjanje veličine ekrana
            elif event.type == pygame.VIDEORESIZE:
                resize_screen(screen.get_size()[0], screen.get_size()[1], False)
        

        draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
