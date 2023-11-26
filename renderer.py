import pygame
import entities
import gamemap
import colours
import menu


colourdict = colours.getcolours() 

black = colourdict["black"]
red = colourdict["red"]
lightblue = colourdict["lightblue"]
maroon = colourdict["maroon"]

def update(screen, font, width, height):
    screen.fill(black)
    player = entities.getplayer()
    entitylist = entities.getentities()
    
    Map = gamemap.getmap()
    # Iterate through every tile of the map
    for y in range(height):
        for x in range(width):
            CurrentTile = Map[y][x]
            # border is always visible so handle seperately
            if CurrentTile.name == "border":
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                text = font.render(CurrentTile.char, True, CurrentTile.colour)
                screen.blit(text, CurrentTilePos)
            # If the current tile should be rendered
            elif CurrentTile.rendered == True:
                # Scale tile sizes up to "pixel sizes". One tile is 16x16 pixels
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                # Create the text to be rendered using the entity info
                text = font.render(CurrentTile.char, True, CurrentTile.colour)
                screen.blit(text, CurrentTilePos)

    # Loop through all active entities and render them ontop of the tiles. 
    for i in range(len(entitylist)):
        CurrentEntity = entitylist[i]
        # If on a rendered tile
        if Map[CurrentEntity.y][CurrentEntity.x].rendered == True:
            CurrentEntityPos = (CurrentEntity.x * 16, CurrentEntity.y * 16)
            text = font.render(CurrentEntity.char, True, CurrentEntity.colour, black)
            # same as before, except the background is specified as black (will completely cover the tile below)
            screen.blit(text, CurrentEntityPos)
            
    
    ui(screen,width,height)
    menu.inventorymenu(screen)
    
    # Update the pygame display- output it. 
    pygame.display.update()

def flash(entity, colour):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("timesnewroman", 16)
    entitypos = (entity.x * 16, entity.y * 16)
    text = font.render(entity.char, True, colour, black)
    screen.blit(text, entitypos)
    pygame.display.update()
    pygame.time.delay(100)
    return
    
def ui(screen,width,height):
    font = pygame.font.SysFont("timesnewroman", 50)
    
    hearttext = font.render("♥", True, red)
    screen.blit(hearttext, (32,850))
    healthtext = font.render(str(entities.getplayer().health)+"/"+str(entities.getplayer().maxhealth), True, red)
    screen.blit(healthtext, (84,850))
    
    startext = font.render("☼", True, lightblue)
    screen.blit(startext, (23,900))
    manatext = font.render(str(entities.getplayer().mana)+"/"+str(entities.getplayer().maxmana), True, lightblue)
    screen.blit(manatext, (84,900))
    
    invtext = pygame.font.SysFont("times new roman", 30).render("Inventory", True, maroon)
    screen.blit(invtext, (800,10))

    spelltext = pygame.font.SysFont("times new roman", 30).render("Spells", True, lightblue)
    screen.blit(spelltext, (800,500))
