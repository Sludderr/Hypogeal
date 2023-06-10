import colours

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

def setup(width, height):
    global Map
    Map = [[Tile_Floor("floor",x,y,white) for x in range(width)] for y in range(height)]
    Map[12][5] = Tile_Wall("wall",5,12,white)
    Map[12][6] = Tile_Wall("wall",6,12,white)
    Map[12][7] = Tile_Wall("wall",7,12,white)
    Map[12][8] = Tile_Wall("wall",8,12,white)
    
    return Map

def getmap():
    global Map
    return Map
