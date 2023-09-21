def setup(width, height):
    global Map

    # Initialise 2D array of floor objects
    Map = NewArray(width,height,floor("floor",x,y))

    # Procedural Generation Algorithm
    Map = drunkardwalk(Map, width, height)

    # Populate with entities
    Map = populate(Map, width, height)

    # Set the border to '#'s
    for x in range(width):
        Map[0][x] = wall("border",x,0)
        Map[height-1][x] = wall("border",x,height-1)
    for y in range(width):
        Map[y][0] = wall("border",0,y)
        Map[y][width-1] = wall("border",width-1,y)
    
    return Map
  
