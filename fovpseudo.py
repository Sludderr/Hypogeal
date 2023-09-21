def pathdetect(Map, startx, starty, destx, desty):
    # While the player tile hasn't been reached and the current tile isn't a wall (collision). If the current space lands on a wall, then the tile is obscured from the player
    while (startx != destx or starty != desty) and Map[starty][startx].name != "wall":
        # get the euclidean distance to the playertile from each surrounding tile
        ndist = distance(startx, starty-1, destx, desty)
        nedist = distance(startx+1, starty-1, destx, desty)
        # etc.. for all 8 directions
        # If North is closest, go North
        if ndist < nedist and ndist < edist and ndist < sedist and ndist < sdist and ndist < swdist and ndist < wdist and ndist < nwdist:
            starty -= 1
        # If North-East is closest, go North-East
        elif nedist < edist and nedist < sedist and nedist < sdist and nedist < swdist and nedist < wdist and nedist < nwdist:
            starty -= 1
            startx += 1
        # If East is closest, go East
        elif edist < sedist and edist < sdist and edist < swdist and edist < wdist and edist < nwdist:
            startx += 1
        # If South-East is closest, go South-East
        elif sedist < sdist and sedist < swdist and sedist < wdist and sedist < nwdist:
            starty += 1
            startx += 1
        # If South is closest, go South
        elif sdist < swdist and sdist < wdist and sdist < nwdist:
            starty += 1
        # If South-West is closest, go South-West
        elif swdist < wdist and swdist < nwdist:
            starty += 1
            startx -= 1
        # If West is closest, go West
        elif wdist < nwdist:
            startx -= 1
        # If North-West is closest, go West
        else:
            starty -= 1
            startx -= 1
    if startx != destx or starty != desty:     # if not the destination tile, return False. The tile is obscured.
        return False
    else:
        return True
