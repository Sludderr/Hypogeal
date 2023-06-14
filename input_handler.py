import pygame
import gamemap
import state

def detectcollision(x,y,Map):
    if Map[y][x].walkable == False:
        return True

def handle(player):
    Map = gamemap.getmap()
    width = gamemap.getwidth()
    height = gamemap.getheight()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP8]:
        if detectcollision(player.x, player.y-1, Map) != True:
            player.y -= player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # UP
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP2]:
        if detectcollision(player.x, player.y+1, Map) != True:
            player.y += player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # DOWN
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP4]:
        if detectcollision(player.x-1, player.y, Map) != True:
            player.x -= player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # LEFT
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP6]:
        if detectcollision(player.x+1, player.y, Map) != True:
            player.x += player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # RIGHT
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP7]:
        if detectcollision(player.x-1, player.y-1, Map) != True:
            player.y -= player.speed
            player.x -= player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # UP_LEFT
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP9]:
        if detectcollision(player.x+1, player.y-1, Map) != True:
            player.y -= player.speed
            player.x += player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # UP_RIGHT
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP1]:
        if detectcollision(player.x-1, player.y+1, Map) != True:
            player.y += player.speed
            player.x -= player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # DOWN_LEFT
        else:
            # COLLISION
            print("The way is blocked")
    elif keys[pygame.K_KP3]:
        if detectcollision(player.x+1, player.y+1, Map) != True:
            player.y += player.speed
            player.x += player.speed
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, width, height))
            # DOWN_RIGHT
        else:
            # COLLISION
            print("The way is blocked")
        
    elif keys[pygame.K_SPACE]:
        if player.viewrestrict == 0:
            player.viewrestrict = 10
        else:
            player.viewrestrict = 0
