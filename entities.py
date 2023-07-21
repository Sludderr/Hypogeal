entitylist = []
import gamemap
import state
import pygame
import input_handler

# Global list "entitylist" holds all active entities. It will be looped through every tick to update the state of each entity


# Base class "Entity".
class Entity():
    def __init__(self, name, x, y, char, colour, viewrestrict, initiative):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.viewrestrict = viewrestrict
        self.speed = 1
        self.initiative = initiative
        self.ap = 0
    def move(self,xoffset,yoffset):
      Map = gamemap.getmap()
      if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
        self.x += xoffset
        self.y += yoffset
        gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight()))
        return True
      else:
        print("The way is blocked")
        return False
    def take_action(self):
        print("Entity: I took an action!")

class Player(Entity):
    def __init__(self, name, x, y, char, colour, viewrestrict, initiative):
        Entity.__init__(self, name, x, y, char, colour, viewrestrict, initiative)

    def take_action(self):
        action = False
        while action != True:
            pygame.time.delay(100)
            pygame.event.wait()
            if input_handler.handle(self) == True:
                action = True
        print("Player: I took an action!")
        
def create_entity(name: str, x: int, y: int, char: str, colour, viewrestrict, initiative):
    global entitylist
    newEntity = Entity(name, x, y, char, colour, viewrestrict, initiative)
    entitylist.insert(0,newEntity)
    return newEntity

def create_player(name: str, x: int, y: int, char: str, colour, viewrestrict, initiative):
    global entitylist
    newEntity = Player(name, x, y, char, colour, viewrestrict, initiative)
    entitylist.insert(0,newEntity)
    return newEntity

def getentities():
    return entitylist

def getplayer():
    return entitylist[len(entitylist)-1]


def detectcollision(x,y,Map):
    if Map[y][x].walkable == False:
        return True
