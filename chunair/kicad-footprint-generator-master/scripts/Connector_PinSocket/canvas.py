#!/usr/bin/env python

#
# Generic extension module for KicadModTree in the kicad-footprint-generator framework
#
# This module requires the kicad-footprint-generator framework
# by Thomas Pointhuber, https://github.com/pointhi/kicad-footprint-generator
#
# This module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

#
# This module contains wrapper classes and methods for parts
# of the KicadModTree primitives.
# They provide "turtle style" drawing using relative moves in order
# to simplify the math involved in calculating and keeping track of vertex coordinates.
# They also introduce the concept of canvases for drawing the different layers, this
# to simplify drawing and provide functionality such as transparent grid align
# and method chaining.
# A canvas is somewhat similar to a workplane in CadQuery which is
# often used for creating KiCad 3D models.
#
# (C) 2017 by Terje Io, <http://github.com/terjeio>

#
# NOTE:
# The code for the the Keepout class is loosely based on code from drawing_tools.py
# Currently oval and rectangular keepout zones are respected
# for horizontal and vertical lines, only basic support (bounding box only) for diagonal lines.
# Arcs and circles are not yet handled. On TODO: list.
# More testing needs to be done for edge cases, such as for lines inside
# the bounding box but outside the keepout area proper.
#

# 2017-11-25

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\..")

from collections import namedtuple

from KicadModTree import Point
from KicadModTree.nodes.base import Line, Arc, Circle, Text, Pad
from KicadModTree.nodes.specialized import RectFill
from KicadModTree.util.kicad_util import formatFloat

class Layer:

    _DEFAULT_LINE_WIDTHS = {'F.SilkS': 0.12,
                            'B.SilkS': 0.12,
                            'F.Fab':   0.1,
                            'B.Fab':   0.1,
                            'F.CrtYd': 0.05,
                            'B.CrtYd': 0.05}

    _DEFAULT_LINE_WIDTH        = 0.15
    _DEFAULT_TEXT_OFFSET       = 1.0
    _DEFAULT_TEXT_SIZE_MIN     = 0.25
    _DEFAULT_TEXT_SIZE_MAX     = 2.00
    _DEFAULT_GRID_CRT          = 0.05
    _DEFAULT_OFFSET_CRT        = 0.25
    _DEFAULT_SOLDERMASK_MARGIN = 0.2 # clearance?

    def __init__(self, footprint, layer='F.Fab', origin=(0,0), line_width=None, offset=None):
        self.footprint = footprint
        self.layer = layer
        self.polyline_start = None
        self.gridspacing = None
        self.keepout = None
        self.setOrigin(origin[0], origin[1])
        self.txt_size = [1.0] * 2
        self.setTextDefaults()
        self.setTextSize(1.0)
        self.txt_offset = self._DEFAULT_TEXT_OFFSET
        if offset == None and layer.split('.')[1] == 'CrtYd':
            offset = self._DEFAULT_OFFSET_CRT
        if offset != None:
            self.offset = offset
        self.auto_offset = offset == None
        self.goHome()
        self.setLineWidth(self._DEFAULT_LINE_WIDTHS.get(layer, self._DEFAULT_LINE_WIDTH) if line_width == None else line_width)
        if layer.split('.')[1] == 'CrtYd':
            self.setGridSpacing(self._DEFAULT_GRID_CRT)
