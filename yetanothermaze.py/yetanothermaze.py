#!/usr/bin/python3
# coding: utf-8

MAZE_SIZE       = (20, 20)

WALLCOLOR       = "blue_grey"
# Filled walls:
LINESIZE        = 0

SCALEFACTOR     = 3
FPS             = 50

CHARSETFILENAME = "ZX_Spectrum_character_set.png"

"""
yetanothermaze.py 1.1 - Pygame script, that lets you walk through a 3D maze

Copyright (C) 2021, hlubenow. License: GNU GPL (version 3 or above):

----------------------
Inspired by this approach in C (by Stefan Haubenthal):
https://atariwiki.org/wiki/Wiki.jsp?page=3dMaze
----------------------

License: GNU GPL (version 3 or above):

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame

import os
import random

COLORS = { "black"     : (0, 0, 0),
           "blue_grey" : (0, 85, 102),
           "magenta"   : (255, 0, 255),
           "white"     : (255, 255, 255) }

class StringSurface:

    def __init__(self):
        self.surface = pygame.Surface((120, 24))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(COLORS["black"])
        self.rect = self.surface.get_rect()
        self.rect.topleft = ((24 + 140) * SCALEFACTOR, 170 * SCALEFACTOR)
        self.visible = 0
        self.csb = CharacterSetBuilder((255, 0, 255))
        self.chars = self.csb.surfaces
        self.createSurface()

    def createSurface(self):
        string_ = "Ouch!"
        x = 0
        for i in string_:
            self.chars[i].setPosition(x, 0)
            self.surface.blit(self.chars[i].surface, self.chars[i].rect)
            x += 24

    def show(self):
        self.visible = 1

    def draw(self, screen):
        if self.visible:
            screen.blit(self.surface, self.rect)
            self.visible += 1
            if self.visible >= 35:
                self.visible = 0


class CharacterSurface:

    def __init__(self, characterbytes, colortuple):
        self.characterbytes = characterbytes
        self.surface     = pygame.Surface((8 * SCALEFACTOR, 8 * SCALEFACTOR))
        self.surface     = self.surface.convert()
        self.surface.set_colorkey(COLORS["black"])
        self.rect        = self.surface.get_rect()
        self.colortuple  = colortuple
        self.background  = COLORS["black"]
        self.createSurface()

    def setPosition(self, pc_x, pc_y):
        self.rect.topleft = (pc_x, pc_y)

    def createSurface(self):
        t_x = 0
        t_y = 0
        rect = pygame.Rect(0, 0, SCALEFACTOR, SCALEFACTOR)
        for byte in self.characterbytes:
            for bit in byte:
                if bit == "1":
                    c = self.colortuple
                else:
                    c = self.background
                rect.topleft = (t_x * SCALEFACTOR, t_y * SCALEFACTOR)
                self.surface.fill(c, rect)
                t_x += 1
            t_y += 1
            t_x -= 8


class CharacterSetBuilder:

    def __init__(self, colortuple):
        self.colortuple         = colortuple
        self.spritesheetsurface = pygame.image.load(CHARSETFILENAME)
        self.spritesheetsurface = self.spritesheetsurface.convert()
        self.rect               = pygame.Rect((0, 0), (8, 8))
        self.surfaces           = {}
        self.buildSurfaces()

    def getSurfaces(self):
        return self.surfaces

    def buildSurfaces(self):
        data = {"O" : (15, 2), "u" : (5, 5), "c" : (3, 4),
                "h" : (8, 4), "!" : (1, 0)}
        for i in data.keys():
            self.surfaces[i] = CharacterSurface(self.getCharCellValues(data[i][0], data[i][1]), self.colortuple)

    def getCharCellValues(self, char_x, char_y):
        # n1 and n2, because the image is scaled by 2:
        a = []
        n1 = 0
        for ty in range(16):
            if n1 == 1:
                n1 = 0
                continue
            b = ""
            n2 = 0
            for tx in range(16):
                if n2 == 1:
                    n2 = 0
                    continue
                c = self.spritesheetsurface.get_at((char_x * 16 + tx, char_y * 16 + ty))
                if c[0] == 0 and c[1] == 0 and c[2] == 0:
                    b += "1"
                else:
                    b += "0"
                n2 = 1
            a.append(b)
            n1 = 1
        return a


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


class Player:

    def __init__(self, maze, x):
        self.maze = maze
        self.x = x
        self.y = 0
        self.entry = (self.x, self.y)
        self.cell = self.maze.maze_map[self.y][self.x]
        self.direction = "E"
        self.status = "init"

    def getCellAhead(self, cell, direction):

        """ If possible, this function returns the cell next to 'cell' in
            direction of 'direction'. Otherwise returns 'None'.

            Also the cells in front of the player's cell have to be displayed, if
            they are visible. Think of "Greater Revelation" (GRRE) in "Bard's Tale".
            So we need to be able to pass different cells to this function.

            Ordinary movement in a forward direction uses this function too.

            Note about "self.maze.maze_map[cell.y][cell.x]":
            The x and y coordinates still are the mathematical x and y coordinates
            of the maze. However, if you store several rows in an array, the value
            in the first square brackets is the y value. """

        if cell.has_wall(direction):
            return None
        if direction == "N":
            if cell.y == 0:
                return None
            else:
                return self.maze.maze_map[cell.y - 1][cell.x]
        if direction == "E":
            if cell.x == self.maze.width - 1:
                return None
            else:
                return self.maze.maze_map[cell.y][cell.x + 1]
        if direction == "W":
            if cell.x == 0:
                return None
            else:
                return self.maze.maze_map[cell.y][cell.x - 1]
        if direction == "S":
            if cell.y == self.maze.height - 1:
                return None
            else:
                return self.maze.maze_map[cell.y + 1][cell.x]

    def checkOtherCellForWallInDirection(self, cell, left_or_right):

        """ If there isn't a wall to the neighbour cell, we take a look into
            it, to find out if it has a wall in direction of 'self.direction'. """

        otherdirection = cell.getRotate(self.direction, left_or_right)
        othercell      = self.getCellAhead(cell, otherdirection)
        if othercell and othercell.has_wall(self.direction):
            cell.shapes[left_or_right + "_edge"] = True

    def rotateLeft(self):
        self.direction = self.cell.getRotate(self.direction, "left")
        self.status = "rotated"
        print(self.direction)
        print()

    def rotateRight(self):
        self.direction = self.cell.getRotate(self.direction, "right")
        self.status = "rotated"
        print(self.direction)
        print()

    def turnBackwards(self):
        self.direction = self.cell.wall_pairs[self.direction]
        self.status = "rotated"
        print(self.direction)
        print()

    def moveForward(self):
        self.status = None
        cell = self.getCellAhead(self.cell, self.direction)
        if cell:
            self.cell = cell
            self.x    = cell.x
            self.y    = cell.y
            print(self.direction)
            print(self.x, self.y)
            print()
            self.status = "moved"
            if self.cell.isExit:
                print("Exit found!")
                print()
        else:
            self.status = "blocked"


class Ladder:

    # This ladder almost drove me crazy. But I hope, it's worth it.

    def __init__(self):
        self.height = 200
        self.steps = (15, 45, 75, 105, 135, 165)
        self.stepwidth = 50
        self.ladderwidths = (3, 2, 1, 1, 1)
        self.drawingsizes = (80, 40, 20, 10, 5)
        self.stepcorrections = (5, 2, 1, 2, 0)
        self.corrections_x = (1, 0, 0, -1, -1)

    def buildSurfaces(self):
        self.surfaces = []
        self.rects = []
        nr = 0
        for drawingsize in self.drawingsizes:
            factor = 2. * drawingsize / self.height
            drawwidth  = factor * self.stepwidth
            drawheight = 2. * drawingsize
            surface = pygame.Surface(((drawwidth + 2 * self.ladderwidths[nr]) * SCALEFACTOR, drawheight * SCALEFACTOR))
            surface = surface.convert()
            surface.set_colorkey(COLORS["black"])
            rect    = surface.get_rect()
            self.drawLine(surface,
                          self.ladderwidths[nr], self.ladderwidths[nr],
                          self.ladderwidths[nr], drawheight,
                          self.ladderwidths[nr]) 
            self.drawLine(surface,
                          drawwidth, self.ladderwidths[nr],
                          drawwidth, drawheight,
                          self.ladderwidths[nr]) 
            for i in self.steps:
                self.drawLine(surface,
                              self.ladderwidths[nr], factor * i + self.stepcorrections[nr],
                              drawwidth, factor * i + self.stepcorrections[nr],
                              self.ladderwidths[nr]) 
            nr += 1
            self.surfaces.append(surface)
            self.rects.append(rect)

    def drawLine(self, surface, from_x, from_y, to_x, to_y, linewidth):

        from_x = int(from_x) * SCALEFACTOR
        from_y = int(from_y) * SCALEFACTOR
        to_x   = int(to_x)   * SCALEFACTOR
        to_y   = int(to_y)   * SCALEFACTOR

        pygame.draw.line(surface, COLORS["white"], (from_x, from_y), (to_x, to_y),
                         linewidth * SCALEFACTOR)

    def draw(self, screen, drawingsize, pc_x, pc_y):
        for i in range(len(self.drawingsizes)):
            if drawingsize == self.drawingsizes[i]:
                pc_x += self.corrections_x[i] * SCALEFACTOR
                self.rects[i].topleft = (pc_x, pc_y)
                screen.blit(self.surfaces[i], self.rects[i])


class DrawScreen:

    def __init__(self, env_, maze, player):
        self.env_ = env_
        self.maze = maze
        self.player = player
        self.linesize = SCALEFACTOR
        self.ladder = Ladder()
        self.ladder.buildSurfaces()
        self.drawladder = False
        self.surface = pygame.Surface((self.env_.pc_paperwidth, self.env_.pc_paperheight))
        self.surface = self.surface.convert()
        self.rect    = self.surface.get_rect()
        self.rect.topleft = (self.env_.pc_borderwidth, self.env_.pc_borderheight)
        self.centerx = self.env_.paperwidth / 2
        self.centery = self.env_.paperheight / 2
        self.drawingsize = self.centerx / 2
        self.drawverticals = {"left" : True, "right": True}

    def clear(self):
        self.surface.fill(COLORS["black"])

    def drawCells(self):
        drawingsize = self.drawingsize
        cells = []
        cells.append(self.player.cell)

        nextcell = self.player.getCellAhead(self.player.cell, self.player.direction)
        while nextcell != None:
            cells.append(nextcell)
            nextcell = self.player.getCellAhead(nextcell, self.player.direction)

        for cell in cells:
            cell.calculateShapes(self.player.direction)
            self.player.checkOtherCellForWallInDirection(cell, "left")
            self.player.checkOtherCellForWallInDirection(cell, "right")

            for i in cell.shapes.keys():
                if cell.isExit and self.player.direction == "S":
                    self.drawLadder(drawingsize)
                self.drawShape(i, drawingsize)
            drawingsize /= 2

    def drawLadder(self, drawingsize):
        pc_x  = self.centerx - int(drawingsize / 3.4)
        pc_y  = self.centery - int(drawingsize * 1.3)
        pc_x *= SCALEFACTOR
        pc_y *= SCALEFACTOR
        self.ladder.draw(self.surface, drawingsize, pc_x, pc_y)

    def drawShape(self, shape, drawingsize):

        if shape == "center_wall":
            self.drawCenterWall(drawingsize)
            return

        if shape == "left_wall":
            self.drawLeftWall(drawingsize)
            return

        if shape == "right_wall":
            self.drawRightWall(drawingsize)
            return

        if shape == "left_edge":
            self.drawLeftEdge(drawingsize)
            return

        if shape == "right_edge":
            self.drawRightEdge(drawingsize)
            return

    def drawCenterWall(self, drawingsize):

        points = (((self.centerx - drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx - drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR))

        rect = pygame.Rect(points[0],
                           (2 * drawingsize * SCALEFACTOR,
                           2 * drawingsize * SCALEFACTOR))

        pygame.draw.rect(self.surface, COLORS[WALLCOLOR], rect, LINESIZE)

        if LINESIZE == 0:
            pygame.draw.line(self.surface, COLORS["white"],
                             points[0], points[2],
                             self.linesize)

            pygame.draw.line(self.surface, COLORS["white"],
                             points[1], points[3],
                             self.linesize)

    def drawLeftWall(self, drawingsize):

        oldsize = drawingsize * 2

        points = (((self.centerx - oldsize) * SCALEFACTOR, (self.centery - oldsize) * SCALEFACTOR),
                  ((self.centerx - drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx - drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR),
                  ((self.centerx - oldsize) * SCALEFACTOR, (self.centery + oldsize) * SCALEFACTOR))

        pygame.draw.polygon(self.surface, COLORS[WALLCOLOR], points, LINESIZE)

        if LINESIZE == 0:
            pygame.draw.line(self.surface, COLORS["white"],
                             points[0], points[3],
                             self.linesize)

            pygame.draw.line(self.surface, COLORS["white"],
                             points[1], points[2],
                             self.linesize)

    def drawRightWall(self, drawingsize):

        oldsize = drawingsize * 2

        points = (((self.centerx + oldsize) * SCALEFACTOR, (self.centery - oldsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR),
                  ((self.centerx + oldsize) * SCALEFACTOR, (self.centery + oldsize) * SCALEFACTOR))

        pygame.draw.polygon(self.surface, COLORS[WALLCOLOR], points, LINESIZE)

        if LINESIZE == 0:
            pygame.draw.line(self.surface, COLORS["white"],
                             points[0], points[3],
                             self.linesize)

            pygame.draw.line(self.surface, COLORS["white"],
                             points[1], points[2],
                             self.linesize)

    def drawLeftEdge(self, drawingsize):

        oldsize = drawingsize * 2

        points = (((self.centerx - oldsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx - drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx - drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR),
                  ((self.centerx - oldsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR))

        pygame.draw.polygon(self.surface, COLORS[WALLCOLOR], points, LINESIZE)

        if LINESIZE == 0:
            pygame.draw.line(self.surface, COLORS["white"],
                             points[0], points[3],
                             self.linesize)

            pygame.draw.line(self.surface, COLORS["white"],
                             points[1], points[2],
                             self.linesize)

    def drawRightEdge(self, drawingsize):

        oldsize = drawingsize * 2

        points = (((self.centerx + oldsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery - drawingsize) * SCALEFACTOR),
                  ((self.centerx + drawingsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR),
                  ((self.centerx + oldsize) * SCALEFACTOR, (self.centery + drawingsize) * SCALEFACTOR))
        pygame.draw.polygon(self.surface, COLORS[WALLCOLOR], points, LINESIZE)

        if LINESIZE == 0:
            pygame.draw.line(self.surface, COLORS["white"],
                             points[0], points[3],
                             self.linesize)

            pygame.draw.line(self.surface, COLORS["white"],
                             points[1], points[2],
                             self.linesize)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Main:

    def __init__(self):

        os.environ['SDL_VIDEO_WINDOW_POS'] = "53, 7"
        self.env_ = Environment()
        self.screen = pygame.display.set_mode((self.env_.screenwidth, self.env_.screenheight))
        pygame.display.set_caption('Yet another maze')
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.maze = Maze(MAZE_SIZE[0], MAZE_SIZE[1], "paths")
        self.message = StringSurface()
        self.sounds = {}
        self.sounds["wallhit"] = pygame.mixer.Sound("sound/wallhit.wav")
        self.player = Player(self.maze, self.maze.entry_x)
        self.paper  = DrawScreen(self.env_, self.maze, self.player)
        self.clock  = pygame.time.Clock()
        self.running = True
        print()
        print("Welcome to the maze!")
        print()

        while self.running:
            self.clocktickt = self.clock.tick(FPS)
            self.screen.fill(COLORS["black"])

            result = self.processEvents()

            if result == pygame.K_LEFT:
                self.player.rotateLeft()

            if result == pygame.K_RIGHT:
                self.player.rotateRight()

            if result == pygame.K_UP:
                self.player.moveForward()

            if result == pygame.K_DOWN:
                self.player.turnBackwards()

            if result == pygame.K_SPACE and self.player.cell.isExit:
                self.running = False

            if result == pygame.K_q:
                self.running = False

            if self.player.status == "blocked" and not self.player.cell.isExit:
                self.sounds["wallhit"].play()
                self.message.show()

            if self.player.status in ("init", "rotated", "moved"):
                self.paper.clear()
                self.paper.drawCells()

            self.paper.draw(self.screen)
            self.message.draw(self.screen)
            self.player.status = None
            pygame.display.flip()

        pygame.quit()

    def processEvents(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

#-----------------------------------


class MazeGenerator:

    """ mazegenerator by "exciteabletom"; edited into a class by me:

        https://github.com/exciteabletom/mazegenerator """

    def __init__(self):
        pass
    
    def change_string_length(self, string, length):
        """
        Append spaces to a string until it reaches 'length'
        """
        diff = length - len(string)
        return string + (" " * diff)
    
    def print_maze(self):
        """
        Prints out the maze matrix in a human readable format, useful for debugging.
        """
        for i in self.maze:
            print(i)
        print("\n")
    
    def get_cell_value(self, coords):
        """
        Gets the value of the cell at the specified coordinates
    
        :param coords: tuple containing x and y values
        :return: value of the cell at the specifed coordinates
        """
        try:
            return self.maze[coords[0]][coords[1]]
        # Sometimes we get an IndexError if the maze doesn't have borders
        # This solution is not perfect, so it is still best practice to use borders
        except IndexError:
            return False
    
    def get_cells_by_value(self, value):
        """
        Get cell coordinates based on the value of the cell.
    
        :param value: The value to search cells for
        :return: list of all coordinates that contain the specified value
        """
        all_matching_cells = []  # the list containing all the coordinates of cells
        for row_index, row in enumerate(self.maze):
            for column_index, cell in enumerate(row):
                if cell == value:
                    all_matching_cells.append((row_index, column_index))
    
        return all_matching_cells
    
    def is_edge(self, coords):
        """
        Check if a piece is an edge or not.
    
        :param coords: A tuple (x,y)
        :return: True if piece is an edge piece False otherwise
        """
        if coords[0] == 0 or coords[0] == len(self.maze) - 1 \
              or coords[1] == 0 or coords[1] == len(self.maze[0]) - 1:  # if edge piece
            return True
    
        return False
    
    def get_cell_by_value(self, value):
        """
        The same as get_cells_by_value, except raises a ValueError if there is more than one cell with that value
    
        :param value: The value to search cells for
        :raises ValueError: If more then one of the value is found in the maze.
        :return: the cell coordinate that contains the value
        """
        values = self.get_cells_by_value(value)
        if len(values) > 1:
            raise ValueError("Expected only one cell to have value '{value}'. {len(values)} cells contained the value.")
    
        return values[0]
    
    def set_cell_value(self, coords, value):
        """
        Sets the value of a cell at the specified coordinates.
    
        :param coords: The coordinates of the cell to be changed
        :param value: The value we want the cell to be set to
        """
        self.maze[coords[0]][coords[1]] = value
    
    def check_cell_exists(self, coords):
        """
        Checks if a cell exists within the maze.
    
        :param coords: A tuple (x,y), representing a cell
        :return bool: True if cell exists, False otherwise
        """
        try:
            _ = self.maze[coords[0]][coords[1]]  # Will throw IndexError if the cell is out of the maze area
            return True  # Cell exists
        except IndexError:
            return False  # Cell doesn't exist
    
    def get_cell_neighbours(self, coords, empty_cell = None, directions = None):
        """
        Gets the values of all cells that neighbour the cell at the specified coordinates
    
        :param coords: Tuple containing the x and y values of the cell to check the neighbours of
        :param empty_cell: specifies an empty cell as a string
        :param directions: String containing directions to be checked for.
        :return: coordinates of all neighbours that have not been visited in
                    a list of tuples. Example: [(x,y), (x,y), (x,y)]
        """
        # different tuples that contain the coords of all positions
        # relative to our input tuple
        up = (coords[0] - 1, coords[1])
        down = (coords[0] + 1, coords[1])
        left = (coords[0], coords[1] - 1)
        right = (coords[0], coords[1] + 1)
    
        # list containing all directional tuples
        all_dirs = [up, down, right, left]
        if directions:
            all_dirs = []
            if "up" in directions:
                all_dirs.append(up)
            if "down" in directions:
                all_dirs.append(down)
            if "right" in directions:
                all_dirs.append(right)
            if "left" in directions:
                all_dirs.append(left)
    
            if not all_dirs:
                raise ValueError("Directions {directions} not recognised.")
    
        visitable_coordinates = []
    
        if type(empty_cell) == str:
            for dir in all_dirs:
                cell_value = self.get_cell_value(dir)
    
                if cell_value == empty_cell:
                    if self.is_edge(dir):
                        continue
    
                    if dir[0] < 0 or dir[1] < 0:  # If negative number
                        continue
    
                    visitable_coordinates.append(dir)  # Don't remove
    
        return visitable_coordinates
    
    def get_cell_neighbour_direction_names(self, coords, direction="all", empty_cell="."):
        """
        Checks which directions can be moved to.
    
        :param coords: A tuple (x,y).
        :param direction: String containing a directions to check. If left out will check every directions.
        :param empty_cell: What value is considered empty
        :return: A list containing directions that can be moved to. E.g. ["right", "up", "left"].
        """
    
        # different tuples that contain the coords of all positions
        # relative to our input tuple
        up = (coords[0] - 1, coords[1])
        down = (coords[0] + 1, coords[1])
        left = (coords[0], coords[1] - 1)
        right = (coords[0], coords[1] + 1)
    
        all_dirs = [(up, "up"), (down, "down"), (right, "right"), (left, "left")]
        good_dirs = []
    
        if direction == "all":
            for cell_data in all_dirs:
                if self.is_edge(cell_data[0]) or self.get_cell_value(cell_data[0]) != empty_cell:
                    continue
                good_dirs.append(cell_data[1])
    
        else:
            if direction == "up":
                index = 0
            elif direction == "down":
                index = 1
            elif direction == "right":
                index = 2
            elif direction == "left":
                index = 3
            else:
                raise ValueError("Direction {direction}, not recognised.")
    
            if get_cell_value(all_dirs[index]) == empty_cell and not is_edge(all_dirs[index]):
                good_dirs.append(direction)
    
        return good_dirs
    
    def next_to_edge(self, coords):
        """
        Function for checking if a cell is next to the edge of the maze.
    
        :param coords: Tuple (x, y)
        :rtype: bool
        :return: True if next to edge, false otherwise
        """
        next_to_wall = False
    
        if coords[0] == 1 or coords[0] == len(self.maze) - 2:
            next_to_wall = True
    
        elif coords[1] == 1 or coords[1] == len(self.maze[-1]) - 2:
            next_to_wall = True
    
        return next_to_wall
    
    def check_seed(self):
        """
        Creates a random seed if one is not defined already
        """
        seed = ""
        if not seed:  # If no user-defined seed
            # Create random seed
            random_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                                "t", "u", "v", "w" "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            for _ in range(15):
                rand_bool = random.random() < 0.5
                rand_char = random_chars[random.randint(0, len(random_chars) - 1)]
    
                if rand_bool:
                    rand_char = rand_char.upper()
    
                seed = seed + rand_char
    
        random.seed(seed)
    
    def init_maze(self, width, height):
        """
        Initialises a maze with only walls
        :param width: The width of the maze
        :param height: The height of the maze
        """
        self.maze = []
    
        for _ in range(height):
            self.maze.append([])
            for _ in range(width):
                self.maze[-1].append("#")
    
    def branch(self, coords, direction, no_exit = False, noise_offset = 0.0):
        """
        Branches out to the side of a target cell, either left, right or down, used to add tree like structure
    
        :param coords: (x,y) indicating a cell position
        :param direction: 'left', 'right' or 'down'
        :param no_exit: Bool indicating whether to not stop randomly
        :param noise_offset: float that affects some of the random chances
        :return: The cell that was last visited
        :rtype: tuple
        """
    
        while True:
            rand_float = random.random() + noise_offset
            if rand_float < 0.05 and not no_exit:
                return coords
    
            neighbour_directions = self.get_cell_neighbour_direction_names(coords, empty_cell="#")
    
            if direction in neighbour_directions:
                final_direction = direction
                if 0.05 < rand_float < 0.45 + noise_offset:
                    final_direction = "down"
    
                try:
                    next_coords = self.get_cell_neighbours(coords, "#", final_direction)[0]
                except IndexError:
                    return coords
    
                if not self.is_edge(next_coords):
                    if next_coords[0] == len(self.maze) - 1:
                        breakpoint()
                    self.set_cell_value(next_coords, ".")
                    coords = next_coords
                else:
                    return coords
            else:
                return coords
    
    def init_solution_path(self):
        """
        Creates a randomized solution path through the maze.
        """
    
        # Find the beginning of the maze
        start_pos = random.randint(1, len(self.maze[0]) - 2)
        self.maze[0][start_pos] = "s"
        start = self.get_cell_by_value("s")
    
        # Set the current cell to be the cell under start
        current_cell = (start[0] + 1, start[1])
        self.set_cell_value(current_cell, ".")
    
        no_up = True
    
        if random.random() < 0.5:
            h_prefer = "right"
            not_h_prefer = "left"
        else:
            h_prefer = "left"
            not_h_prefer = "right"
    
        rows = len(self.maze) - 2
        last_row = 0
    
        # Path from start
        while True:
            if current_cell[0] != last_row:
                last_row = current_cell[0]
    
            if current_cell[0] == len(self.maze) - 2:  # If on second last row of maze
                self.set_cell_value((len(self.maze) - 1, current_cell[1]), "e")
                break
    
            # Possible directions we could travel to
            directions = self.get_cell_neighbour_direction_names(current_cell, empty_cell="#")
    
            if no_up and "up" in directions:  # Currently will always be triggered
                directions.remove("up")
    
            # A random direction
            rand_direction = directions[random.randint(0, len(directions) - 1)]
    
            if h_prefer in directions and random.random() < 0.6:
                rand_direction = h_prefer
    
            elif random.random() < 0.01:
                current_cell = self.branch(current_cell, h_prefer)
                last_row = current_cell[0]
                if random.random() < 0.5:
                    h_prefer, not_h_prefer = (not_h_prefer, h_prefer)
                continue
    
            next_cell = self.get_cell_neighbours(current_cell, "#", rand_direction)[0]
            self.set_cell_value(next_cell, ".")
    
            if self.next_to_edge(current_cell):
                if random.random() < 0.60:
                    h_prefer, not_h_prefer = (not_h_prefer, h_prefer)
    
            current_cell = next_cell
    
    def expand_rows(self, noise_offset):
        """
        'expands' rows by adding random paths on, above, and below the rows
        :param noise_offset: An offset applied to some of the random float values generated
                                A negative offset reduces noise, a positive one increases noise
        """
        for row_index, row in enumerate(self.maze):
            if row_index % 3 == 0:
                continue
    
            if row_index == len(self.maze) - 1:
                continue
    
            for cell_index, cell in enumerate(row):
                if cell_index in (0, len(self.maze[0]) - 1):
                    continue
    
                cell_coords = (row_index, cell_index)
                rand = random.randint(0, 13)
    
                if cell == "#":  # If cell is wall
                    cell_neighbours = self.get_cell_neighbours(cell_coords, empty_cell=".")
    
                    if cell_neighbours and rand < 1:
                        self.set_cell_value(cell_coords, ".")
                    elif rand in (2, 3):
                        rand_direction = ""
    
                        if random.random() < 0.005:
                            rand_direction = "down"
                        elif rand == 2:
                            rand_direction = "left"
                        elif rand == 3:
                            rand_direction = "right"
                        else:
                            raise ValueError("DEVERROR: Random integer out of range")
    
                        self.branch(cell_coords, rand_direction, random.random() < 0.001, noise_offset)
    
    def generate(self, width, height, noise_bias):
        """
        Main function that creates the maze.
        :param width: Width of the matrix
        :param height: Height of the matrix
        :param noise_bias: Either "wall", "less", "none", or and empty string indicating no bias
        """
        self.check_seed()
        self.init_maze(width, height)
        self.init_solution_path()
    
        if noise_bias != "none":  # If we should generate noise
            noise_offset = 0
    
            if noise_bias == "walls":  # Draw less paths
                print("Creating more walls")
                noise_offset = -0.09
    
            elif noise_bias == "paths":  # Draw more paths
                # print("Creating more paths")
                noise_offset = 0.25
    
            self.expand_rows(noise_offset)
        else:
            print("Only rendering solution path")
    

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        self.wall_turns = {"N" : ("W", "E"), "W" : ("S", "N"),
                           "E" : ("N", "S"), "S" : ("E", "W")}
        self.isEntrance = False
        self.isExit     = False
        self.shapes     = {}

    def setWalls(self, walls):
        self.walls = walls

    def calculateShapes(self, direction):
        self.shapes = {}
        if self.has_wall(direction):
            self.shapes["center_wall"] = True
        if self.has_wall(self.wall_turns[direction][0]):
            self.shapes["left_wall"] = True
        if self.has_wall(self.wall_turns[direction][1]):
            self.shapes["right_wall"] = True


    def getRotate(self, direction, turn):
        if turn == "left":
            return self.wall_turns[direction][0]
        else:
            return self.wall_turns[direction][1]

    def has_wall(self, direction):
        if self.walls[direction]:
            return True
        else:
            return False

