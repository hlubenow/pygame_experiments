#!/usr/bin/python3
# coding: utf-8

import pygame
import os
from inputhandler import InputHandler

"""
    pygame_code-skeleton.py 1.0 - Some Pygame code to build from there.

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

SCALEFACTOR  = 3
FPS          = 60

COLORS = {"black"   : (0, 0, 0),
          "blue"    : (0, 0, 197),
          "magenta" : (192, 0, 192),
          "red"     : (192, 0, 0),
          "green"   : (0, 192, 0),
          "cyan"    : (0, 192, 192),
          "yellow"  : (189, 190, 0),
          "white"   : (189, 190, 197),
          "gray"   :  (127, 127, 127),
          "transparent" : (0, 0, 0, 0) }

c = ("black", "blue", "red", "magenta", "green", "cyan", "yellow", "white")
COLORNRS = {}
for i in c:
    COLORNRS[i] = c.index(i)


class MySprite(pygame.sprite.Sprite):

    def __init__(self, name, id, speed):
        pygame.sprite.Sprite.__init__(self)
        self.name           = name
        self.id             = id
        self.speed          = speed
        self.image          = None
        self.rect           = None

    def setPosition(self, spos_x, spos_y):
        self.spos_x = spos_x
        self.spos_y = spos_y

    def setPCPosition(self):
        self.pcpos_x = self.spos_x * SCALEFACTOR
        self.pcpos_y = self.spos_y * SCALEFACTOR

    def getPosition(self):
        return (self.spos_x, self.spos_y)

    def draw(self, screen):
        self.setPCPosition()
        self.rect.topleft = (self.pcpos_x, self.pcpos_y)
        screen.blit(self.image, self.rect)


class Ball(MySprite):

    def __init__(self, name, id, width, height, x, y, colorname, speed):
        MySprite.__init__(self, name, id, speed)
        self.createImage(width, height, colorname)
        self.setPosition(x, y)

    def move(self, direction, ssize_screen, clocktick):
        if direction == "left":
            self.spos_x -= self.speed * clocktick
            if self.spos_x < 0:
                self.setPosition(ssize_screen[0], self.spos_y)
        if direction == "right":
            self.spos_x += self.speed * clocktick
            if self.spos_x > ssize_screen[0]:
                self.setPosition(0, self.spos_y)
        if direction == "up":
            self.spos_y -= self.speed * clocktick
            if self.spos_y < 0:
                self.setPosition(self.spos_x, ssize_screen[1])
        if direction == "down":
            self.spos_y += self.speed * clocktick
            if self.spos_y > ssize_screen[1]:
                self.setPosition(self.spos_x, 0 )

    def createImage(self, ssize_x, ssize_y, colorname):
        self.image     = pygame.Surface((ssize_x * SCALEFACTOR, ssize_y * SCALEFACTOR))
        self.image     = self.image.convert_alpha()
        self.rect      = self.image.get_rect()
        self.image.fill(COLORS["transparent"])
        pygame.draw.circle(self.image, COLORS[colorname], (self.rect.width // 2, self.rect.height // 2), self.rect.height // 2)


class BallGroup(pygame.sprite.Group):

    def __init__(self, *args):
        pygame.sprite.Group.__init__(self, *args)

    def draw(self, surface):
        for s in self.sprites():
            s.draw(surface) 

class Main:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "185, 30"
        pygame.init()
        self.ssize_screen = (256, 192) 
        self.screen = pygame.display.set_mode((self.ssize_screen[0] * SCALEFACTOR, self.ssize_screen[1] * SCALEFACTOR))
        pygame.display.set_caption("Hello Ball")
        self.ih = InputHandler(True)
        self.clock = pygame.time.Clock()
        self.initSprites()
        self.running = True
        while self.running:
            self.clocktick = self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))

            self.ballgroup.draw(self.screen)

            if self.checkInput() == "quit":
                print("Bye.")
                self.running = False
                continue
            pygame.display.flip()
        pygame.quit()

    def initSprites(self):
        self.ball = Ball("ball", 1, 10, 10, 130, 100, "red", speed = 0.15)
        self.ballgroup = BallGroup()
        self.ballgroup.add(self.ball)

    def checkInput(self):
        # "action" is a dictionary with the keys "left right up down fire quit":
        action = self.ih.getKeyboardAndJoystickAction()
        for i in action.keys():
            if i == "quit" and action[i]:
                return "quit"
            if action[i]:
                self.ball.move(i, self.ssize_screen, self.clocktick)
        return 0

Main()
