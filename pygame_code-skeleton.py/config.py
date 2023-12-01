#!/usr/bin/python3
# coding: utf-8

SSIZE_SCREEN_X = 256
SSIZE_SCREEN_Y = 192
SCALEFACTOR    = 3

WINDOWPOSITION_X = 185
WINDOWPOSITION_Y = 30

FPS            = 60

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
