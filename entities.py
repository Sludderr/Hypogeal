entitylist = []
import gamemap
import state
import pygame
import input_handler
import raycaster
import random
import colours
import renderer

colourdict = colours.getcolours() 
red = colourdict["red"]
lightblue = colourdict["lightblue"]
green = colourdict["green"]

# Global list "entitylist" holds all active entities. It will be looped through every tick to update the state of each entity

# Base class "Entity".
class Entity():
    def __init__(self, name, x, y, health, char, colour):
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = health
        self.char = char
        self.colour = colour
        self.speed = 1
        self.blocking = False
        self.sentient = False
        self.pickupable = False
        
    def take_action(self):
        return 0
        
    def move(self,xoffset,yoffset):
      Map = gamemap.getmap()
      if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
        Map[self.y][self.x].occupants.remove(self)
        self.x += xoffset
        self.y += yoffset
        Map[self.y][self.x].occupants.append(self)
        
        
        player = getplayer()
        gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),getplayer().viewrestrict))
        return 1
      else:
        return 0
    
    def attack(self, target, damage, col):
        target.health -= damage
        renderer.flash(target,col)
        if target.health <= -2:
            print(target.name, " is destroyed!")
            entitylist.remove(target)
            Map = gamemap.getmap()
            Map[target.y][target.x].occupants.remove(target)
            player = getplayer()
            gamemap.setmap(state.update_visibility(Map, player.x, player.y, gamemap.getwidth(), gamemap.getheight(),getplayer().viewrestrict))
            return 1
        elif target.health <= 0:
            print(target.name, " is dead!")
            target.name = target.name + "'s corpse"
            target.speed = 0
            target.initiative = 0
            target.ap = 0
            target.char = "%"
            
        else:
            print(target.name, "'s health is now ", target.health)

        return 1
    
    def heal(self,amount):
        self.health = min(self.health+amount, self.maxhealth)

class Enemy(Entity):
    def __init__(self, name, x, y, health, char, colour,initiative):
        Entity.__init__(self, name, x, y, health, char, colour)
        self.initiative = initiative
        self.ap = random.randint(0,initiative)
        self.sentient = True
        self.blocking = True

    def take_action(self):
        player = getplayer()
        dist = raycaster.distance(self.x, self.y, player.x, player.y)
        if dist < 1.5 and self.health > 0:
            self.attack(player, 4, red)
        elif dist < 10 and self.health > 0:
            x,y = direction(self.x, self.y, player.x, player.y)
            self.move(x*self.speed,y*self.speed)
        #print("Entity: I took an action!")
        return 1
    
class Player(Entity):
    def __init__(self, name, x, y, health, char, colour, initiative):
        Entity.__init__(self, name, x, y, health, char, colour)
        self.mana = 20
        self.maxmana = 20
        self.initiative = initiative
        self.ap = 0
        self.viewrestrict = 10
        self.sentient = True
        self.blocking = True
        self.inventory = []
        
    def take_action(self):
        action = False
        while action != True:
            pygame.time.delay(100)
            pygame.event.wait()
            returncode = input_handler.handle(self)
            if returncode == 1:
                action = True
            elif returncode == 2:
                return 2
        print("Player: I took an action!")
        return 1
        
    def move(self,xoffset,yoffset):
        Map = gamemap.getmap()
        if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
            Map[self.y][self.x].occupants.remove(self)
            self.x += xoffset*self.speed
            self.y += yoffset*self.speed
            Map[self.y][self.x].occupants.append(self)
            gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
            return 1

        elif Map[self.y+yoffset][self.x+xoffset].occupants != [] and self.health > 0:
            self.attack(Map[self.y+yoffset][self.x+xoffset].occupants[0], 2, lightblue)
            return 1
        elif self.health > 0:
            print("The way is blocked")
            return 0
        else:
            print("You are dead. Act like it.")
            
    def stair(self):
        Map = gamemap.getmap()
        width = gamemap.getwidth()
        height = gamemap.getheight()
        if Map[self.y][self.x].name == "stairs":
            self.x = random.randint(10, width-10)
            self.y = random.randint(10, height-10)
            global entitylist
            entitylist = [self]
            Map = gamemap.setup(width, height, self.x, self.y)
            Map[self.y][self.x].occupants.append(self)
            return 2
        else:
            print("You are not above a way down")
            return 0
            
    def pickup(self):
        Map = gamemap.getmap()
        for i in range(len(Map[self.y][self.x].occupants)):
            current = Map[self.y][self.x].occupants[i]
            if current.pickupable == True:
                Map[self.y][self.x].occupants.pop(i)
                entitylist.remove(current)
                self.inventory.append(current)
                print("Picked up", current.name)
                print(self.inventory)
                gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight(),self.viewrestrict))
                return 1
        return 0
            
def create_entity(name: str, x: int, y: int, health: int, char: str, colour):
    global entitylist
    newEntity = Entity(name, x, y, health, char, colour)
    entitylist.insert(0,newEntity)
    return newEntity

def create_enemy(name: str, x: int, y: int, health: int, char: str, colour, initiative):
    global entitylist
    newEnemy = Enemy(name, x, y, health, char, colour, initiative)
    entitylist.insert(0,newEnemy)
    return newEnemy

def create_player(name: str, x: int, y: int, health: int, char: str, colour, initiative):
    global entitylist
    newPlayer = Player(name, x, y, health, char, colour, initiative)
    entitylist.insert(0,newPlayer)
    return newPlayer

def getentities():
    return entitylist

def getplayer():
    return entitylist[len(entitylist)-1]


def detectcollision(x,y,Map):
    if Map[y][x].walkable == True:
        if Map[y][x].occupants != []:
            for i in range(len(Map[y][x].occupants)):
                if Map[y][x].occupants[i].blocking == True:
                    return True
        return False
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
