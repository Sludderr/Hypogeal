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
mint = colourdict["mint"]
camel = colourdict["camel"]

def setup(width, height):
    global Map
    Map = [[Tile_Floor("floor",x,y,camel) for x in range(width)] for y in range(height)]
    Map[12][5] = Tile_Wall("wall",5,12,white)
    Map[12][6] = Tile_Wall("wall",6,12,white)
    Map[12][7] = Tile_Wall("wall",7,12,white)
    Map[12][8] = Tile_Wall("wall",8,12,white)
    for x in range(width):
        Map[0][x] = Tile_Wall("boundary", x, 0, mint)
    for x in range(width):
        Map[height-1][x] = Tile_Wall("boundary", x, height-1, mint)
    for y in range(height):
        Map[y][0] = Tile_Wall("boundary", 0, y, mint)
    for y in range(height):
        Map[y][width-1] = Tile_Wall("boundary", width-1, y, mint)
    
    
    
    return Map

def getmap():
    global Map
    return Map
