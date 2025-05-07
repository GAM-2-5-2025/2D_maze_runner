#uvozimo knjiznice
import pygame
from sys import exit

#pokretanje igrice, rezolucije i ime prozora
pygame.init()
screen=pygame.display.set_mode((1366,768))
pygame.display.set_caption('2D maze runner')
clock = pygame.time.Clock()

#ulazimo u beskonačnu petlju koja se može prekinuti samo iznutra
while True:
    for event in pygame.event.get():
        #interno zaustavljanje programa
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #konst. azuriranje ekrana
    pygame.display.update()
    clock.tick(60)
    
