import pygame
import gamemap
import state
import storage

def handle(player):
    # Get key inputs
    keys = pygame.key.get_pressed()
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
            storage.storeplayer(player)
            return 1
        return 0

    elif keys[pygame.K_UP]:
        player.viewrestrict += 1
        gamemap.setmap(state.update_visibility(gamemap.getmap(), player.x, player.y, gamemap.width, gamemap.height,player.viewrestrict+1))
        return 1
    
    elif keys[pygame.K_DOWN]:
        player.viewrestrict -= 1
        gamemap.setmap(state.update_visibility(gamemap.getmap(), player.x, player.y, gamemap.width, gamemap.height,player.viewrestrict+1))
        return 1
        
    # Swap view restrict mode for dev purposes
    elif keys[pygame.K_SPACE]:
        if player.viewrestrict == 0:
            player.viewrestrict = 10
        else:
            player.viewrestrict = 0
        return 1
            
    return 0
