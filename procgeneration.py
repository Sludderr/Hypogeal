import gamemap
import colours
import random

colourdict = colours.getcolours() 

white = colourdict["white"]
mint = colourdict["mint"]
camel = colourdict["camel"]


def checkadjacent(Map, width, height, x, y, nametag, altnametag):
    count = 0
    
    if y != 0 and (Map[y-1][x].name == nametag or Map[y-1][x].name == altnametag):
        count += 1
    if y != 0 and x != width-1 and (Map[y-1][x+1].name == nametag or Map[y-1][x+1].name == altnametag):
        count += 1
    if x != width-1 and (Map[y][x+1].name == nametag or Map[y][x+1].name == altnametag):
        count += 1
    if x != width-1 and y != height-1 and (Map[y+1][x+1].name == nametag or Map[y+1][x+1].name == altnametag):
        count += 1
    if y != height-1 and (Map[y+1][x].name == nametag or Map[y+1][x].name == altnametag):
        count += 1
    if y != height-1 and x != 0 and (Map[y+1][x-1].name == nametag or Map[y+1][x-1].name == altnametag):
        count += 1
    if x != 0 and (Map[y][x-1].name == nametag or Map[y][x-1].name == altnametag):
        count += 1
    if y != 0 and x != 0 and (Map[y-1][x-1].name == nametag or Map[y-1][x-1].name == altnametag):
        count += 1
    
    return count
    


def drunkardwalk(Map, width, height, startx, starty):
    for y in range(height):
        for x in range(width):
            Map[y][x] = gamemap.Tile_Wall("wall",x,y,mint)
    drunkx = startx
    drunky = starty
    limit = 0
    border = random.randint(2, 8)
    while limit <= random.randint(700,1300):
        if Map[drunky][drunkx].name == "wall":
            Map[drunky][drunkx] = gamemap.Tile_Floor("floor",drunkx,drunky,camel)
            limit += 1
            
        rand = random.randint(1,4)
        if rand == 1 and drunky > border and drunkx < width-(border+1) and drunkx > border:
            drunky -= 1
        if rand == 2 and drunkx < width-(border+1) and drunky > border and drunky < height-(border+1):
            drunkx += 1
        if rand == 3 and drunky < height-(border+1) and drunkx < width-(border+1) and drunkx > border:
            drunky += 1
        if rand == 4 and drunkx > border and drunky > border and drunky < height-(border+1):
            drunkx -= 1
            
    for y in range(height):
        for x in range(width):
            surrounding = checkadjacent(Map, width, height, x, y, "wall", "")
            
            if surrounding <= 1:
                Map[y][x] = gamemap.Tile_Floor("floor",x,y,camel)
                
            elif surrounding == 8:
                Map[y][x].visible = False
    
    return Map
