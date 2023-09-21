entitylist = []
import gamemap
import state
import pygame
import input_handler
import raycaster
import random

# Global list "entitylist" holds all active entities. It will be looped through every tick to update the state of each entity



class Tile():
    def __init__(self, name, x, y, char, colour, walkable, visible, rendered):
        self.name = name
        self.x = x
        self.y = y
        self.char = char # String, the character used to represent the tile. E.g. # for walls, ~ for floors.
        self.colour = colour
        self.walkable = walkable # Bool, whether the tile can be walked over
        self.visible = visible # Bool, whether the tile is actually rendered- off for tiles completely obscured (surrounded by 8 walls). This saves processing time in not bothering to process rendering for them
        self.rendered = rendered # Bool, whether the tile is currently rendered
        self.occupants = [] # Stores pointers to all entities in this tile
  
class Tile_Floor(Tile): # This subclass defaults certain attributes for a floor tile.
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "~", colour, True, True, False)
        
class Tile_Wall(Tile): # This subclass defaults certain attibutes for a wall tile.
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "#", colour, False, True, False)

# Base class "Entity".
class Enemy(Entity):
    def __init__(self, name, x, y, health, char, colour, initiative):
        Entity.__init__(self,name,x,y,health,char,colour)
        self.initiative = initiative # Extra attributes for enemy- they can take turns
        self.ap = 0 # AP starts a 0 for all enemies
    def take_action(self):
        dist = distance(self.x, self.y, player.x, player.y) # Euclidean distance to player
        if dist < 1.5 and self.health > 0: # If the entity is alive and within reach of the player, the enemy attacks
            self.attack(player)
        elif dist < 10 and self.health > 0: # if within "sensing" range, move towards player.
            x,y = Astar(Map[self.y][self.x],Map[player.y][player.x]) # get route to take
            self.move(x,y) # move the entity
        return True # action taken, so return true to the Turn Handler. The enemies' ap will be reset.
    def attack(self, target):
        if target.health > 0: # if the target isn't dead/destroyed
            target.health -= 1 # take away health
            if target.health == 0: # entity has been killed! Remove it's ability to take actions.
                print(target.name, " is dead!")
                target.name = target.name + "'s corpse"
                target.initiative = 0
                target.ap = 0
                target.char = "%" # change character to reflect deadness
            else:
                print(target.name, "'s health is now ", target.health)
        else:
            print(target.name, " is dead")
        return True # action taken, so return True to Turn Handler.

class Player(Entity):
    def __init__(self, name, x, y, health, char, colour, initiative):
        Entity.__init__(self, name, x, y, health, char, colour)

    def take_action(self): # take_action method is different for the player than the enemies.
        action = False
        while action != True: # Until the Input Handler recieves a valid input.
            pygame.time.delay(100) # Limits fps and stops input buffering which would lag the game.
            pygame.event.wait() # Wait for a user input
            if input_handler.handle(self) == True: # If a valid action was taken
                action = True
        print("Player: I took an action!")
        
    def move(self,xoffset,yoffset):
        Map = gamemap.getmap()
        if detectcollision(self.x+xoffset, self.y+yoffset,Map) != True:
            Map[self.y][self.x].occupants.remove(self)
            self.x += xoffset
            self.y += yoffset
            Map[self.y][self.x].occupants.append(self)
            gamemap.setmap(state.update_visibility(Map, self.x, self.y, gamemap.getwidth(), gamemap.getheight())
            return True # Valid Action
        elif Map[self.y+yoffset][self.x+xoffset].occupants != [] and self.health > 0: # if there's another entity in there, attack instead of move
            self.attack(Map[self.y+yoffset][self.x+xoffset].occupants[0])
            return True
        elif self.health > 0: # The failed move is due to blockage
            print("The way is blocked")
            return False
        else:
            print("You are dead. Act like it.") # The failed move is due to the player being dead
            
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
