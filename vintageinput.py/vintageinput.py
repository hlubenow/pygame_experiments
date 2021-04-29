#!/usr/bin/python
# coding: utf-8

"""
    vintageinput.py 1.0 - Creates an 8-bit style text input environment in Pygame

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
import os
import pygame

SCALEFACTOR = 3
FPS         = 50

CHARSETFILENAME = "ZX_Spectrum_character_set.png"

COLORSET = "zx"


class CharacterSurface:

    def __init__(self, characterbytes, colortuple):
        self.characterbytes = characterbytes
        self.surface     = pygame.Surface((8 * SCALEFACTOR, 8 * SCALEFACTOR))
        self.surface     = self.surface.convert_alpha()
        self.rect        = self.surface.get_rect()
        self.colortuple  = colortuple
        self.opaque      = (0, 0, 0, 0)
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
                    c = self.opaque
                rect.topleft = (t_x * SCALEFACTOR, t_y * SCALEFACTOR)
                self.surface.fill(c, rect)
                t_x += 1
            t_y += 1
            t_x -= 8


class CharacterSetBuilder:

    def __init__(self, colorset):
        self.colorset           = colorset
        self.spritesheetsurface = pygame.image.load(CHARSETFILENAME)
        self.spritesheetsurface = self.spritesheetsurface.convert()
        self.rect               = pygame.Rect((0, 0), (8, 8))
        self.surfaces           = {}
        self.buildSurfaces()
        self.createTextCursor()

    def createTextCursor(self):
        bytes_ = []
        byte_  = "{0:08b}".format(255)
        for i in range(8):
            bytes_.append(byte_)
        self.surfaces["[textcursor]"] = CharacterSurface(bytes_, self.colorset["textcursor"])

    def getSurfaces(self):
        return self.surfaces

    def buildSurfaces(self):
        c = 32
        for char_y in range(6):
            for char_x in range(16):
                self.surfaces[chr(c)] = CharacterSurface(self.getCharCellValues(char_x, char_y), self.colorset["ink"])
                c += 1

    def getCharCellValues(self, char_x, char_y):
        # n1 and n2, because the imagie is scaled by 2:
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
        self.paperwidth  = 256
        self.paperheight = 192
        self.char_width  = self.paperwidth  / 8 # 32
        self.char_height = self.paperheight / 8 # 24
        self.pc_paperwidth  = self.paperwidth  * SCALEFACTOR
        self.pc_paperheight = self.paperheight * SCALEFACTOR
        self.borderwidth = 24
        self.borderheight = 12
        self.pc_borderwidth = self.borderwidth * SCALEFACTOR
        self.pc_borderheight = self.borderheight * SCALEFACTOR
        self.screenwidth  = self.pc_paperwidth + 2 * self.pc_borderwidth
        self.screenheight = self.pc_paperheight + 2 * self.pc_borderheight


class Paper:

    def __init__(self, env_, colorset):
        self.colorset     = colorset
        self.env_         = env_
        self.surface      = pygame.Surface((self.env_.pc_paperwidth, self.env_.pc_paperheight))
        self.surface      = self.surface.convert()
        self.rect         = self.surface.get_rect()
        self.rect.topleft = (self.env_.pc_borderwidth, self.env_.pc_borderheight)

    def clear(self):
        self.surface.fill(self.colorset["paper"])

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class TextField:

    def __init__(self, env_, charset, paper):
        self.env_   = env_
        self.borders = {"left"   : 2,
                        "right"  : self.env_.char_width - 1,
                        "top"    : 0,
                        "bottom" : self.env_.char_height - 1}
        self.paper  = paper
        self.paper.clear()
        self.width  = self.borders["right"] - self.borders["left"]
        self.height = self.borders["bottom"] - self.borders["top"]
        self.drawposition_x = self.borders["left"]
        self.drawposition_y = self.borders["top"]
        self.textbuffer = []
        self.viewpoint = 0
        self.bufferposition = -1
        self.lsep = "\n"
        self.charset = charset
        self.textcursor = self.charset["[textcursor]"]

    def print_(self, string_):
        self.addChar(self.lsep)
        for i in string_:
            self.addChar(i)

    def printREADY(self):
        self.addChar(self.lsep)
        for i in "READY":
            self.addChar(i)
        self.addChar(self.lsep)

    def moveCursorLeft(self):
        if self.bufferposition > 0:
            self.bufferposition -= 1
            self.refresh()

    def moveCursorRight(self):
        if self.bufferposition < len(self.textbuffer) - 1:
            self.bufferposition += 1
            self.refresh()

    def cursorToStart(self):
        self.bufferposition = 0
        self.refresh()

    def cursorToEnd(self):
        self.bufferposition = len(self.textbuffer) - 1
        self.refresh()

    def addChar(self, char):
        self.bufferposition += 1
        self.textbuffer.insert(self.bufferposition, char)
        self.refresh()

    def backspace(self):
        if self.bufferposition >= 0:
            del self.textbuffer[self.bufferposition]
            self.bufferposition -= 1
            self.refresh()

    def delChar(self):
        if self.bufferposition < len(self.textbuffer) - 1:
            del self.textbuffer[self.bufferposition + 1]
            self.refresh()

    def getViewPoint(self):

        """ Trying to calculate the part of "self.textbuffer" to be shown on the screen.
            Should enable scrolling. """

        self.viewpoint = 0
        lines = []
        chars = 0
        for i in range(len(self.textbuffer)):
            if chars > self.width or self.textbuffer[i] == self.lsep:
                lines.append(i)
                chars = 0
            chars += 1
        n = len(lines) - self.height
        if n >= 0:
            self.viewpoint = lines[n]

    def refresh(self):
        """ Display contents of 'self.textbuffer' on the screen. """
        self.paper.clear()
        self.drawposition_y = self.borders["top"]
        self.drawposition_x = self.borders["left"]
        self.getViewPoint()

        if self.bufferposition == -1:
            self.drawCursor()
            self.drawposition_x += 1

        for i in range(self.viewpoint, len(self.textbuffer), 1):

            if self.textbuffer[i] != self.lsep:
                self.drawChar(self.textbuffer[i])
                self.drawposition_x += 1

            if self.textbuffer[i] == self.lsep or self.drawposition_x > self.borders["right"]:
                self.drawposition_y += 1
                self.drawposition_x = self.borders["left"]

            if i == self.bufferposition:
                self.drawCursor()
                self.drawposition_x += 1

    def drawChar(self, char):
        pc_x = self.drawposition_x * 8 * SCALEFACTOR
        pc_y = self.drawposition_y * 8 * SCALEFACTOR
        l = self.charset[char]
        l.setPosition(pc_x, pc_y)
        self.paper.surface.blit(l.surface, l.rect)

    def drawCursor(self):
        pc_x = self.drawposition_x * 8 * SCALEFACTOR
        pc_y = self.drawposition_y * 8 * SCALEFACTOR
        self.textcursor.setPosition(pc_x, pc_y)
        self.paper.surface.blit(self.textcursor.surface, self.textcursor.rect)

class Main:

    def __init__(self):
        self.data  = Data()
        self.env_  = Environment()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "191, 6"
        # Reducing the sound buffer size to avoid latency:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((self.env_.screenwidth, self.env_.screenheight))
        pygame.display.set_caption("Text Input")
        self.charset = CharacterSetBuilder(self.data.colorset)
        self.charset = self.charset.getSurfaces()
        self.clock = pygame.time.Clock()
        self.paper = Paper(self.env_, self.data.colorset)
        self.tfield = TextField(self.env_, self.charset, self.paper)
        self.tfield.printREADY()
        self.sounds = {}
        self.sounds["click"] = pygame.mixer.Sound("sound/click.wav")
        self.running = True

        while self.running:
            self.clock.tick(FPS)
            self.screen.fill(self.data.colorset["border"])
            result = self.getASCIICodeFromKeyboard()
            if result["quit"]:
                self.running = False

            if result["keycode"] not in (0, 303, 304):
                self.playSound("click")

            if result["keycode"] == pygame.K_LEFT:
                self.tfield.moveCursorLeft()
            elif result["keycode"] == pygame.K_RIGHT:
                self.tfield.moveCursorRight()
            elif result["keycode"] == pygame.K_BACKSPACE:
                self.tfield.backspace()
            elif result["keycode"] == pygame.K_DELETE:
                self.tfield.delChar()
            elif result["keycode"] == pygame.K_HOME:
                self.tfield.cursorToStart()
            elif result["keycode"] == pygame.K_END:
                self.tfield.cursorToEnd()
            elif result["keycode"] == pygame.K_RETURN:
                self.tfield.print_("")
                self.tfield.printREADY()
            # Letters:
            elif result["keycode"] > 31 and result["keycode"] < 127:
                self.tfield.addChar(chr(result["keycode"]))

            self.paper.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


    def playSound(self, name):
        self.sounds[name].play()

    def getASCIICodeFromKeyboard(self):

        result = {"keycode" : 0, "quit": False}
        shift_pressed  = False

        if pygame.key.get_mods() & (pygame.KMOD_SHIFT | pygame.KMOD_LSHIFT):
            shift_pressed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result["quit"] = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_F10):
                    result["quit"] = True
                    return result

                if shift_pressed:
                    # ?:
                    if event.key == 223:
                        result["keycode"] = 63
                        return result

                    if event.key == 32:
                        result["keycode"] = event.key
                        return result

                    # a-z to A-Z:
                    if event.key >= 97 and event.key <= 122:
                        result["keycode"] = event.key - 32
                        return result

                    for i in self.data.shiftvals.keys():
                        if event.key == i:
                            result["keycode"] = self.data.shiftvals[i]
                            return result
                else:
                    result["keycode"] = event.key

        return result

#------------------------------------------------

class Data:

    def __init__(self):
        unshifted = """124567890+#,.-"""
        shifted   = """!"$%&/()=*';:_"""
        self.shiftvals = {}
        for i in range(len(unshifted)):
            self.shiftvals[ord(unshifted[i])] = ord(shifted[i])

        self.colors = {"black"            : (0, 0, 0),
                       "red"              : (192, 0, 0),
                       "white"            : (189, 190, 197),
                       "at_default_blue"  : (28, 113, 198),
                       "at_default_white" : (112, 199, 255)}

        self.colorsets = { "at" : {"border"     : "black",
                                   "paper"      : "at_default_blue",
                                   "ink"        : "at_default_white",
                                   "textcursor" : "at_default_white"},
                           "zx" : {"border"     : "red",
                                   "paper"      : "white",
                                   "ink"        : "black",
                                   "textcursor" : "black"} }

        self.colorset = {}
        print COLORSET
        for i in self.colorsets[COLORSET].keys():
            self.colorset[i] = self.colors[self.colorsets[COLORSET][i]]


if __name__ == '__main__':
    Main()
