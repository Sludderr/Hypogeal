def drunkardwalk(Map, width, height):
    # Iterate through each tile of the Map and set every tile to a wall
    for y in range(height):
        for x in range(width):
            Map[y][x] = wall("wall",x,y)
    total = 0 # Number of tiles placed
    limit = random.randint(700,1300)
    border = random.randint(3, 8) # Random border width
    # Until the number of tiles placed meets the random total (creates variety in the types of map)
    while total <= limit:
        # tunnel out a floor tile
        if Map[drunky][drunkx].name == "wall":
            Map[drunky][drunkx] = floor("floor",drunkx,drunky)
            total += 1
        # Choose a random direction
        rand = random.randint(1,4)
        if rand == 1:
            drunky -= 1  # Go North
        if rand == 2:
            drunkx += 1  # Go East
        if rand == 3:
            drunky += 1  # Go South
        if rand == 4:
            drunkx -= 1  # Go West
    for y in range(height):
        for x in range(width):
            # number of surrounding wall tiles
            surrounding = checkadjacent(Map, width, height)
            if surrounding <= 1:
                # Cull small groups of tiles
                Map[y][x] = floor("floor",x,y)
            elif surrounding == 8:
                # black out totally invisible tiles (surrounded on all sides)
                Map[y][x].visible = False
    return Map
