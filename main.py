#uvozimo pygame
import pygame

#pokrecemo igricu, postavljamo rezoluciju W=1366 piksela i H=768 piksela
pygame.init()
screen=pygame.display.set_mode((1366,768))

#ulazimo u beskonačnu petlju koja se može prekinuti samo iznutra
while True:
    for event in pygame.event.get():
        #interno zaustavljanje programa
        if event.type == pygame.QUIT:
            pygame.quit()
    
    #postavimo konstantno azuriranje ekrana
    pygame.display.update()
    