class Maze:

    def __init__(self, width, height, noise_bias):

        self.width  = width
        self.height = height
        self.m      = MazeGenerator()
        self.m.generate(width, height, noise_bias)
        self.rawMazeToCellMaze()
        # self.m.print_maze()

    def rawMazeToCellMaze(self):
        self.maze_map = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y)
                cell.setWalls(self.getCellWalls(x, y))
                if self.m.maze[y][x] == "s":
                    cell.isEntrance = True
                    self.entry_x = x
                if self.m.maze[y][x] == "e":
                    cell.isExit = True
                row.append(cell)
            self.maze_map.append(row)

    def getCellWalls(self, x, y):
        """ The x and y coordinates still are the x and y coordinates of the
            maze. However, if you store several rows in an array, the first
            brackets refer to the y value. """
        if self.m.maze[y][x] == "#":
            walls = {'N': True, 'S': True, 'E': True, 'W': True}
            return walls
        walls = {}
        if y == 0:
            walls["N"] = True
        else:
            if self.m.maze[y - 1][x] == "#":
                walls["N"] = True
            else:
                walls["N"] = False

        if x == 0:
            walls["W"] = True
        else:
            if self.m.maze[y][x - 1] == "#":
                walls["W"] = True
            else:
                walls["W"] = False

        if x == self.width - 1:
            walls["E"] = True
        else:
            if self.m.maze[y][x + 1] == "#":
                walls["E"] = True
            else:
                walls["E"] = False

        if y == self.height - 1:
            walls["S"] = True
        else:
            if self.m.maze[y + 1][x] == "#":
                walls["S"] = True
            else:
                walls["S"] = False

        return walls


if __name__ == '__main__':
    Main()
