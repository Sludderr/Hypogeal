def update(screen, font, width, height):
    screen.fill(black)
    player = entities.getplayer()
    entitylist = entities.entitylist
    
    Map = gamemap.getmap()
    # Iterate through every tile of the map
    for y in range(height):
        for x in range(width):
            CurrentTile = Map[y][x]
            # border is always visible so handle seperately
            if CurrentTile.name == "border":
                CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                text = font.render(CurrentTile.char, True, CurrentTile.colour)
                screen.blit(text, CurrentTilePos)
            else:
                # If using dev mode
                if player.viewrestrict == 0:
                    if CurrentTile.visible == True:
                        # scale tile sizes up to "pixel sizes". One tile is 16x16 pixels
                        CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                        # create the text to be rendered using the entity info
                        text = font.render(CurrentTile.char, True, CurrentTile.colour)
                        screen.blit(text, CurrentTilePos)
                # If the current tile should be rendered
                elif CurrentTile.rendered == True:
                    # Scale tile sizes up to "pixel sizes". One tile is 16x16 pixels
                    CurrentTilePos = (CurrentTile.x * 16, CurrentTile.y * 16)
                    # Create the text to be rendered using the entity info
                    text = font.render(CurrentTile.char, True, CurrentTile.colour)
                    screen.blit(text, CurrentTilePos)