#        else:
#            self.setGridSpacing(0.001)

    @staticmethod        
    def getBevel(width, height):
        return min(1.0, min(width, height) * 0.25)

    def setOrigin(self, x, y):
        self.origin = (self._align(x), self._align(y))
        self.goHome()
        return self

    def getOrigin(self):
        return self.origin

    def setLineWidth(self, width):
        self.line_width = width
        if self.auto_offset:
            self.offset = self.line_width / 2.0
        return self

    def getSoldermaskMargin(self):
        return self._DEFAULT_SOLDERMASK_MARGIN

    def setTextDefaults(self, max_size=None, min_size=None):
        if max_size == None and min_size == None:
            self.text_size_min = self._DEFAULT_TEXT_SIZE_MIN
            self.text_size_max = self._DEFAULT_TEXT_SIZE_MAX
        else:
            if max_size != None:
                self.text_size_max = round(max_size, 2)
            if min_size != None:
                self.text_size_min = round(min_size, 2)
        return self    

    def setTextSize(self, height, width=None, thickness=None):
        height = round(height, 2)
        self.txt_size[0] = min(max(height, self.text_size_min), self.text_size_max)
        self.txt_size[1] = min(max(height if width == None else round(width, 2), self.text_size_min), self.text_size_max)
        self.txt_thickness = round(self.txt_size[0] * 0.15 if thickness == None else thickness, 2)
        return self

    def setGridSpacing(self, grid):
        self.gridspacing = grid
        if self.gridspacing != None:
            self.alignToGrid()
        return self

    def goHome(self):
        self.x = self.origin[0]
        self.y = self.origin[1]
        return self

    def goto(self, x, y):
        self.x = self._align(x)
        self.y = self._align(y)
        return self

    def gotoX(self, x):
        self.x = self._align(x)
        return self

    def gotoY(self, y):
        self.y = self._align(y)
        return self

    def jump(self, x, y):
        self.x += self._align(x)
        self.y += self._align(y)
        return self

    def _align(self, value):
        return round(value, 6) if self.gridspacing == None\
                      else (math.ceil(value / self.gridspacing) * self.gridspacing if value > 0.0 else math.floor(value / self.gridspacing) * self.gridspacing)

    def alignToGrid(self):
        self.x = self._align(self.x)
        self.y = self._align(self.y)
        self.setOrigin(self._align(self.origin[0]), self._align(self.origin[1]))
        return self

    def _line(self, x, y):
        if self.keepout != None:
            segments = self.keepout.processLine(self.x, self.y, self.x + x, self.y + y)
            for line in segments: # TODO: move grid alignment to keepout code?
                line[0] = self._align(line[0])
                line[1] = self._align(line[1])
                line[2] = self._align(line[2])
                line[3] = self._align(line[3])
                self.footprint.append(Line(start=[line[0], line[1]], end=[line[2], line[3]], layer=self.layer, width=self.line_width))
        else:            
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x + x, self.y + y], layer=self.layer, width=self.line_width))

    def to(self, x, y, draw=True):
        x = self._align(x)
        y = self._align(y)
        if draw:
            self._line(x, y)
        self.x += x
        self.y += y
        return self

    def left(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self._line(-distance, 0.0)
        self.x -= distance
        return self

    def right(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self._line(distance, 0.0)
        self.x += distance
        return self

    def up(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self._line(0.0, -distance)
        self.y -= distance
        return self

    def down(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self._line(0.0, distance)
        self.y += distance
        return self

    def polyline(self, vertices, close=False):
        if self.polyline_start == None:
            self.polyline_start = (self.x, self.y)
        for vertex in vertices:
            x = self._align(vertex[0])
            y = self._align(vertex[1])
            self._line(self.x + x, self.y + y)
            self.x += x
            self.y += y
        if close:
            self.close()
        return self

    def close(self):
        if self.polyline_start != None:
            if self.x != self.polyline_start[0] or self.x != self.polyline_start[1]:
                self._line(self.polyline_start[0], self.polyline_start[1])
            self.polyline_start = None
        return self

    def arc(self, center_x, center_y, angle):
        arc = Arc(start=[self.x, self.y], center=[self.x + center_x, self.y + center_y], angle=angle, layer=self.layer, width=self.line_width)
        self.footprint.append(arc)
        end = arc._calulateEndPos()    
        self.x += center_x + end.y
        self.y += center_y + end.x
        return self

    def circle(self, radius, filled=False):
        if filled:
            line_width = radius / 3.0 + self.line_width / 2.0
            r = line_width / 2.0
            while r < radius:
                self.footprint.append(Circle(center=[self.x, self.y], radius=r, layer=self.layer, width=line_width))        
                r += line_width - self.line_width / 2.0
        else:
            line_width = round(min(self.line_width, radius / 2.0), 3)
            self.footprint.append(Circle(center=[self.x, self.y], radius=radius, layer=self.layer, width=line_width))
        return self
   
    def fillrect(self, w, h): #TODO: add origin handling
        x = self.x
        y = self.y
        w = self._align(w)
        h = self._align(h - self.line_width)
        
        #self.jump(self._align(-w / 2.0), self._align(-h / 2.0))
        
        l = math.ceil(h / self.line_width)
        h = h / l

        self.jump(0.0, self.line_width / 2.0)

        while(l > 0):
            self._line(w, 0.0)
            self.jump(0.0, h)
            l -= 1   

        self.x = x
        self.y = y
        return self

    def rect(self, w, h, bevel=(0.0, 0.0, 0.0, 0.0), draw=(True, True, True, True), origin='center'):

        x = self.x
        y = self.y
        w = self._align(w)
        h = self._align(h)
        
        if type(bevel) in [int, float]:
            bevel = [bevel] * 4
        elif bevel == None:
            bevel = [0.0] * 4

        if origin == 'center':
            self.jump(self._align(-w / 2.0), self._align(-h / 2.0))

        if bevel[0] != 0.0:
            self.jump(bevel[0], 0.0)

        self.right(w - bevel[0] - bevel[1], draw[0])

        if bevel[1] != 0.0:
            self.to(bevel[1], bevel[1])

        self.down(h - bevel[1] - bevel[2], draw[1])

        if bevel[2] != 0.0:
            self.to(-bevel[2], bevel[2])

        self.left(w - bevel[3] - bevel[2], draw[2])

        if bevel[3] != 0.0:
            self.to(-bevel[3], -bevel[3])

        self.up(h - bevel[3] - bevel[0], draw[3])

        if bevel[0] != 0.0:
            self.to(bevel[0], -bevel[0])

        self.x = x
        self.y = y

        return self

    def rrect(self, w, h, radius, origin='center'):

        x = self.x
        y = self.y
        w = self._align(w)
        h = self._align(h)

        if origin == 'center':
            self.jump(self._align(-w / 2.0), self._align(-h / 2.0))

        w -= radius * 2.0          
        h -= radius * 2.0          

        self.jump(radius, 0.0)
        self.right(w)
        self.arc(0.0, radius, 90.0)
        self.down(h)
        self.arc(-radius, 0.0, 90.0)
        self.left(w)
        self.arc(0.0, -radius, 90.0)
        self.up(h)
        self.arc(radius, 0.0, 90.0)

        self.x = x
        self.y = y

        return self

    def text(self, type, text, rotation=0):
        self.footprint.append(Text(type=type, text=text, at=[self.x, self.y], rotation=rotation, layer=self.layer, size=self.txt_size, thickness=self.txt_thickness))
        return self

# TODO: add methods for offsetting etc
class PolyLine ():

    def __init__(self, vertices=None):
        self.vertices = []
        if vertices != None:   
            for vertex in vertices:
                self.vertices.append(Point(vertex))

    def __getattr__(self, name):
        if name == "isClosed":
            return False if len(self.vertices) < 3 else self.vertices[0].x == self.vertices[-1].x and self.vertices[0].y == self.vertices[-1].y
        else:
            raise AttributeError
        
    def append(self, x, y):
        self.vertices.append([x, y])
        return self

    
class PadLayer:

    def __init__(self, footprint, size, type, shape, shape_first=None, drill=None, layers=None, x_offset=0.0, y_offset=0.0):
        self.footprint = footprint
        self.type = type
        self.layers = layers
        self.shape = shape
        self.shape_first = shape if shape_first == None else shape_first
        self.size = size
        self.drill = 0.5 if drill == None and type == Pad.TYPE_SMT else drill
        self.x_offset = x_offset
        self.y_offset = y_offset
        self._init_layers(layers)
        self.p = 1
        self.last_pad = None

    def _init_layers(self, layers):

        if layers == None:
            if self.type == Pad.TYPE_SMT:
                layers = Pad.LAYERS_SMT
            elif self.type == Pad.TYPE_THT:
                layers = Pad.LAYERS_THT

        self.layers=layers

    def add(self, x, y, number=None, type=None, shape=None, size=None, x_offset=None, y_offset=None):

        if number == None:
            number = self.p
            self.p += 1

        if x_offset == None:
            x_offset = self.x_offset

        if y_offset == None:
            y_offset = self.y_offset
            
        if shape == None:
            shape=self.shape_first if number == 1 else self.shape

        self.last_pad = Pad(number=number,
                            type=self.type if type == None else type,
                            shape=shape,
                            at=[x + x_offset, y + y_offset],
                            size=self.size if size == None else size,
                            drill=self.drill, layers=self.layers)
        self.footprint.append(self.last_pad)
        return self

    def getLast(self):
        return self.last_pad

_RectWH = namedtuple("_RectWH", [
    'x',
    'y',
    'height',
    'width'
])

class _Point: 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(x={x}, y={y})".format(x=formatFloat(self.x), y=formatFloat(self.y))
        
class _Line: 
    def __init__(self, a, b, x1=None, y1=None, normalize=False):
        if x1 == None and y1 == None:
            self._add_points(a, b, normalize)
        else:    
            self._add_points(_Point(a, b), _Point(x1, y1), normalize)

    def _add_points(self, a, b, normalize):
        if normalize:  
            self.x0 = round(min(a.x, b.x), 8)
            self.x1 = round(max(a.x, b.x), 8)
            self.y0 = round(min(a.y, b.y), 8)
            self.y1 = round(max(a.y, b.y), 8)
        elif a.y < b.y:
            self.x0 = a.x
            self.x1 = b.x
            self.y0 = a.y
            self.y1 = b.y           
        else:
            self.x0 = b.x
            self.x1 = a.x
            self.y0 = b.y
            self.y1 = a.y           

    def __repr__(self):
        return "(x0={x0}, y0={y0}, x1={x1}, y1={y1})".format(x0=formatFloat(self.x0), y0=formatFloat(self.y0),
                                                             x1=formatFloat(self.x1), y1=formatFloat(self.y1))

class _Keepout:
    def __init__(self, a, b, x1=None, y1=None, radius=0.0):
        self.lines = []
        self.radius = radius
        if x1 == None and y1 == None:
            self._add_points(a, b)
        else:    
            self._add_points(_Point(a, b), _Point(x1, y1))

    def _add_points(self, a, b):        
        self.x0 = round(min(a.x, b.x), 5)
        self.x1 = round(max(a.x, b.x), 5)
        self.y0 = round(min(a.y, b.y), 5)
        self.y1 = round(max(a.y, b.y), 5)

    def pointIsInside(self, x, y):
        x = round(x, 5); y = round(y, 5)
        return x >= self.x0 and x <= self.x1 and y >= self.y0 and y <= self.y1

    def _feq(self, a, b):
        return abs(a-b) < 0.0001
    
    def _bbox_overlap(self, bbox):
        x0 = min(bbox.x0, bbox.x1)
        x1 = max(bbox.x0, bbox.x1)
        y0 = min(bbox.y0, bbox.y1)
        y1 = max(bbox.y0, bbox.y1)
        return not (self.x0 < x1 and self.x1 > x0 and self.y0 > y1 and self.y1 < y0)

    def lineIntersects(self, l):
        
        # skip proccesing if line bounding box is completely outside keepout bounding box
        if not self._bbox_overlap(l):
            return False
    
        points = []
  
        # get lines representing keepout bounding box
        if len(self.lines) == 0:
            self.lines.append(_Line(self.x0, self.y0, self.x1, self.y0))
            self.lines.append(_Line(self.x1, self.y0, self.x1, self.y1))
            self.lines.append(_Line(self.x0, self.y1, self.x1, self.y1))
            self.lines.append(_Line(self.x0, self.y0, self.x0, self.y1))
        
        # find and return intersecting points
        a1 = l.y1 - l.y0
        b1 = l.x0 - l.x1
        lr = l.x1 > l.x0

        i = 0

        for k in self.lines:
            a2 = k.y1 - k.y0
            b2 = k.x0 - k.x1
            d = a1 * b2 - a2 * b1
                    
            if d != 0.0:
                c2 = a2 * k.x0 + b2 * k.y0;
                c1 = a1 * l.x0 + b1 * l.y0
                xp = (b2 * c1 - b1 * c2) / d
                yp = (a1 * c2 - a2 * c1) / d
  
                ka = (xp >= l.x0 and xp <= l.x1) if lr else (xp <= l.x0 and xp >= l.x1)
                kb = self._feq(xp, k.x0) if k.x0 == k.x1 else self._feq(yp, k.y0)

                if ka and kb and self.pointIsInside(xp, yp):
                    if lr and (i == 0 or i == 3):
                        points.insert(0, [xp, yp, i])
                    else:
                        points.append([xp, yp, i])
            i += 1       

        return False if len(points) == 0 else points

    def HlineIntersects(self, y):
        return y > self.y0 and y < self.y1

    def VlineIntersects(self, x):
        return round(x, 8) > self.x0 and round(x, 8) < self.x1

    def _HLineTrim(self, y, r):
        h = (self.y0 + r - y if y < self.y0 + r else y - self.y1 + r)
        return r - math.sqrt(r * r - h * h)
        
    def _VLineTrim(self, x, r):
        h = (self.x0 + r - x if x < self.x0 + r else x - self.x1 + r)
        return r - math.sqrt(r * r - h * h)

    def HLineTrim(self, l):

        line = _Line(l[0], l[1], l[2], l[3], normalize=True)

        # check if line is outside rectangular bounding box and exit if so
        if line.x1 < self.x0 or line.x0 > self.x1:
            return False

        # check if line completely inside rectangular bounding box and exit with no segments if so
        if self.radius == 0.0 and line.x0 >= self.x0 and line.x1 <= self.x1:
            return []

        r = self.radius
        segments = []

        if r == 0.0 or (line.y0 >= self.y0 + r and line.y0 <= self.y1 - r):
            if line.x0 < self.x0:
                segments.append([line.x0, line.y0, self.x0, line.y1])
            if line.x1 > self.x1:
                segments.append([self.x1, line.y0, line.x1, line.y1])
        elif line.x1 > self.x0 and line.x0 < self.x1:
            h = self._HLineTrim(line.y0, r) 
            if line.x0 < self.x0 + r:
                segments.append([line.x0, line.y0, min(line.x1, self.x0 + h), line.y1])
            if line.x1 > self.x1 - r:
                segments.append([max(line.x0, self.x1 - h), line.y0, line.x1, line.y1])
        return False if len(segments) == 0 else segments

    def VLineTrim(self, l):

        line = _Line(l[0], l[1], l[2], l[3], normalize=True)

        # check if line is outside
        if line.y1 <= self.y0 or line.y0 >= self.y1:
            return False

        # check if line completely inside rectangular bounding box and exit with no segments if so
        if self.radius == 0.0 and line.y0 >= self.y0 and line.y1 <= self.y1:
            return []

        r = self.radius
        segments = []

        if r == 0.0 or (line.x0 >= self.x0 + r and line.x0 <= self.x1 - r):
            if line.y0 < self.y0:
                segments.append([line.x0, line.y0, line.x1, self.y0])
            if line.y1 > self.y1:
                segments.append([line.x0, self.y1, line.x1, line.y1])
        elif line.y1 > self.y0 and line.y0 < self.y1:
            h = self._VLineTrim(line.x0, r) 
            if line.y0 < self.y0 + r:
                segments.append([line.x0, line.y0, line.x1, min(line.y1, self.y0 + h)])
            if line.y1 > self.y1 - r:
                segments.append([line.x0, max(self.y1 - h, line.y0), line.x1, line.y1])

        return False if len(segments) == 0 else segments

    def __repr__(self):
        return "(x0={x0}, y0={y0}, x1={x1}, y1={y1}, r={r})".format(x0=formatFloat(self.x0), y0=formatFloat(self.y0),
                                                             x1=formatFloat(self.x1), y1=formatFloat(self.y1),
                                                             r=formatFloat(self.radius))


class Keepout():

    DEBUG = 0
    _NUM_RECTS = 5

    def __init__(self, layer):
        self.layer = layer
        self.keepouts = []
        self.min_length = 0.01
        layer.keepout = self

    # float-variant of range()
    @staticmethod
    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump

    def __getattr__(self, name):
        if name == "offset":
            return self.layer.line_width / 2.0 + self.layer.getSoldermaskMargin()
        else:
            raise AttributeError

    def _align(self, value):
        return self.layer._align(value)

    def _add(self, x0, y0, x1, y1, radius=0.0):
        self.keepouts.append(_Keepout(self._align(x0), self._align(y0), self._align(x1), self._align(y1), radius))

    # add keepout area for rectangle
    def addRect(self, x, y, w, h, offset=None):
        if offset == None:
            offset = 0.0
        w = w / 2.0 + offset
        h = h / 2.0 + offset
        self._add(x - w, y - h, x + w, y + h)
        return self

    # add keepout area for circular or oval object
    def addRound(self, x, y, w, h, offset=None):
        if offset == None:
            offset = self.offset
#        d = w - h         
        r = min(h, w) / 2.0 + offset
        w = w / 2.0 + offset
        h = h / 2.0 + offset
        self._add(x - w, y - h, x + w, y + h, r)
#        self.addRect(x - w, y - w, d if d > 0.0 else 0.0, -d if d < 0.0 else 0.0, r)
        return self
    
    def addPads(self):
        nodes = self.layer.footprint.getNormalChilds()
        offset = self.offset
        for node in nodes:
            if isinstance(node, Pad):
                if node.shape == Pad.SHAPE_RECT:
                    self.addRect(node.at.x, node.at.y, node.size.x, node.size.y, offset)
                else:
                    self.addRound(node.at.x, node.at.y, node.size.x, node.size.y, offset)

    def getPadBB(self, number):
        # TODO: use node.calculateBoundingBox when implemented, this is a simple version that does not honor any rotation
        nodes = self.layer.footprint.getNormalChilds()
        offset = self.offset * 2.0
        bb = None
        for node in nodes:
            if isinstance(node, Pad) and node.number == number:
                bb = _RectWH(x = node.at.x, y = node.at.y, width = node.size.x + offset, height = node.size.y + offset)
        return bb

    # internal method for keepout-processing
    def _processHVLine(self, line):
        
        def add_segment(x0, y0, x1, y1):
            length = x1 - x0 + y1 - y0 
            if length >= self.min_length:
                segments.append([x0, y0, x1, y1])

        vertical = line.x0 == line.x1
        segments = [[line.x0, line.y0, line.x1, line.y1]]

        if self.DEBUG & 2:
            print("S", line)

        changes = len(self.keepouts) > 0
        while changes != False:
            changes = False
            for keepout in self.keepouts:
                if keepout.VlineIntersects(line.x0) if vertical else keepout.HlineIntersects(line.y0):
                    for i in reversed(range(0, len(segments))):
                        segment = segments[i]
                        changes = keepout.VLineTrim(segment) if vertical else keepout.HLineTrim(segment)
                        if changes != False:
                            segments.pop(i)
                            for segment in changes:
                                add_segment(segment[0], segment[1], segment[2], segment[3])
                            
                        if self.DEBUG & 2:
                            print("CHOP - line:", segment[0], segment[1], segment[2], segment[3], "keepout:", keepout)

            if changes != False:
                break

        if self.DEBUG & 2:
            print("LI", segments)

        return segments
    
    # split an arbitrary line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
    def processLine(self, x0, y0, x1, y1):

        line = _Line(x0, y0, x1, y1, normalize=True)

        if line.x0 == line.x1 or line.y0 == line.y1: # use simpler and faster algorithm for horizontal and vertical lines
            return self._processHVLine(line)
    
        # TODO: update to handle keepout area proper, now only respects the bounding box.
        
        segments=[[line.x0, line.y0, line.x1, line.y1]]
        for keepout in self.keepouts:
            for i in reversed(range(0, len(segments))):
                segment = segments[i]
                changes = keepout.lineIntersects(_Line(segment[0], segment[1], segment[2], segment[3]))
                if changes != False:
                    segments.pop(i)
                    segments.append([segment[0], segment[1], changes[0][0], changes[0][1]])
                    if len(changes) == 2:
                        segments.append([changes[1][0], changes[1][1], segment[2], segment[3]])
        return segments       

    # draws the keepouts
    def debug_draw(self):
        if self.DEBUG & 1:
            x = self.layer.x
            y = self.layer.y
            lw = self.layer.line_width
            self.layer.line_width = 0.01
            self.layer.keepout = None
            for keepout in self.keepouts:
                self.layer.goto(keepout.x0, keepout.y0)
                if(keepout.radius > 0.0):
                    self.layer.rrect(keepout.x1 - keepout.x0, keepout.y1 - keepout.y0, keepout.radius, origin="topLeft")
                self.layer.rect(keepout.x1 - keepout.x0, keepout.y1 - keepout.y0, origin="topLeft")
            self.layer.line_width = lw
            self.layer.keepout = self
            self.layer.x = x
            self.layer.y = y


class OutDir:

    def __init__(self, root_dir=None):    
        self.root_dir = "" if root_dir == None else root_dir
        if root_dir != "" and self.root_dir[-1] != os.sep:
            self.root_dir += os.sep

    def saveTo(self, lib_name):
        out_dir = "" if self.root_dir == "" else self.root_dir + lib_name + ".pretty" + os.sep   
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir

### EOF ###
