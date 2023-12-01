#!/usr/bin/python3
# coding: utf-8

import pygame
import os
from sprites import *
from config import *

"""
    pygame_code-skeleton.py 2.0 - Some Pygame code to build from there.

    Copyright (C) 2023 Hauke Lubenow

    This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

class Game:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(WINDOWPOSITION_X) + ", " + str(WINDOWPOSITION_Y)
        pygame.init()
        self.screen = pygame.display.set_mode((SSIZE_SCREEN_X * SCALEFACTOR, SSIZE_SCREEN_Y * SCALEFACTOR))
        pygame.display.set_caption("Hello Ball")
        self.ih = InputHandler(True)
        self.clock = pygame.time.Clock()
        self.initSprites()
        self.running = True
        while self.running:
            self.clocktick = self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
        pygame.quit()

    def initSprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.player      = Player("player", 1, self, 10, 10, 130, 100, "red", speed = 0.15)

Game()
