#!/usr/bin/python
# coding: utf-8

import pygame
from pygame.locals import *

import os, sys

"""
    rainbow_colors.py 1.0 - A Graphics Demo

    Copyright (C) 2023 hlubenow

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

SCALEFACTOR = 3
FPS         = 50

class ATEnvironment:

    def __init__(self, at_data):
        self.at_data = at_data
        self.at_paperwidth  = 320
        self.at_paperheight = 192
        self.pc_paperwidth  = self.at_paperwidth  * SCALEFACTOR
        self.pc_paperheight = self.at_paperheight * SCALEFACTOR
        self.at_borderwidth = 24
        self.at_borderheight = 12
        self.pc_borderwidth = self.at_borderwidth * SCALEFACTOR
        self.pc_borderheight = self.at_borderheight * SCALEFACTOR
        self.screenwidth  = self.pc_paperwidth + 2 * self.pc_borderwidth
        self.screenheight = self.pc_paperheight + 2 * self.pc_borderheight

    def initPaper(self):
        self.paper = pygame.Surface((self.pc_paperwidth, self.pc_paperheight))
        self.paperpos = (self.pc_borderwidth, self.pc_borderheight)
        self.paper.fill((0, 0, 0))

    def setPaperColor(self, colorname):
        self.paper.fill(self.at_data.getColorTuple(colorname))


class ATColorField:

    def __init__(self, at_env, at_data, nroflines, linewidth, lineheight, at_position):
        self.at_env      = at_env
        self.at_data     = at_data
        self.linerects = []
        # We assume, that the ColorField is blitted to self.at_env.paper:
        for i in range(nroflines):
            left   = at_position[0] * SCALEFACTOR
            top    = (at_position[1] + lineheight * i) * SCALEFACTOR
            width  = linewidth * SCALEFACTOR
            height = lineheight * SCALEFACTOR
            self.linerects.append(pygame.Rect(left, top, width, height))

        self.coloroffset = 0
        self.direction = "up"
        self.running = 0

    def drawField(self, paper):
        for i in range(len(self.linerects)):
            colortuple = self.at_data.colorcodes[self.coloroffset + i]
            pygame.draw.rect(paper, colortuple, self.linerects[i])

    def cycleColors(self):

        if self.running < 100:
            return

        if self.direction == "up":
            self.coloroffset += 1

        if self.direction == "down":
            self.coloroffset -= 1

        if self.coloroffset + len(self.linerects) > 255:
            self.direction = "down"
            self.coloroffset = 255 - len(self.linerects)
            self.running = 0

        if self.coloroffset < 0:
            self.direction = "up"
            self.coloroffset = 0
            self.running = 0

    def checkRunning(self):
        self.running += 1
   
    def draw(self, screen):
        for i in self.lines:
            screen.draw(i)


class ATData:

    def __init__(self):

        self.colornames = {"black"       : 0,
                           "dark_grey"   : 2,
                           "grey"        : 4,
                           "light_grey"  : 8,
                           "dark_blue"   : 112,
                           "blue"        : 114,
                           "dark_brown"  : 242,
                           "brown"       : 244,
                           "light_brown" : 248,
                           "ocher"       : 234,
                           "dark_red"    : 48,
                           "red"         : 52,
                           "light_red"   : 54, 
                           "orange"      : 38,
                           "magenta"     : 70,
                           "pink"        : 74,
                           "dark_green"  : 210,
                           "green"       : 184,
                           "light_green" : 188,
                           "cyan"        : 152,
                           "yellow"      : 28,
                           "white"       : 15,
                           "blue_default"  : 300,
                           "white_default" : 301}

        self.colorcodes = {0 : (0, 0, 0),
                           1 : (37, 37, 37),
                           2 : (52, 52, 52),
                           3 : (78, 78, 78),
                           4 : (104, 104, 104),
                           5 : (117, 117, 117),
                           6 : (142, 142, 142),
                           7 : (164, 164, 164),
                           8 : (184, 184, 184),
                           9 : (197, 197, 197),
                           10 : (208, 208, 208),
                           11 : (215, 215, 215),
                           12 : (225, 225, 225),
                           13 : (234, 234, 234),
                           14 : (244, 244, 244),
                           15 : (255, 255, 255),
                           16 : (65, 32, 0),
                           17 : (84, 40, 0),
                           18 : (118, 55, 0),
                           19 : (154, 80, 0),
                           20 : (195, 104, 6),
                           21 : (228, 123, 7),
                           22 : (255, 145, 26),
                           23 : (255, 171, 29),
                           24 : (255, 197, 31),
                           25 : (255, 208, 59),
                           26 : (255, 216, 76),
                           27 : (255, 230, 81),
                           28 : (255, 244, 86),
                           29 : (255, 249, 112),
                           30 : (255, 255, 144),
                           31 : (255, 255, 170),
                           32 : (69, 25, 4),
                           33 : (114, 30, 17),
                           34 : (159, 36, 30),
                           35 : (179, 58, 32),
                           36 : (200, 81, 32),
                           37 : (227, 105, 32),
                           38 : (252, 129, 32),
                           39 : (253, 140, 37),
                           40 : (254, 152, 44),
                           41 : (255, 174, 56),
                           42 : (255, 185, 70),
                           43 : (255, 191, 81),
                           44 : (255, 198, 109),
                           45 : (255, 213, 135),
                           46 : (255, 228, 152),
                           47 : (255, 230, 171),
                           48 : (93, 31, 12),
                           49 : (122, 36, 13),
                           50 : (152, 44, 14),
                           51 : (176, 47, 15),
                           52 : (191, 54, 36),
                           53 : (211, 78, 42),
                           54 : (231, 98, 62),
                           55 : (243, 110, 74),
                           56 : (253, 120, 84),
                           57 : (255, 138, 106),
                           58 : (255, 152, 124),
                           59 : (255, 164, 139),
                           60 : (255, 179, 158),
                           61 : (255, 194, 178),
                           62 : (255, 208, 195),
                           63 : (255, 218, 208),
                           64 : (74, 23, 0),
                           65 : (114, 31, 0),
                           66 : (168, 19, 0),
                           67 : (200, 33, 10),
                           68 : (223, 37, 18),
                           69 : (236, 59, 36),
                           70 : (250, 82, 54),
                           71 : (252, 97, 72),
                           72 : (255, 112, 95),
                           73 : (255, 126, 126),
                           74 : (255, 143, 143),
                           75 : (255, 157, 158),
                           76 : (255, 171, 173),
                           77 : (255, 185, 189),
                           78 : (255, 199, 206),
                           79 : (255, 202, 222),
                           80 : (73, 0, 54),
                           81 : (102, 0, 75),
                           82 : (128, 3, 95),
                           83 : (149, 15, 116),
                           84 : (170, 34, 136),
                           85 : (186, 61, 153),
                           86 : (202, 77, 169),
                           87 : (215, 90, 182),
                           88 : (228, 103, 195),
                           89 : (239, 114, 206),
                           90 : (251, 126, 218),
                           91 : (255, 141, 225),
                           92 : (255, 157, 229),
                           93 : (255, 165, 231),
                           94 : (255, 175, 234),
                           95 : (255, 184, 236),
                           96 : (72, 3, 108),
                           97 : (92, 4, 136),
                           98 : (101, 13, 144),
                           99 : (123, 35, 167),
                           100 : (147, 59, 191),
                           101 : (157, 69, 201),
                           102 : (167, 79, 211),
                           103 : (178, 90, 222),
                           104 : (189, 101, 233),
                           105 : (197, 109, 241),
                           106 : (206, 118, 250),
                           107 : (213, 131, 255),
                           108 : (218, 144, 255),
                           109 : (222, 156, 255),
                           110 : (226, 169, 255),
                           111 : (230, 182, 255),
                           112 : (5, 30, 129),
                           113 : (6, 38, 165),
                           114 : (8, 47, 202),
                           115 : (38, 61, 212),
                           116 : (68, 76, 222),
                           117 : (79, 90, 236),
                           118 : (90, 104, 255),
                           119 : (101, 117, 255),
                           120 : (113, 131, 255),
                           121 : (128, 145, 255),
                           122 : (144, 160, 255),
                           123 : (151, 169, 255),
                           124 : (159, 178, 255),
                           125 : (175, 190, 255),
                           126 : (192, 203, 255),
                           127 : (205, 211, 255),
                           128 : (11, 7, 121),
                           129 : (32, 28, 142),
                           130 : (53, 49, 163),
                           131 : (70, 66, 180),
                           132 : (87, 83, 197),
                           133 : (97, 93, 207),
                           134 : (109, 105, 219),
                           135 : (123, 119, 233),
                           136 : (137, 133, 247),
                           137 : (145, 141, 255),
                           138 : (156, 152, 255),
                           139 : (167, 164, 255),
                           140 : (178, 175, 255),
                           141 : (187, 184, 255),
                           142 : (195, 193, 255),
                           143 : (211, 209, 255),
                           144 : (29, 41, 90),
                           145 : (29, 56, 118),
                           146 : (29, 72, 146),
                           147 : (29, 92, 172),
                           148 : (29, 113, 198),
                           149 : (50, 134, 207),
                           150 : (72, 155, 217),
                           151 : (78, 168, 236),
                           152 : (85, 182, 255),
                           153 : (105, 202, 255),
                           154 : (116, 203, 255),
                           155 : (130, 211, 255),
                           156 : (141, 218, 255),
                           157 : (159, 212, 255),
                           158 : (180, 226, 255),
                           159 : (192, 235, 255),
                           160 : (0, 75, 89),
                           161 : (0, 93, 110),
                           162 : (0, 111, 132),
                           163 : (0, 132, 156),
                           164 : (0, 153, 191),
                           165 : (0, 171, 202),
                           166 : (0, 188, 222),
                           167 : (0, 208, 245),
                           168 : (16, 220, 255),
                           169 : (62, 225, 255),
                           170 : (100, 231, 255),
                           171 : (118, 234, 255),
                           172 : (139, 237, 255),
                           173 : (154, 239, 255),
                           174 : (177, 243, 255),
                           175 : (199, 246, 255),
                           176 : (0, 72, 0),
                           177 : (0, 84, 0),
                           178 : (3, 107, 3),
                           179 : (14, 118, 14),
                           180 : (24, 128, 24),
                           181 : (39, 146, 39),
                           182 : (54, 164, 54),
                           183 : (78, 185, 78),
                           184 : (81, 205, 81),
                           185 : (114, 218, 114),
                           186 : (124, 228, 124),
                           187 : (133, 237, 133),
                           188 : (153, 242, 153),
                           189 : (179, 247, 179),
                           190 : (195, 249, 195),
                           191 : (205, 252, 205),
                           192 : (22, 64, 0),
                           193 : (28, 83, 0),
                           194 : (35, 102, 0),
                           195 : (40, 120, 0),
                           196 : (46, 140, 0),
                           197 : (58, 152, 12),
                           198 : (71, 165, 25),
                           199 : (81, 175, 35),
                           200 : (92, 186, 46),
                           201 : (113, 207, 67),
                           202 : (133, 227, 87),
                           203 : (141, 235, 95),
                           204 : (151, 245, 105),
                           205 : (160, 254, 114),
                           206 : (177, 255, 138),
                           207 : (188, 255, 154),
                           208 : (44, 53, 0),
                           209 : (56, 68, 0),
                           210 : (68, 82, 0),
                           211 : (73, 86, 0),
                           212 : (96, 113, 0),
                           213 : (108, 127, 0),
                           214 : (121, 141, 10),
                           215 : (139, 159, 28),
                           216 : (158, 178, 47),
                           217 : (171, 191, 60),
                           218 : (184, 204, 73),
                           219 : (194, 214, 83),
                           220 : (205, 225, 83),
                           221 : (219, 239, 108),
                           222 : (232, 252, 121),
                           223 : (242, 255, 171),
                           224 : (70, 58, 9),
                           225 : (77, 63, 9),
                           226 : (84, 69, 9),
                           227 : (108, 88, 9),
                           228 : (144, 118, 9),
                           229 : (171, 139, 10),
                           230 : (193, 161, 32),
                           231 : (208, 176, 47),
                           232 : (222, 190, 61),
                           233 : (230, 198, 69),
                           234 : (237, 205, 76),
                           235 : (245, 216, 98),
                           236 : (251, 226, 118),
                           237 : (252, 238, 152),
                           238 : (253, 243, 169),
                           239 : (253, 243, 190),
                           240 : (64, 26, 2),
                           241 : (88, 31, 5),
                           242 : (112, 36, 8),
                           243 : (141, 58, 19),
                           244 : (171, 81, 31),
                           245 : (181, 100, 39),
                           246 : (191, 119, 48),
                           247 : (208, 133, 58),
                           248 : (225, 147, 68),
                           249 : (237, 160, 78),
                           250 : (249, 173, 88),
                           251 : (252, 183, 92),
                           252 : (255, 193, 96),
                           253 : (255, 202, 105),
                           254 : (255, 207, 126),
                           255 : (255, 218, 150),
                           300 : (28, 112, 198),
                           301 : (112, 197, 255)}

    def getColorTuple(self, colorname):
        return self.colorcodes[self.colornames[colorname]]


class Main:

    def __init__(self):
        self.at_data = ATData()
        self.at_env  = ATEnvironment(self.at_data)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "78, 2"
        pygame.init()
        self.screen = pygame.display.set_mode((self.at_env.screenwidth, self.at_env.screenheight))
        pygame.display.set_caption("Rainbow Colors")
        self.at_env.initPaper()
        self.at_env.setPaperColor("blue_default")
        self.clock = pygame.time.Clock()
        self.colorfield = ATColorField(at_env      = self.at_env,
                                       at_data     = self.at_data,
                                       nroflines   = 100,
                                       linewidth   = 200,
                                       lineheight  = 1,
                                       at_position = (60, 50))
        self.running = True

        while self.running:
            self.clock.tick(FPS)
            if self.processEvents() == "quit":
                self.running = False
            self.screen.fill((0, 0, 0))
            self.colorfield.checkRunning()
            self.colorfield.cycleColors()
            self.colorfield.drawField(self.at_env.paper)
            self.screen.blit(self.at_env.paper, self.at_env.paperpos)
            pygame.display.flip()

        pygame.quit()

    def processEvents(self):
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[K_q] or pressed[K_ESCAPE]:
            return "quit"
        return 0

if __name__ == "__main__":
    Main()
