#!/usr/bin/python3
# coding: utf-8

import os
import math

import pygame

"""
    tangents.py 1.0 - Drawing tangents to a circle

    Copyright (C) 2026 hlubenow.
    The math ("drawTangents()") was unfortunately improved by ChatGPT.

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


#######################################

# Config:

SCALEFACTOR = 4
PLAYERSPEED = 0.08

RESX = 320
RESY = 200
RESX_PC = 1500
RESY_PC = 1000
WINDOWPOSITION_X = 175
WINDOWPOSITION_Y = 0

FPS = 60

COLORS = {"black"   : (0, 0, 0),
          "blue"    : (0, 0, 197),
          "red"     : (192, 0, 0),
          "white"   : (189, 190, 197)}

INK       = "black"
PLAYERINK = "red"

BORDERX = int((RESX_PC - RESX * SCALEFACTOR) / 2.)
BORDERY = int((RESY_PC - RESY * SCALEFACTOR) / 2.)

#######################################

# Main:

class Main:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(WINDOWPOSITION_X) + ", " + str(WINDOWPOSITION_Y)
        pygame.init()
        self.screen = pygame.display.set_mode((RESX_PC, RESY_PC))
        pygame.display.set_caption("Draw Tangents to Circle")
        self.ih = InputHandler(False)
        self.cx = 160
        self.cy = 80
        self.r  = 40
        self.px = 100
        self.py = 60
        self.initSprites()
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.clocktick = self.clock.tick(FPS)
            self.screen.fill(COLORS["white"])
            self.checkInput()
            self.player.movement(self.cx, self.cy, self.r)
            self.allSprites.update(self.screen)
            pygame.display.flip()
        pygame.quit()

    def initSprites(self):
        self.bordergroup = BorderGroup()
        self.bordergroup.add(BorderPart(RESX_PC - 2 * BORDERX, BORDERY, BORDERX, 0))
        self.bordergroup.add(BorderPart(BORDERX, RESY_PC, 0, 0))
        self.bordergroup.add(BorderPart(BORDERX, RESY_PC, RESX_PC - BORDERX, 0))
        self.bordergroup.add(BorderPart(RESX_PC - 2 * BORDERX, BORDERY, BORDERX, RESY_PC - BORDERY))
        self.bordergroup.setColor("blue")

        self.circle = Circle(self.cx, self.cy, self.r)
        self.player = Player(self, self.px, self.py, PLAYERSPEED)
        self.allSprites = AllSpritesGroup(self.bordergroup, self.circle, self.player)

    def drawLine(self, x1, y1, x2, y2):
        x1_pc = int(x1 * SCALEFACTOR + BORDERX)
        y1_pc = int(y1 * SCALEFACTOR + BORDERY)
        x2_pc = int(x2 * SCALEFACTOR + BORDERX)
        y2_pc = int(y2 * SCALEFACTOR + BORDERY)
        pygame.draw.line(self.screen, COLORS[INK], (x1_pc, y1_pc), (x2_pc, y2_pc), SCALEFACTOR)

    def checkInput(self):
        self.keyaction = self.ih.getKeyboardAndJoystickAction()
        if self.keyaction["quit"]:
            self.running = False
            return
        if self.keyaction["fire"]:
            self.drawTangents()

    def drawTangents(self):
        px = self.player.x
        py = self.player.y

        cx = self.cx
        cy = self.cy
        r = self.r

        # Vector from center of circle to point p:
        vx = px - cx
        vy = py - cy
 
        # Distance to square
        d2 = vx * vx + vy * vy

        if d2 <= r * r:
            print("Point's not outside the circle.")
            return

        # Similar part of both touching points
        faktor1 = r * r / d2

        # Part vertical to vector cp
        faktor2 = r * math.sqrt(d2 - r * r) / d2

        # First touching point
        lx = cx + faktor1 * vx - faktor2 * (-vy)
        ly = cy + faktor1 * vy - faktor2 * vx

        # Second touching point
        ax = cx + faktor1 * vx + faktor2 * (-vy)
        ay = cy + faktor1 * vy + faktor2 * vx

        self.drawLine(px, py, ax, ay)
        self.drawLine(px, py, lx, ly)
        self.drawLine(px, py, cx, cy)
        self.drawLine(lx, ly, cx, cy)
        self.drawLine(ax, ay, cx, cy)

#######################################

# Sprites:

class BorderPart(pygame.sprite.Sprite):

    def __init__(self, width, height, pc_posx, pc_posy):
        pygame.sprite.Sprite.__init__(self)
        self.image          = pygame.Surface((width, height))
        self.rect           = self.image.get_rect()
        self.rect.x         = pc_posx
        self.rect.y         = pc_posy

    def changeColor(self, colorname):
        self.image.fill(COLORS[colorname])

    def update(self, screen):
        screen.blit(self.image, self.rect)


class Circle(pygame.sprite.Sprite):

    def __init__(self, cx, cy, r):
        pygame.sprite.Sprite.__init__(self)
        self.cx   = cx
        self.cy   = cy
        self.r    = r
        self.r_pc = r * SCALEFACTOR
        self.createImage()
        self.setTopleftPosition(self.cx - self.r, self.cy - self.r)

    def createImage(self):
        self.image = pygame.Surface((self.r_pc * 2, self.r_pc * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS[INK], (self.r_pc, self.r_pc), self.r_pc, width = SCALEFACTOR)
        self.rect  = self.image.get_rect()

    def setTopleftPosition(self, x, y):
        x_pc_topleft = x * SCALEFACTOR + BORDERX
        y_pc_topleft = y * SCALEFACTOR + BORDERY
        self.rect.x = x_pc_topleft 
        self.rect.y = y_pc_topleft 

    def update(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = 2
        self.game   = game
        self.speed  = speed
        self.createImage()
        self.setPosition()

    def setPosition(self):
        self.rect.x = (self.x - self.r) * SCALEFACTOR + BORDERX
        self.rect.y = (self.y - self.r) * SCALEFACTOR + BORDERY

    def movement(self, cx, cy, cr):
        if self.game.keyaction["quit"]:
            self.game.running = False
            return
        old = (self.x, self.y)
        # self.x and self.y may change by less than 1 per frame.
        # That's why you can't use "int()" on them, because it
        # could disable movement.
        if self.game.keyaction["left"]:
            self.x -= self.speed * self.game.clocktick
        if self.game.keyaction["right"]:
            self.x += self.speed * self.game.clocktick
        if self.game.keyaction["up"]:
            self.y -= self.speed * self.game.clocktick
        if self.game.keyaction["down"]:
            self.y += self.speed * self.game.clocktick
        # Check boundaries:
        if self.x < 1 or self.x > RESX - 1 or self.y < 1 or self.y > RESY - 1:
            self.x = old[0]
            self.y = old[1]
        # Check collision with circle:
        cp = math.sqrt((cx - self.x) ** 2 + (cy - self.y) ** 2)
        if cp < cr:
            self.x = old[0]
            self.y = old[1]
        self.setPosition()

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def createImage(self):
        self.image = pygame.Surface((self.r * 2 * SCALEFACTOR, self.r * 2 * SCALEFACTOR), pygame.SRCALPHA)
        r_pc = self.r * SCALEFACTOR
        pygame.draw.circle(self.image, COLORS[PLAYERINK], (r_pc, r_pc), r_pc)
        self.rect  = self.image.get_rect()

#######################################

# Groups:

class BorderGroup(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def setColor(self, colorname):
        for s in self.sprites():
            s.changeColor(colorname)

class AllSpritesGroup(pygame.sprite.Group):

    def __init__(self, *args):
        pygame.sprite.Group.__init__(self, *args)

    def update(self, screen):
        for s in self.sprites():
            s.update(screen)

#######################################

# InputHandler:

class InputHandler:

    # Ye olde, trustworthy InputHandler:

    def __init__(self, hasjoystick):
        self.hasjoystick = hasjoystick

        self.data = { pygame.K_LEFT  : "left", pygame.K_RIGHT   : "right",
                      pygame.K_UP    : "up",   pygame.K_DOWN    : "down",
                      pygame.K_LCTRL : "fire", pygame.K_RCTRL   : "fire",
                      pygame.K_q     : "quit", pygame.K_ESCAPE : "quit" }

        self.datakeys = self.data.keys()
        self.datavalues = self.data.values()

        self.joystick = {}
        if self.hasjoystick:
            self.initJoystick()
        self.initKeys()

    def initJoystick(self):
        if pygame.joystick.get_count() == 0:
            print("No joysticks found.")
            self.hasjoystick = False
            return
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
        for i in self.datavalues:
            if i == "quit":
                continue
            self.joystick[i] = False

    def initKeys(self):
        self.keypresses = {}
        for i in self.datakeys:
            self.keypresses[i] = False

    def getKeyboardAndJoystickAction(self):
        action = {"left" : False, "right" : False, "up" : False, "down" : False,
                  "fire" : False, "quit" : False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action["quit"] = True
                continue
            if event.type == pygame.KEYDOWN:
                for i in self.keypresses:
                    if event.key == i:
                        self.keypresses[i] = True
            if event.type == pygame.KEYUP:
                for i in self.keypresses:
                    if event.key == i:
                        self.keypresses[i] = False
            if self.hasjoystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.joystick["fire"] = True
                if event.type == pygame.JOYBUTTONUP:
                    self.joystick["fire"] = False
                if event.type == pygame.JOYAXISMOTION:
                    # Joystick pushed:
                    if event.axis == 0 and int(event.value) == -1:
                        self.joystick["left"] = True
                    if event.axis == 0 and int(event.value) == 1:
                        self.joystick["right"] = True
                    if event.axis == 1 and int(event.value) == -1:
                        self.joystick["up"] = True
                    if event.axis == 1 and int(event.value) == 1:
                        self.joystick["down"] = True
                    # Joystick released:
                    if event.axis == 0 and int(event.value) == 0:
                        self.joystick["left"] = False
                        self.joystick["right"] = False
                    if event.axis == 1 and int(event.value) == 0:
                        self.joystick["up"] = False
                        self.joystick["down"] = False

        # Same indentation level as "for event in pygame.event.get()":
        for i in self.datakeys:
            if self.keypresses[i]:
                action[self.data[i]] = True
        if self.hasjoystick:
            for i in self.datavalues:
                if i == "quit":
                    continue
                if self.joystick[i]:
                    action[i] = True
        return action

#######################################

Main()
