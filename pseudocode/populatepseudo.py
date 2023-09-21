def populate(Map, width, height):
    # number of entities placed so far
    total = 0
    limit = random.randint(5, 20) # how many entities to add to the map.
    # while the number of entities hasn't been met
    while total < limit:
        # random location inside the map
        curx = random.randint(3,width-3)
        cury = random.randint(3,height-3)
        if Map[cury][cury].walkable == True:
            # if the tile is walkable then an entity can be spawned on it
            total += 1
            # create an entity using the entities module. This just creates the object and adds it to the entity list
            entities.create_entity("Dummy", curx, cury, "$", red, 0, 30)
            # name = Dummy
            # xpos = random x position
            # ypos = random y position
            # char = $
            # colour = red
            # ap = 0
            # initiative = 30
    return Map
