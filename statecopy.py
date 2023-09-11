def update_visibility(Map, playerx, playery):
    # iterate through map tiles within the range of the player
    for y in range(21):
        for x in range(21):
            # set first position in map
            # will only check the 20 diameter circle around the player
            ytemp = playery-10+y
            xtemp = playerx-10+x
            if insidemap(xtemp, ytempt):
                # if inside the map
                if distance(xtemp, ytemp) < 10:
                    # if within viewing distance
                    if checkadjacent() == 8 or pathdetect(Map, xtemp, ytemp) == False:
                        # if obscured or inside a wall
                        Map[ytemp][xtemp].rendered = False
                    else:
                        # otherwise render it
                        Map[ytemp][xtemp].rendered = True
                else:
                    Map[ytemp][xtemp].rendered = False
    return Map
