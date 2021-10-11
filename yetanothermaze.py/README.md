yetanothermaze.py 1.1 - Pygame script, that lets you walk through a 3D maze

Copyright (C) 2021, hlubenow.

License: GNU GPL (version 3 or above)

Version 1.1: Now with solid (= filled) walls.

#### Description, license notes and credits (all in one)

The image-file "ZX_Spectrum_character_set.png" was redistributed [from Wikipedia](https://commons.wikimedia.org/wiki/File:ZX_Spectrum_character_set.png) (CC0-license):

The ZX Spectrum font is part of the ZX Spectrum's ROM, which is (C) Amstrad, 1986. Amstrad have generally given permission for the redistribution of their copyrighted material but retain their copyright, as declared in [this message](https://groups.google.com/g/comp.sys.amstrad.8bit/c/HtpBU2Bzv_U/m/HhNDSU3MksAJ). I just used 5 characters here, and my code doesn't contain any font or ROM code directly.

This script in Python/Pygame lets you walk through a maze, that is visualized in 3D with simple 80s style line drawings.
The goal is to find a ladder, that then can be used to escape the maze (by pressing the space bar).

Regarding development I'm standing "on the shoulders of giants" here:

The script is hugely inspired by C code for the Atari 800 XL by Stefan Haubenthal, which can be found [here](https://atariwiki.org/wiki/Wiki.jsp?page=3dMaze).

Generating a random maze by algorithm seems to be a general problem in computer science.
I used the [Python maze generation code by 'exciteabletom'](https://github.com/exciteabletom/mazegenerator), built a class around it and edited it into my script. As this code is rather sophisticated, it would make even very large mazes possible, in which the player would get totally stuck. By default, the maze has a size of just 20x20 locations.

The ladder was my own development. There may have been such maze ladders in 1980s' games somewhere.

Sound for hitting a wall: Free software synthesizer "ZynAddSubFX".

It seems, these kind of mazes go back to a game called "[Maze War](https://en.wikipedia.org/wiki/Maze_War)", which was already created in about 1973 and ran on these large computers of universities or other institutions (model "Imlac PDS-1", a predecessor to the later "computer workstations"). That game even supported network play. Multiple players could walk through the maze and shoot each other. So in fact "Maze War" was the earliest "first-person shooter". I haven't played it though and wasn't familiar with its history, when I wrote this little project here.
