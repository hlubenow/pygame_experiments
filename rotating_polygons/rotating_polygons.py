#!/usr/bin/python3
# coding: utf-8

import pygame
from math import cos, sin
import os, sys
from inputhandler import InputHandler

"""
    Rotating Polygons 1.1 - Rotation of Polygons such as cubes and pyramids
                            as seen in classic vector graphics games.

    Based upon:

    https://github.com/yuta-51/3DProjection
    https://github.com/Magoninho/3D-projection-tutorial
    https://github.com/Wireframe-Magazine/Wireframe-67/tree/main/source-code-elite

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

WINDOW_SIZE = (800, 600)

SHOW = ("cube", "pyramid", "coordinatesystem")

if len(sys.argv) > 1 and "ship" in sys.argv[1]:
    SHOW = ("ship",)

class Polygon:

    def __init__(self, angle_x, angle_y, angle_z):
        self.scale   = 100
        self.rotate_speed = 0.03
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.projection_matrix = ((1, 0, 0),
                                  (0, 1, 0),
                                  (0, 0, 0))
        self.pointdata = ()
        self.connectdata = ()

    def printAngles(self):
        print ("angle_x:    " + str(self.angle_x))
        print ("angle_y:    " + str(self.angle_y))
        print ("angle_z:    " + str(self.angle_z))
        print ()

    def reformatPointData(self, a):
        """ What we need is a matrix, with three rows and one column (= column-vector).
            As tuples, it looks like this: "((2,), (5,), (3,))". """
        b = []
        for i in a:
            c = []
            for u in i:
                d = [u]
                c.append(d)
            b.append(c)
        return b

    def multiply_m(self, a, b):
        """ Input are two matrices. If a matrix is a vector (in this script typically b), it has
            to be a column-vector, that is, it has to have several lines, but just one column.
            Not a row-vector. """
        a_rows = len(a)
        a_cols = len(a[0])
        b_rows = len(b)
        b_cols = len(b[0])
        if a_cols != b_rows:
            print("INCOMPATIBLE MATRIX SIZES")
            return
        # Dot product matrix dimensions = a_rows x b_cols
        product = []
        for i in range(a_rows):
            line = []
            for u in range(b_cols):
                n = 0
                for u2 in range(b_rows):
                    n += a[i][u2] * b[u2][u]
                line.append(n)
            product.append(line)
        return product 

    def rotate(self, direction):
        if direction == "left":
            self.angle_y += self.rotate_speed
        if direction == "right":
            self.angle_y -= self.rotate_speed
        if direction == "up":
            self.angle_x += self.rotate_speed
        if direction == "down":
            self.angle_x -= self.rotate_speed

    def draw(self, screen):

        rotation_x = ((1, 0, 0),
                      (0, cos(self.angle_x), -sin(self.angle_x)),
                      (0, sin(self.angle_x), cos(self.angle_x)))
        rotation_y = ((cos(self.angle_y), 0, sin(self.angle_y)),
                      (0, 1, 0),
                      (-sin(self.angle_y), 0, cos(self.angle_y)))
        rotation_z = ((cos(self.angle_z), -sin(self.angle_z), 0),
                      (sin(self.angle_z), cos(self.angle_z), 0),
                      (0, 0, 1))

        points = []
        for point in self.pointdata:
            rotate_x = self.multiply_m(rotation_x, point)
            rotate_y = self.multiply_m(rotation_y, rotate_x)
            rotate_z = self.multiply_m(rotation_z, rotate_y)
            point_2d = self.multiply_m(self.projection_matrix, rotate_z)
            x = int(point_2d[0][0] * self.scale + WINDOW_SIZE[0] / 2)
            y = int(point_2d[1][0] * self.scale + WINDOW_SIZE[1] / 2)
            points.append((x, y))
            if self.name != "ship":
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)

        # Connect points:
        for i in self.connectdata:
            pygame.draw.line(screen, (255, 255, 255), (points[i[0]][0], points[i[0]][1]) , (points[i[1]][0], points[i[1]][1]), 2)

        # self.printAngles()


class CoordinateSystem(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, -2.92, 3.46, 0)
        self.name = name
        l = 2
        self.pointdata = ((-l, 0, 0),
                          (l,  0, 0),
                          (0, -l, 0),
                          (0,  l, 0),
                          (0, 0, -l),
                          (0,  0, l))
        self.pointdata = self.reformatPointData(self.pointdata)

        self.connectdata = ((0, 1), (2, 3), (4, 5))


class Cube(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, -2.92, 3.46, 0)
        self.name = name
        l = 1
        self.pointdata = ((-1, -1, 1),
                          (1, -1, 1),
                          (1, 1, 1),
                          (-1, 1, 1),
                          (-1, -1, -1),
                          (1, -1, -1),
                          (1, 1, -1),
                          (-1, 1, -1))
        self.pointdata = self.reformatPointData(self.pointdata)

        self.connectdata = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 6), (2, 3), (3, 7), 
                            (4, 5), (4, 7), (6, 5), (6, 7)) 

class Pyramid(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, -2.92, 3.46, 0)
        self.name = name
        l = 1
        self.pointdata = ((l,  -l, -l),
                          (l,  -l, l),
                          (-l,  -l, -l),
                          (-l,  -l, l),
                          (0,  l, 0))
        self.pointdata = self.reformatPointData(self.pointdata)

        self.connectdata =((0, 1), (2, 3), (0, 2), (1, 3),
                           (0, 4), (1, 4), (2, 4), (3, 4))

class Ship(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, -3.6, -0.48, 0)
        self.name = name
        self.scale = 1.7
        self.rotate_speed = 0.04
        l = 1
        self.pointdata = ((32, 0, 76), (-32, 0, 76), (0, 26, 24), (-120, -3, -8),
                          (120, -3, -8), (-88, 16, -40), (88, 16, -40), (128, -8, -40),
                          (-128, -8, -40), (0, 26, -40), (-32, -24, -40), (32, -24, -40),
                          (-36, 8, -40), (-8, 12, -40), (8, 12, -40), (36, 8, -40),
                          (36, -12, -40), (8, -16, -40), (-8, -16, -40), (-36, -12, -40),
                          (0, 0, 76), (0, 0, 90), (-80, -6, -40), (-80, 6, -40),
                          (-88, 0, -40), (80, 6, -40), (88, 0, -40), (80, -6, -40))
        self.pointdata = self.reformatPointData(self.pointdata)

        self.connectdata =((1, 2), (2, 0), (0, 20), (20, 1),
                           (1, 5), (5, 2), (6, 0), (2, 6),
                           (1, 3), (3, 5), (4, 0), (6, 4),
                           (5, 9), (9, 2), (9, 6), (3, 8),
                           (8, 5), (7, 4), (6, 7), (8, 10),
                           (10, 11), (11, 8), (1, 10), (0, 11),
                           (7, 11), (18, 13), (13, 12), (12, 19),
                           (19, 18), (17, 16), (16, 15), (15, 14),
                           (14, 17), (22, 23), (23, 24), (24, 22),
                           (27, 26), (26, 25), (25, 27), (20, 21))


class PolygonGroup:

    def __init__(self):
        self.group = []

    def add(self, a):
        self.group.append(a)

    def remove(self, a):
        self.group.remove(a)

    def rotate(self, direction):
        for i in self.group:
            i.rotate(direction)

    def draw(self, screen):
        for i in self.group:
            i.draw(screen)


class Main:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "185, 30"
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Rotating Polygons")
        self.ih = InputHandler(True)
        self.initPolygons()
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.clock.tick(50)
            self.screen.fill((0, 0, 0))

            self.pggroup.draw(self.screen)

            if self.checkInput() == "quit":
                print("Bye.")
                self.running = False
                continue
            pygame.display.flip()
        pygame.quit()

    def initPolygons(self):
        self.pggroup = PolygonGroup()
        if "coordinatesystem" in SHOW:
           self.pggroup.add(CoordinateSystem("coordinatesystem"))
        if "pyramid" in SHOW:
            self.pggroup.add(Pyramid("pyramid"))
        if "cube" in SHOW:
            self.pggroup.add(Cube("cube"))
        if "ship" in SHOW:
            self.pggroup.add(Ship("ship"))

    def checkInput(self):
        # "action" is a dictionary with the keys "left right up down fire quit":
        action = self.ih.getKeyboardAndJoystickAction()
        for i in action.keys():
            if i == "quit" and action[i]:
                pygame.quit()
                return "quit"
            if action[i]:
                self.pggroup.rotate(i)
        return 0

Main()
