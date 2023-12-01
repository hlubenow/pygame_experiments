#!/usr/bin/python3
# coding: utf-8

import pygame
from inputhandler import *
from config import *

class MySprite(pygame.sprite.Sprite):

    def __init__(self, name, id, game, speed, groups):
        self.game           = game
        pygame.sprite.Sprite.__init__(self, groups)
        self.name           = name
        self.id             = id
        self.speed          = speed
        self.image          = None
        self.rect           = None

    def setPosition(self, spos_x, spos_y):
        self.rect.x = self.spos_x * SCALEFACTOR
        self.rect.y = self.spos_y * SCALEFACTOR

    def getPosition(self):
        return (self.spos_x, self.spos_y)


class Player(MySprite):

    def __init__(self, name, id, game, width, height, spos_x, spos_y, colorname, speed):
        self.groups = game.all_sprites, game.playergroup
        MySprite.__init__(self, name, id, game, speed, self.groups)
        self.spos_x = spos_x
        self.spos_y = spos_y
        self.ih = InputHandler(True)
        self.createImage(width, height, colorname)
        self.setPosition(self.spos_x, self.spos_y)

    def update(self):
        self.movement()
        self.setPosition(self.spos_x, self.spos_y)

    def movement(self):
        action = self.ih.getKeyboardAndJoystickAction()
        if action["quit"]:
            self.game.running = False
            return
        if action["left"]:
            self.spos_x -= self.speed * self.game.clocktick
            if self.spos_x < 0:
                self.setPosition(SSIZE_SCREEN_X, self.spos_y)
        if action["right"]:
            self.spos_x += self.speed * self.game.clocktick
            if self.spos_x > SSIZE_SCREEN_X:
                self.setPosition(0, self.spos_y)
        if action["up"]:
            self.spos_y -= self.speed * self.game.clocktick
            if self.spos_y < 0:
                self.setPosition(self.spos_x, SSIZE_SCREEN_Y)
        if action["down"]:
            self.spos_y += self.speed * self.game.clocktick
            if self.spos_y > SSIZE_SCREEN_Y:
                self.setPosition(self.spos_x, 0 )

    def createImage(self, ssize_x, ssize_y, colorname):
        self.image = pygame.Surface((ssize_x * SCALEFACTOR, ssize_y * SCALEFACTOR))
        self.image = self.image.convert()
        self.rect  = self.image.get_rect()
        self.image.fill(COLORS["black"])
        pygame.draw.circle(self.image, COLORS[colorname], (self.rect.width // 2, self.rect.height // 2), self.rect.height // 2)
        self.image.set_colorkey(COLORS["black"])
