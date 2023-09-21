def handle(player):
    # Get key inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP8]:     # North
        if player.move(0,-1) == True:
            return True
    elif keys[pygame.K_KP2]:   # South
        if player.move(0,+1) == True:
            return True
    elif keys[pygame.K_KP4]:   # West
        if player.move(-1,0) == True:
            return True
    elif keys[pygame.K_KP6]:   # East
        if player.move(+1,0) == True:
            return True
    elif keys[pygame.K_KP7]:   # North-West
        if player.move(-1,-1) == True:
            return True
    elif keys[pygame.K_KP9]:   # North-East
        if player.move(+1,-1) == True:
            return True
    elif keys[pygame.K_KP1]:   # South-West
        if player.move(-1,+1) == True:
            return True
    elif keys[pygame.K_KP3]:   # South-East
        if player.move(+1,+1) == True:
            return True
    elif keys[pygame.K_KP5]:
        return True

    return False
