#!/usr/bin/python3
# coding: utf-8

import pygame
from math import cos, sin
import os
from inputhandler import InputHandler

"""
    Rotating Polygons 1.0 - Rotation of Polygons such as cubes and pyramids
                            as seen in classic vector graphics games.

    Based upon:

    https://github.com/yuta-51/3DProjection
    https://github.com/Magoninho/3D-projection-tutorial

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

WINDOW_SIZE  =  (800, 600)
ROTATE_SPEED = 0.02
SCALE        = 100

class Polygon:

    def __init__(self, angle_x, angle_y, angle_z):
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.projection_matrix = ((1,0,0),
                                  (0,1,0),
                                  (0,0,0))
        self.pointdata = ()
        self.connectdata = ()

    def multiply_m(self, a, b):
        a_rows = len(a)
        a_cols = len(a[0])
        b_rows = len(b)
        b_cols = len(b[0])
        # Dot product matrix dimensions = a_rows x b_cols
        product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
        if a_cols == b_rows:
            for i in range(a_rows):
                for j in range(b_cols):
                    for k in range(b_rows):
                        product[i][j] += a[i][k] * b[k][j]
        else:
            print("INCOMPATIBLE MATRIX SIZES")
        return product        

    def rotate(self, direction):
        if direction == "left":
            self.angle_y += ROTATE_SPEED
        if direction == "right":
            self.angle_y -= ROTATE_SPEED
        if direction == "up":
            self.angle_x += ROTATE_SPEED
        if direction == "down":
            self.angle_x -= ROTATE_SPEED

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
            x = int(point_2d[0][0] * SCALE + WINDOW_SIZE[0] / 2)
            y = int(point_2d[1][0] * SCALE + WINDOW_SIZE[1] / 2)
            points.append((x, y))
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)

        # Connect points:
        for i in self.connectdata:
            pygame.draw.line(screen, (255, 255, 255), (points[i[0]][0], points[i[0]][1]) , (points[i[1]][0], points[i[1]][1]))


class CoordinateSystem(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, 0, 0, 0)
        self.name = name
        l = 2
        self.pointdata = (((-l, ), (0, ), (0, )),
                          ((l, ),  (0, ), (0, )),
                          ((0, ), (-l, ), (0, )),
                          ((0, ),  (l, ), (0, )),
                          ((0, ), (0, ), (-l, )),
                          ((0, ),  (0, ), (l, )))
        self.connectdata = ((0, 1), (2, 3), (4, 5))

class Cube(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, 0, 0, 0)
        self.name = name
        l = 1
        self.pointdata = (((-1, ), (-1, ), (1, )),
                          ((1, ),(-1, ),(1, )),
                          ((1, ),(1, ),(1, )),
                          ((-1, ),(1, ),(1, )),
                          ((-1, ),(-1, ),(-1, )),
                          ((1, ),(-1, ),(-1, )),
                          ((1, ),(1, ),(-1, )),
                          ((-1, ),(1, ),(-1, )))

        self.connectdata = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 6), (2, 3), (3, 7), 
                            (4, 5), (4, 7), (6, 5), (6, 7)) 

class Pyramid(Polygon):

    def __init__(self, name):
        Polygon.__init__(self, 0, 0, 0)
        self.name = name
        l = 1
        self.pointdata = (((l, ),  (-l, ), (-l, )),
                          ((l, ),  (-l, ), (l, )),
                          ((-l, ),  (-l, ), (-l, )),
                          ((-l, ),  (-l, ), (l, )),
                          ((0, ),  (l, ), (0, )))

        self.connectdata =((0, 1), (2, 3), (0, 2), (1, 3),
                           (0, 4), (1, 4), (2, 4), (3, 4))

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
        self.pggroup.add(CoordinateSystem("coordinatesystem"))
        self.pggroup.add(Pyramid("pyramid"))
        self.pggroup.add(Cube("cube"))

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
