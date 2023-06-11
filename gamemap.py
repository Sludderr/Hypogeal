import colours
import procgeneration
import random
import state

colourdict = colours.getcolours() 

class Tile():
    def __init__(self, name: str, x, y, char: str, colour, walkable: bool, visible, rendered):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.walkable = walkable
        self.visible = visible
        self.rendered = rendered

class Tile_Floor(Tile):
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "~", colour, True, True, False)
        
class Tile_Wall(Tile):
    def __init__(self, name, x, y, colour):
        Tile.__init__(self, name, x, y, "#", colour, False, True, False)

white = colourdict["white"]
mint = colourdict["mint"]
camel = colourdict["camel"]
darkslate = colourdict["darkslate"]

def setup(widther, heighter, startx, starty):
    global Map
    global width
    global height
    
    width = widther
    height = heighter
    
    Map = [[Tile_Floor("floor",x,y,camel) for x in range(width)] for y in range(height)]
    Map = procgeneration.drunkardwalk(Map, width, height, startx, starty)
    
    for x in range(width):
        Map[0][x] = Tile_Wall("border",x,0,darkslate)
        Map[height-1][x] = Tile_Wall("border",x,height-1,darkslate)
    for y in range(width):
        Map[y][0] = Tile_Wall("border",0,y,darkslate)
        Map[y][width-1] = Tile_Wall("border",width-1,y,darkslate)
    
    Map = state.update_visibility(Map, startx, starty, width, height)
    
    return Map

def getmap():
    global Map
    return Map

def setmap(Maptemp):
    global Map
    Map = Maptemp
    
def getwidth():
    global width
    return width

def getheight():
    global height
    return height

