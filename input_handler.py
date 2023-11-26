import pygame
import storage
import menu

def handle(player):
    # Get key inputs
    keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    # North
    if keys[pygame.K_KP8]:
        if player.move(0,-1) == 1:
            return 1
    # South
    elif keys[pygame.K_KP2]:
        if player.move(0,+1) == 1:
            return 1
    # West
    elif keys[pygame.K_KP4]:
        if player.move(-1,0) == 1:
            return 1
    # East
    elif keys[pygame.K_KP6]:
        if player.move(+1,0) == 1:
            return 1
    # North-West
    elif keys[pygame.K_KP7]:
        if player.move(-1,-1) == 1:
            return 1
    # North-East
    elif keys[pygame.K_KP9]:
        if player.move(+1,-1) == 1:
            return 1
    # South-West
    elif keys[pygame.K_KP1]:
        if player.move(-1,+1) == 1:
            return 1
    # South-East
    elif keys[pygame.K_KP3]:
        if player.move(+1,+1) == 1:
            return 1
    elif keys[pygame.K_KP5]:
        return 1
    elif keys[pygame.K_KP_ENTER]:
        if player.stair() == 2:
            return 2
        else:
            return 0
    
    elif keys[pygame.K_KP_MULTIPLY]:
        if player.pickup() == 1:
            return 1
        return 0
    
    elif keys[pygame.K_ESCAPE]:
        if player.health > 0:
            storage.storeall()
        else:
            storage.clearstorage()
        return 50
    
    elif keys[pygame.K_KP_PLUS]:
        if menu.interface() == 1:
            return 1

    elif keys[pygame.K_KP_MINUS]:
        if menu.spellinterface() == 1:
            return 1
            
    return 0
