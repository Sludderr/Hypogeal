import gamemap
import colours
import random
import entities

colourdict = colours.getcolours() 

white = colourdict["white"]
mint = colourdict["mint"]
camel = colourdict["camel"]
red = colourdict["red"]

def checkadjacent(Map, width, height, x, y, nametag, altnametag):
    count = 0

    # Check cardinal directions
    
    # North
    if y != 0 and (Map[y-1][x].name == nametag or Map[y-1][x].name == altnametag):
        count += 1
    # North-East
    if y != 0 and x != width-1 and (Map[y-1][x+1].name == nametag or Map[y-1][x+1].name == altnametag):
        count += 1
    # East
    if x != width-1 and (Map[y][x+1].name == nametag or Map[y][x+1].name == altnametag):
        count += 1
    # South-East
    if x != width-1 and y != height-1 and (Map[y+1][x+1].name == nametag or Map[y+1][x+1].name == altnametag):
        count += 1
    # South
    if y != height-1 and (Map[y+1][x].name == nametag or Map[y+1][x].name == altnametag):
        count += 1
    # South-West
    if y != height-1 and x != 0 and (Map[y+1][x-1].name == nametag or Map[y+1][x-1].name == altnametag):
        count += 1
    # West
    if x != 0 and (Map[y][x-1].name == nametag or Map[y][x-1].name == altnametag):
        count += 1
    # North-West
    if y != 0 and x != 0 and (Map[y-1][x-1].name == nametag or Map[y-1][x-1].name == altnametag):
        count += 1
    
    return count
    


def drunkardwalk(Map, width, height, startx, starty):
    # Iterate through each tile of the Map
    for y in range(height):
        for x in range(width):
            Map[y][x] = gamemap.Tile_Wall("wall",x,y,mint)
            # Set every tile to a wall
    drunkx = startx
    drunky = starty
    # Number of tiles placed
    total = 0
    limit = random.randint(700,1300)
    # Random border width
    border = random.randint(3, 8)
    # Until the number of tiles placed meets the random total (creates variety in the types of map)
    while total <= limit:
        if Map[drunky][drunkx].name == "wall":
            Map[drunky][drunkx] = gamemap.Tile_Floor("floor",drunkx,drunky,camel)
            total += 1

        # Choose a random direction
        rand = random.randint(1,4)
        
        if rand == 1 and drunky > border and drunkx < width-(border+1) and drunkx > border:
            # Go North
            drunky -= 1
        if rand == 2 and drunkx < width-(border+1) and drunky > border and drunky < height-(border+1):
            # Go East
            drunkx += 1
        if rand == 3 and drunky < height-(border+1) and drunkx < width-(border+1) and drunkx > border:
            # Go South
            drunky += 1
        if rand == 4 and drunkx > border and drunky > border and drunky < height-(border+1):
            # Go West
            drunkx -= 1
            
    for y in range(height):
        for x in range(width):
            surrounding = checkadjacent(Map, width, height, x, y, "wall", "")
            
            if surrounding <= 1:
                # Cull small groups of tiles
                Map[y][x] = gamemap.Tile_Floor("floor",x,y,camel)
                
            elif surrounding == 8:
                # black out totally invisible tiles (surrounded on all sides)
                Map[y][x].visible = False
    
    return Map


def populate(Map, width, height, startx,starty):
    total = 0
    limit = random.randint(0, 20)
    while total < limit:
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
        if Map[cury][cury].walkable == True:
            total += 1
            entities.create_entity("Dummy", curx, cury, "$", red, 0, 30)
    
    
    return Map
