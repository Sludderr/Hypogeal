import colours
import procgeneration

colourdict = colours.getcolours() 

class Tile():
    def __init__(self, name: str, x, y, char: str, colour, walkable: bool, visible):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.walkable = walkable
        self.visible = visible

class Tile_Floor(Tile):
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "~", colour, True, True)
        
class Tile_Wall(Tile):
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "#", colour, False, True)

white = colourdict["white"]
mint = colourdict["mint"]
camel = colourdict["camel"]

def setup(width, height):
    global Map
    Map = [[Tile_Floor("floor",x,y,camel) for x in range(width)] for y in range(height)]
    Map = procgeneration.drunkardwalk(Map, width, height)
    
    return Map

def getmap():
    global Map
    return Map
