import pygame

def handle(player):
    # Get key inputs
    keys = pygame.key.get_pressed()
    # North
    if keys[pygame.K_KP8]:
        if player.move(0,-1) == True:
            return True
    # South
    elif keys[pygame.K_KP2]:
        if player.move(0,+1) == True:
            return True
    # West
    elif keys[pygame.K_KP4]:
        if player.move(-1,0) == True:
            return True
    # East
    elif keys[pygame.K_KP6]:
        if player.move(+1,0) == True:
            return True
    # North-West
    elif keys[pygame.K_KP7]:
        if player.move(-1,-1) == True:
            return True
    # North-East
    elif keys[pygame.K_KP9]:
        if player.move(+1,-1) == True:
            return True
    # South-West
    elif keys[pygame.K_KP1]:
        if player.move(-1,+1) == True:
            return True
    # South-East
    elif keys[pygame.K_KP3]:
        if player.move(+1,+1) == True:
            return True


    # Swap view restrict mode for dev purposes
    elif keys[pygame.K_SPACE]:
        if player.viewrestrict == 0:
            player.viewrestrict = 10
        else:
            player.viewrestrict = 0
        return True
            
    return False
