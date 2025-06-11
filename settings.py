import pygame

# Rezolucija
FPS = 30
WIDTH, HEIGHT = 1920, 1080

# Igrica
minimum_maze_width, minimum_maze_height = 5,5


# Player
player_move_time = 0.14
up = (pygame.K_UP, pygame.K_w)
left = (pygame.K_LEFT, pygame.K_a)
down = (pygame.K_DOWN, pygame.K_s)
right = (pygame.K_RIGHT, pygame.K_d)
input_delay = 0.1
wallpunch_time = 10

# Zombies
zombie_move_time = 0.7
zombie_pause_time = 0.5
zombie_acceleration = 0.01 # Koliko im puta treba manje da se pomaknu

# Difficulties (Easy, pa normal, pa hard)

maze_simpleness = (16, 20, 25) # Čim veće tim teže
maze_safezone_chance = (0.65, 0.5, 0.35) # Šansa za no zombie zonu
smarter_chance = (0.25, 0.25, 0.25)
#brain_chance = (0.01, 0.015, 0.025)
brain_chance = (0.10, 0.15, 0.20)

    
