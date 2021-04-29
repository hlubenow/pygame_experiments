vintageinput.py 1.0 - Creates an 8-bit style text input environment in Pygame
-------------------------------------------------------
#### License stuff:

Program-code: Copyright (C) 2021 hlubenow. License: GNU GPL, version 3.

The image-file "ZX_Spectrum_character_set.png" was redistributed from [Wikipedia](https://commons.wikimedia.org/wiki/File:ZX_Spectrum_character_set.png) (CC0-license).

The ZX Spectrum font is part of the ZX Spectrum's ROM, which is (C) Amstrad, 1986. Amstrad kindly have generally given permission for the redistribution of their copyrighted material but retain their copyright, as declared in [this message](https://groups.google.com/g/comp.sys.amstrad.8bit/c/HtpBU2Bzv_U/m/HhNDSU3MksAJ).

My script doesn't contain font- or other ROM code.

The file "sound/click.wav" was sampled from the Spectrum emulator "fuse".

-------------------------------------------------------
#### Description:

The script creates a vintage-, 8-bit style text input environment/user interface in Python/Pygame.
At the moment, this is "only" the input routine. So you can type in something, and always just get the message "READY".
Nothing more happens at the moment. But from here, I could for example write a Basic interpreter or a text adventure game
in this style. With a little effort, I could also split the screen into a text display area and a text input area,
like it could be seen in a number of adventure games of the time, including "The Hobbit" and "Sherlock" on the ZX Spectrum.
As this is a Pygame window, it would also be possible to display graphics. But this is also not implemented yet,
and I'm not much of a painter, really.
