#!/usr/bin/python
# coding: utf-8

"""
    horizontal_starfield.py 1.0 - Creates a horizontal starfield in Pygame, as seen
                                  in one of my favourite games on the Amiga.

    Copyright (C) 2021 hlubenow

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

import pygame
import os
import random

SCALEFACTOR = 3
FPS         = 50
SPEEDSETTING = 0

STARS_PER_GROUP = 30

BLACK = (0, 0, 0)

class Environment:

    def __init__(self):
        self.paperwidth      = 320
        self.paperheight     = 192
        self.pc_paperwidth   = self.paperwidth  * SCALEFACTOR
        self.pc_paperheight  = self.paperheight * SCALEFACTOR
        self.borderwidth     = 24
        self.borderheight    = 12
        self.pc_borderwidth  = self.borderwidth * SCALEFACTOR
        self.pc_borderheight = self.borderheight * SCALEFACTOR
        self.screenwidth     = self.pc_paperwidth + 2 * self.pc_borderwidth
        self.screenheight    = self.pc_paperheight + 2 * self.pc_borderheight

class Star:

    def __init__(self, env_, color, position, delay, accel):
        self.env_      = env_
        self.surface   = pygame.Surface((SCALEFACTOR, SCALEFACTOR))
        self.surface   = self.surface.convert()
        self.rect      = self.surface.get_rect()
        self.posx      = position[0]
        self.initposx  = self.posx
        self.posy      = position[1]
        self.delaytime = delay + SPEEDSETTING 
        self.accel     = accel
        self.surface.fill(color)
        self.timer     = pygame.time.get_ticks()

    def inScreenRange(self):
        # Only draw stars, when they're on the "paper" (= insider the border):
        if self.posx <= self.env_.pc_borderwidth + self.env_.pc_paperwidth and self.posx >= self.env_.pc_borderwidth:
            return True
        else:
            return False
 
    def moveLeft(self, currenttime):
        if currenttime - self.timer < self.delaytime:
            return
        self.posx -= self.accel * SCALEFACTOR
        if self.posx < 0:
            self.posx = self.initposx
        self.rect.topleft = (self.posx, self.posy)
        self.timer = currenttime

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Main:

    def __init__(self):
        self.env_  = Environment()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "78, 2"
        pygame.init()
        self.screen = pygame.display.set_mode((self.env_.screenwidth, self.env_.screenheight))
        pygame.display.set_caption("Horizontal Starfield")
        self.clock = pygame.time.Clock()
        self.createStarfield()
        self.running = True

        while self.running:
            self.clock.tick(FPS)
            self.timer = pygame.time.get_ticks()
            if self.processEvents() == "quit":
                self.running = False
            self.screen.fill(BLACK)
            for star in self.starfield:
                star.moveLeft(self.timer)
                if star.inScreenRange():
                    star.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def createStarfield(self):
        self.starfield = []
        colors = []
        for i in (85, 119, 187, 255):
            colors.append((i, i, i))
        delays = (100, 50, 20, 0)
        accel  = (2, 2, 2, 2)
        h = {}
        for g in range(4):
            for n in range(STARS_PER_GROUP):
                # Start stars one screen-size right to the visible screen:
                x = self.env_.screenwidth + random.randrange(self.env_.screenwidth)
                y = self.env_.pc_borderheight + random.randrange(self.env_.pc_paperheight)
                # Every star should have its own y-coordinate:
                while y in h:
                    y = self.env_.pc_borderheight + random.randrange(self.env_.pc_paperheight)
                h[y] = 1
                self.starfield.append(Star(self.env_, colors[g], (x, y), delays[g], accel[g]))

    def processEvents(self):
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]:
            return "quit"
        return 0

Main()
