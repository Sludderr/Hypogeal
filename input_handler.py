import pygame

def handle(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP8]:
        player.y -= player.speed
        print("UP")
    if keys[pygame.K_KP2]:
        player.y += player.speed
        print("DOWN")
    if keys[pygame.K_KP4]:
        player.x -= player.speed
        print("LEFT")
    if keys[pygame.K_KP6]:
        player.x += player.speed
        print("RIGHT")
    if keys[pygame.K_KP7]:
        player.y -= player.speed
        player.x -= player.speed
        print("UP_LEFT")
    if keys[pygame.K_KP9]:
        player.y -= player.speed
        player.x += player.speed
        print("UP_RIGHT")
    if keys[pygame.K_KP1]:
        player.y += player.speed
        player.x -= player.speed
        print("DOWN_LEFT")
    if keys[pygame.K_KP3]:
        player.y += player.speed
        player.x += player.speed
        print("DOWN_RIGHT")
        
