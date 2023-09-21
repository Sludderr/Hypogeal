def update(screen, width, height):
    # Fill the screen with black
    screen.fill(black)
    # Get the entities from the entity module
    player = entities.getplayer()
    entitylist = entities.entitylist

    # Get the current map from the gamemap module
    Map = gamemap.getmap()
    # Iterate through every tile of the map
    for y in range(height):
        for x in range(width):
            CurrentTile = Map[y][x]
            # border is always visible so handle seperately
            if CurrentTile.name == "border":
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                output(CurrentTile.char, CurrentTile.colour, CurrentTilePos)
            # If the current tile should be rendered
            elif CurrentTile.rendered == True:
                # Scale tile sizes up to "pixel sizes". One tile is 16x16 pixels
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                output(CurrentTile.char, CurrentTile.colour, CurrentTilePos)

    # Loop through all active entities and render them ontop of the tiles. 
    for i in range(len(entitylist)):
        CurrentEntity = entitylist[i]
        # If on a rendered tile
        if Map[CurrentEntity.y][CurrentEntity.x].rendered == True:
            CurrentEntityPos = (CurrentEntity.x * 16, CurrentEntity.y * 16)
            output(CurrentEntity.char, CurrentEntity.colour, CurrentEntityPos)

    # Update the pygame display- output it. 
    pygame.display.update()
    
