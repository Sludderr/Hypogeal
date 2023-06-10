import pygame
import gamemap



def detectcollision(x,y,Map):
    if Map[y][x].walkable == False:
        return True

def handle(player):
    Map = gamemap.getmap()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP8]:
        if detectcollision(player.x, player.y-1, Map) != True:
            player.y -= player.speed
            print("UP")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP2]:
        if detectcollision(player.x, player.y+1, Map) != True:
            player.y += player.speed
            print("DOWN")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP4]:
        if detectcollision(player.x-1, player.y, Map) != True:
            player.x -= player.speed
            print("LEFT")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP6]:
        if detectcollision(player.x+1, player.y, Map) != True:
            player.x += player.speed
            print("RIGHT")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP7]:
        if detectcollision(player.x-1, player.y-1, Map) != True:
            player.y -= player.speed
            player.x -= player.speed
            print("UP_LEFT")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP9]:
        if detectcollision(player.x+1, player.y-1, Map) != True:
            player.y -= player.speed
            player.x += player.speed
            print("UP_RIGHT")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP1]:
        if detectcollision(player.x-1, player.y+1, Map) != True:
            player.y += player.speed
            player.x -= player.speed
            print("DOWN_LEFT")
        else:
            print("The way is blocked")
    elif keys[pygame.K_KP3]:
        if detectcollision(player.x+1, player.y+1, Map) != True:
            player.y += player.speed
            player.x += player.speed
            print("DOWN_RIGHT")
        else:
            print("The way is blocked")
        
