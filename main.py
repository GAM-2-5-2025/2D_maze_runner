#uvozimo knjiznice
import pygame
from sys import exit

#pokretanje igrice, rezolucije, ime prozora, pod
pygame.init()
screen=pygame.display.set_mode((1366,768))
pygame.display.set_caption('2D maze runner')
clock = pygame.time.Clock()

test_pod = pygame.Surface((1366,768))
test_pod.fill('bisque2')

#ulazimo u beskonačnu petlju koja se može prekinuti samo iznutra
while True:
    for event in pygame.event.get():
        #interno zaustavljanje programa
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_pod,(0,0))        
    
    #konst. azuriranje ekrana
    pygame.display.update()
    clock.tick(60)
    
