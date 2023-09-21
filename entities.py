entitylist = []
import gamemap
import state
import pygame
import input_handler
import raycaster
import random

# Global list "entitylist" holds all active entities. It will be looped through every tick to update the state of each entity


# Base class "Entity".
class Entity():
    def __init__(self, name, x, y, health, char, colour, viewrestrict, initiative):
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.char = char
        self.colour = colour
        self.viewrestrict = viewrestrict
        self.speed = 1
        self.initiative = initiative
        self.ap = 0
    def move(self,xoffset,yoffset):
      Map = gamemap.getmap()
      if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
        Map[self.y][self.x].occupants.remove(self)
        self.x += xoffset
        self.y += yoffset
        Map[self.y][self.x].occupants.append(self)
        
        
        player = getplayer()
        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),getplayer().viewrestrict))
        return True
      else:
        return False
    def take_action(self):
        player = getplayer()
        dist = raycaster.distance(self.x, self.y, player.x, player.y)
        if dist < 1.5 and self.health > 0:
            self.attack(player)
        elif dist < 10 and self.health > 0:
            x,y = direction(self.x, self.y, player.x, player.y)
            self.move(x*self.speed,y*self.speed)
        #print("Entity: I took an action!")
        return True
    
    def attack(self, target):
        if target.health > 0:
            target.health -= 1
            if target.health == 0:
                print(target.name, " is dead!")
                target.name = target.name + "'s corpse"
                target.speed = 0
                target.initiative = 0
                target.ap = 0
                target.char = "%"
            else:
                print(target.name, "'s health is now ", target.health)
        else:
            print(target.name, " is dead")
        return True

class Player(Entity):
    def __init__(self, name, x, y, health, char, colour, viewrestrict, initiative):
        Entity.__init__(self, name, x, y, health, char, colour, viewrestrict, initiative)

    def take_action(self):
        action = False
        while action != True:
            pygame.time.delay(100)
            pygame.event.wait()
            if input_handler.handle(self) == True:
                action = True
        print("Player: I took an action!")
        
    def move(self,xoffset,yoffset):
        Map = gamemap.getmap()
        if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
            Map[self.y][self.x].occupants.remove(self)
            self.x += xoffset*self.speed
            self.y += yoffset*self.speed
            Map[self.y][self.x].occupants.append(self)
            gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
            return True

        elif Map[self.y+yoffset][self.x+xoffset].occupants != [] and self.health > 0:
            self.attack(Map[self.y+yoffset][self.x+xoffset].occupants[0])
            return True
        elif self.health > 0:
            print("The way is blocked")
            return False
        else:
            print("You are dead. Act like it.")
            
def create_entity(name: str, x: int, y: int, health: int, char: str, colour, viewrestrict, initiative):
    global entitylist
    newEntity = Entity(name, x, y, health, char, colour, viewrestrict, initiative)
    newEntity.ap = random.randint(0,29)
    entitylist.insert(0,newEntity)
    return newEntity

def create_player(name: str, x: int, y: int, health: int, char: str, colour, viewrestrict, initiative):
    global entitylist
    newEntity = Player(name, x, y, health, char, colour, viewrestrict, initiative)
    entitylist.insert(0,newEntity)
    return newEntity

def getentities():
    return entitylist

def getplayer():
    return entitylist[len(entitylist)-1]


def detectcollision(x,y,Map):
    if Map[y][x].walkable == False or Map[y][x].occupants != []:
        return True

def direction(startx, starty, destx, desty):
    ndist = raycaster.distance(startx, starty-1, destx, desty)
    nedist = raycaster.distance(startx+1, starty-1, destx, desty)
    edist = raycaster.distance(startx+1, starty, destx, desty)
    sedist = raycaster.distance(startx+1, starty+1, destx, desty)
    sdist = raycaster.distance(startx, starty+1, destx, desty)
    swdist = raycaster.distance(startx-1, starty+1, destx, desty)
    wdist = raycaster.distance(startx-1, starty, destx, desty)
    nwdist = raycaster.distance(startx-1, starty-1, destx, desty)

    # If North is closest, go North
    if ndist < nedist and ndist < edist and ndist < sedist and ndist < sdist and ndist < swdist and ndist < wdist and ndist < nwdist:
        return 0,-1
    # If North-East is closest, go North-East
    elif nedist < edist and nedist < sedist and nedist < sdist and nedist < swdist and nedist < wdist and nedist < nwdist:
        return 1,-1
    # If East is closest, go East
    elif edist < sedist and edist < sdist and edist < swdist and edist < wdist and edist < nwdist:
        return 1,0
    # If South-East is closest, go South-East
    elif sedist < sdist and sedist < swdist and sedist < wdist and sedist < nwdist:
        return 1,1
    # If South is closest, go South
    elif sdist < swdist and sdist < wdist and sdist < nwdist:
        return 0,1
    # If South-West is closest, go South-West
    elif swdist < wdist and swdist < nwdist:
        return -1,1
    # If West is closest, go West
    elif wdist < nwdist:
        return -1,0
    # If North-West is closes, go West
    else:
        return -1,-1
