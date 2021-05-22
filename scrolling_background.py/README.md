### scrolling_background.py

This is an example of creating scrolling game backgrounds in Pygame.

Making the background scroll while the player avatar is animated on a spot, to give the illusion of movement, is an essential programming technique, that is used in many 2D games. Think of Atari games like "River Raid" or "Dropzone", C64 games like "Uridium" or Amiga games like "Giana Sisters", "Turrican", "Hybris", "Silkworm" or "Katakis".

Considering how important that technique is, there should be many tutorials on how to do that in Pygame. But it seems, there are only a few. And it also seems, some of them don't do it right, so the result is still juddering.

I found a way that seems to work. First, we have to think a bit about what has to be done: So there's a scenery, that is larger than the screen. And there's a visible part of that scenery. This part is usually called a "viewport".

The player avatar stays at one spot in the viewport, while the background starts scrolling along in the scenery. If the end of the scenery is reached, maybe the player avatar starts walking again to the end of the viewport (and in this case also the scenery). That's the behaviour of my example script.

In my opinion the key to smooth scrolling of the background in Pygame is the possibility to pass a third argument to the `.blit()` function. That third argument defines, what area of a surface is blitted. So the code would be something like this:

    self.scenerysurface = pygame.Surface((8192, 1024))
    self.arearect = pygame.Rect((1024, 0), (640, 480))
    self.screen.blit(self.scenerysurface, (0, 0), self.arearect)

That would blit just a part of 640x480 pixels of the whole scenery surface to the main screen at position (0, 0). Pixels, that are located in the scenery surface at position (1024, 0).

By moving the area rectangle and blitting just the selected part of the scenery surface to the main screen, the scrolling of the background is created.

The scenery surface (that is much larger than the visible screen) can be created in whole before the main loop starts. Afterwards, it must be left unchanged. Especially the player avatar must not be blitted onto the scenery surface. It must be blitted either onto the main screen itself or onto another surface, that functions as a "paper" on top of the main screen. Then, the parts of the scenery surface can also be blitted onto that "paper" or onto the main screen. Of course, the order has to be the other way round: That is, first, there's there's a "paper" surface. Then the wanted part of the scenery surface is blitted onto that "paper". Then, the player avatar, enemy avatars and what else is in the foreground is blitted onto that "paper". When everything, that's supposed to be on the "paper" is in its place, the "paper" is blitted onto the main screen.

Well, just try the script. You'll see, what it can do.

License: GNU GPL version 3 (or higher)
