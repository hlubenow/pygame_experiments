#!/usr/bin/python
# coding: utf-8

"""
    scrollexample.py - An example of creating a scrolling background
                       in Pygame.

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

SCALEFACTOR = 2
TILESIZE    = 25

if os.name == "posix":
    FONTNAME    = "Sans"
else:
    FONTNAME    = "Arial"

FPS = 50

COLORS = {"black"      : (0, 0, 0),
          "darkgrey"   : (76, 76, 76),
          "grey"       : (140, 140, 140),
          "lightgrey"  : (220, 220, 220),
          "red"        : (204, 0, 0),
          "blue"       : (0, 0, 200),
          "darkblue"   : (0, 0, 150)}

class Map:

    def __init__(self, screenborder):
        self.screenborder       = screenborder
        self.tilespermappart    = 9
        self.mappartsx          = 3
        self.mappartsy          = 3
        self.tilemapsize        = (self.tilespermappart * self.mappartsx,
                                   self.tilespermappart * self.mappartsy)
        self.mappartwidth       = self.tilespermappart * TILESIZE * SCALEFACTOR
        self.mappartheight      = self.tilespermappart * TILESIZE * SCALEFACTOR
        self.mappart_halfwidth  = self.mappartwidth // 2
        self.mappart_halfheight = self.mappartheight // 2
        self.mapwidth           = self.mappartsx * self.mappartwidth 
        self.mapheight          = self.mappartsy * self.mappartheight
        self.lastpart_x         = self.mapwidth - self.mappartwidth
        self.lastpart_y         = self.mapheight - self.mappartheight

    def createSurface(self):
        self.surface = pygame.Surface((self.mapwidth, self.mapheight))
        self.surface = self.surface.convert()
        self.rect    = pygame.Rect(0, 0, self.mappartwidth, self.mappartheight)
        for y in range(self.mappartsy):
            for x in range(self.mappartsx):
                mappartsurface = self.getMapPartSurface(y * self.mappartsx + x + 1)
                mappartrect    = mappartsurface.get_rect()
                mappartrect.topleft = (x * self.mappartwidth, y * self.mappartheight)
                self.surface.blit(mappartsurface, mappartrect)


    def getMapPartSurface(self, mappartnumber):
        surface = pygame.Surface((self.mappartwidth, self.mappartheight))
        surface = surface.convert()
        cnum = 1
        for y in range(self.tilespermappart):
            for x in range(self.tilespermappart):
                if cnum:
                    c = COLORS["lightgrey"]
                else:
                    c = COLORS["grey"]
                pygame.draw.rect(surface,
                                 c,
                                 pygame.Rect(x * TILESIZE * SCALEFACTOR + 1,
                                             y * TILESIZE  * SCALEFACTOR + 1,
                                             TILESIZE * SCALEFACTOR - SCALEFACTOR,
                                             TILESIZE * SCALEFACTOR - SCALEFACTOR))
                cnum = 1 - cnum
                if x == 0 and y == 0:
                    font = pygame.font.SysFont(FONTNAME, 32) 
                    textsurface = font.render(str(mappartnumber), True, COLORS["red"])
                    textrect      = textsurface.get_rect()
                    textrect.topleft = (TILESIZE // 2 * SCALEFACTOR - textrect.width // 2,
                                        TILESIZE // 2 * SCALEFACTOR - textrect.width)
                    surface.blit(textsurface, textrect)
        return surface

    def move(self, player):
        self.rect.topleft = (player.x - player.drawx, player.y - player.drawy)

    def draw(self, surface):
        # Most important line for scrolling background:
        surface.blit(self.surface, (self.screenborder[0] // 2, self.screenborder[1] // 2), self.rect)


class Player:

    def __init__(self, map, screenborder):
        self.map          = map
        self.screenborder = screenborder
        self.radius       = 6
        self.createSurface()
        """ (self.x, self.y), (self.drawx, self.drawy) refer to the topleft
            of the surface. Adjustments due to the size of the circle are
            made only just before drawing or moving. Otherwise also the
            moving map would get confused.
        """
        self.x = self.map.mappartsx // 2 * self.map.mappartwidth + self.map.mappart_halfwidth
        self.y = self.map.mappartsy // 2 * self.map.mappartwidth + self.map.mappart_halfheight
        self.drawx = self.x
        self.drawy = self.y
        self.speed  = 3
        self.setDrawCoordinates()
        self.map.move(self)

    def createSurface(self):

        self.surface = pygame.Surface((self.radius * 2 * SCALEFACTOR,
                                       self.radius * 2 * SCALEFACTOR))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(COLORS["black"])
        self.rect    = self.surface.get_rect()
        pygame.draw.circle(self.surface,
                           COLORS["blue"],
                           (self.radius * SCALEFACTOR, self.radius * SCALEFACTOR),
                           self.radius * SCALEFACTOR)

    def printPosition(self):
        print self.x, self.y
        print self.drawx, self.drawy
        print

    def setDrawCoordinates(self):

        if self.x < self.map.mappart_halfwidth:
            self.drawx = self.x

        elif self.x >= self.map.mappart_halfwidth and self.x < self.map.lastpart_x + self.map.mappart_halfwidth:
            self.drawx = self.map.mappart_halfwidth
        else:
            self.drawx = self.x - self.map.lastpart_x

        if self.y < self.map.mappart_halfheight:
            self.drawy = self.y

        elif self.y >= self.map.mappart_halfheight and self.y < self.map.lastpart_y + self.map.mappart_halfheight:
            self.drawy = self.map.mappart_halfheight
        else:
            self.drawy = self.y - self.map.lastpart_y

        self.rect.topleft = (self.drawx + self.screenborder[0] // 2 - self.radius * SCALEFACTOR, self.drawy + self.screenborder[1] // 2 - self.radius * SCALEFACTOR)

    def move(self, movement):

        m = self.speed * SCALEFACTOR
        r = self.radius * SCALEFACTOR

        if movement == "left":
            if self.x > m + r:
                self.x -= m
            else:
                self.x = r

        if movement == "right":
            if self.x < self.map.mapwidth - r:
                self.x += m
            else:
                self.x = self.map.mapwidth - r

        if movement == "up":
            if self.y > m + r:
                self.y -= m
            else:
                self.y = r

        if movement == "down":
            if self.y < self.map.mapheight - r:
                self.y += m
            else:
                self.y = self.map.mapheight - r

        self.setDrawCoordinates()
        self.map.move(self)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Main:

    def __init__(self):

        self.screenborder = (100 * SCALEFACTOR, 50 * SCALEFACTOR)
        self.map = Map(self.screenborder)

        self.movements = {  pygame.K_LEFT   : "left",
                            pygame.K_RIGHT  : "right",
                            pygame.K_UP     : "up",
                            pygame.K_DOWN   : "down" }
         
        os.environ['SDL_VIDEO_WINDOW_POS'] = "226, 65"
        self.screen = pygame.display.set_mode((self.screenborder[0] + self.map.mappartwidth, self.screenborder[1] + self.map.mappartheight))
        pygame.display.set_caption("Scrolling Background Example")
        pygame.init()
        self.map.createSurface()
        self.player = Player(self.map, self.screenborder)
        self.running = True
        self.clock = pygame.time.Clock()

        while self.running:
            self.clock.tick(FPS)
            self.screen.fill(COLORS["darkblue"])
            if self.processEvents() == "quit":
                self.running = False
            self.map.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def processEvents(self):

        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]:
            return "quit"
        for i in self.movements.keys():
            if pressed[i]:
                self.player.move(self.movements[i])
        return 0

Main()
