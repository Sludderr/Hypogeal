entitylist = []

class Entity():
    def __init__(self, name, x, y, char):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.speed = 16
        
def create_entity(name: str, x: int, y: int, char: str):
    global entitylist
    newEntity = Entity(name, x, y, char)
    entitylist.append(newEntity)
    return newEntity
