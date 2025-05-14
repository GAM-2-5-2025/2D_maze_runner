#uvozimo knjiznice
import pygame
import sys

#pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()

WIDTH, HEIGHT = 1366, 768
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2D maze runner')

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Fonts
FONT = pygame.font.Font(None, 36) #Default

#test_pod = pygame.Surface((1366,768))
#test_pod.fill('bisque2')

# Input boxes setup
input_boxes = [
    pygame.Rect(100, 80, 140, 40),
    pygame.Rect(100, 140, 140, 40)
]
inputs = ["", ""]
active_box = [False, False]

# Start button setup
start_button = pygame.Rect(100, 200, 140, 50)

# Maze setup
maze = [][]


def draw():
    screen.fill(WHITE)

    labels = ["Width", "Height"]
    
    # Draw input boxes
    for i, box in enumerate(input_boxes):
        # Label text
        label_surface = FONT.render(labels[i], True, BLACK)
        screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + 5))

        # Input box
        color = BLUE if active_box[i] else GRAY
        pygame.draw.rect(screen, color, box, 2)
        text_surface = FONT.render(inputs[i], True, BLACK)
        screen.blit(text_surface, (box.x + 5, box.y + 5))
        box.w = max(140, text_surface.get_width() + 10)

    # Draw Start button
    pygame.draw.rect(screen, GREEN, start_button)
    button_text = FONT.render("Start", True, WHITE)
    text_rect = button_text.get_rect(center=start_button.center)
    screen.blit(button_text, text_rect)

    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Input box activation
                for i in range(len(input_boxes)):
                    active_box[i] = input_boxes[i].collidepoint(event.pos)

                # Start button click
                if start_button.collidepoint(event.pos):
                    print("Start button clicked!")
                    print("Entered numbers:", inputs)

            if event.type == pygame.KEYDOWN:
                for i in range(len(input_boxes)):
                    if active_box[i]:
                        if event.key == pygame.K_BACKSPACE:
                            inputs[i] = inputs[i][:-1]
                        elif event.unicode.isdigit():
                            inputs[i] += event.unicode

        draw()
        clock.tick(30)


if __name__ == "__main__":
    main()
