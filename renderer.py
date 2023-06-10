import pygame
import entities

def update(screen, font):
    screen.fill((0,0,0))
    
    entitylist = entities.entitylist

    for i in range(len(entitylist)):
        CurrentEntity = entitylist[i]
        CurrentEntityPos = (CurrentEntity.x * 16, CurrentEntity.y * 16)
        text = font.render(CurrentEntity.char, True, CurrentEntity.colour)
        screen.blit(text, CurrentEntityPos)
        
    pygame.display.update()
