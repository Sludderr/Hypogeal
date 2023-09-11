def drunkardwalk(Map, width, height):
    # Iterate through each tile of the Map
    for y in range(height):
        for x in range(width):
            Map[y][x] = wall("wall",x,y)
            # Set every tile to a wall
    # Number of tiles placed
    total = 0
    limit = random.randint(700,1300)
    # Random border width
    border = random.randint(3, 8)
    # Until the number of tiles placed meets the random total (creates variety in the types of map)
    while total <= limit:
        if Map[drunky][drunkx].name == "wall":
            Map[drunky][drunkx] = floor("floor",drunkx,drunky)
            total += 1
        # Choose a random direction
        rand = random.randint(1,4)
        if rand == 1:
            # Go North
            drunky -= 1
        if rand == 2:
            # Go East
            drunkx += 1
        if rand == 3:
            # Go South
            drunky += 1
        if rand == 4:
            # Go West
            drunkx -= 1
    for y in range(height):
        for x in range(width):
            surrounding = checkadjacent(Map, width, height)
            if surrounding <= 1:
                # Cull small groups of tiles
                Map[y][x] = floor("floor",x,y)
            elif surrounding == 8:
                # black out totally invisible tiles (surrounded on all sides)
                Map[y][x].visible = False
    return Map
