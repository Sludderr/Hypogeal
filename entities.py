entitylist = []

class Entity():
    def __init__(self, name, x, y, char, colour):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.speed = 1
        
def create_entity(name: str, x: int, y: int, char: str, colour):
    global entitylist
    newEntity = Entity(name, x, y, char, colour)
    entitylist.insert(0,newEntity)
    return newEntity

def getentities():
    return entitylist

def getplayer():
    return entitylist[len(entitylist)-1]
