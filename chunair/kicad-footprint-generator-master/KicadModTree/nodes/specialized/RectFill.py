# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from KicadModTree.Vector import *
from KicadModTree.nodes.Node import Node
from KicadModTree.nodes.base import Line


class RectFill(Node):
    r"""Add the filling of a Rect to the render tree

    Normally, this class isn't needed, because ``FilledRect`` combines ``RectLine`` with ``RectFill``

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Vector2D``) --
          start edge of the rect fill
        * *end* (``Vector2D``) --
          end edge of the rect fill
        * *layer* (``str``) --
          layer on which the rect fill is drawn (default: 'F.SilkS')
        * *width* (``float``) --
          width of the filling lines (default: 0.12)

    :Example:

    >>> from KicadModTree import *
    >>> RectFill(start=[-3, -2], end=[3, 2], layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.start_pos = Vector2D(kwargs['start'])
        self.end_pos = Vector2D(kwargs['end'])

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width', 0.12)  # TODO: auto detection

        self.virtual_childs = self._createChildNodes(self.start_pos, self.end_pos, self.layer, self.width)

    def _createChildNodes(self, start_pos, end_pos, layer, width):
        nodes = []

        cur_y_pos = min([start_pos.y, end_pos.y])
        max_y_pos = max([start_pos.y, end_pos.y])

        while (cur_y_pos + width) < max_y_pos:
            cur_y_pos += width
            new_node = Line(start=Vector2D(start_pos.x, cur_y_pos),
                            end=Vector2D(end_pos.x, cur_y_pos),
                            layer=layer,
                            width=width)
            new_node._parent = self
            nodes.append(new_node)

        return nodes

    def getVirtualChilds(self):
        return self.virtual_childs

    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)

        render_string = ['start: [x: {sx}, y: {sy}]'.format(sx=self.start_pos.x, sy=self.start_pos.y),
                         'end: [x: {ex}, y: {ey}]'.format(ex=self.end_pos.x, ey=self.end_pos.y)]

        render_text += " [{}]".format(", ".join(render_string))

        return render_text
