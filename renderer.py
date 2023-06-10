import pygame
import entities
import gamemap
import colours

colourdict = colours.getcolours() 

black = colourdict["black"]

def update(screen, font, width, height):
    screen.fill(black)
    
    Map = gamemap.getmap()
    for y in range(height):
        for x in range(width):
            CurrentTile = Map[y][x]
            if CurrentTile.visible == True:
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                text = font.render(CurrentTile.char, True, CurrentTile.colour)
                screen.blit(text, CurrentTilePos)
            
    
    entitylist = entities.entitylist

    for i in range(len(entitylist)):
        CurrentEntity = entitylist[i]
        CurrentEntityPos = (CurrentEntity.x * 16, CurrentEntity.y * 16)
        text = font.render(CurrentEntity.char, True, CurrentEntity.colour, black)
        screen.blit(text, CurrentEntityPos)
        
    pygame.display.update()

