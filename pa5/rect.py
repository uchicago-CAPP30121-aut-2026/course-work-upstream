"""
CAPP 30121, Autumn 2026: Class for representing rectangles.
"""

import math

from drawing import ChiCanvas, ColorKey

X_SCALE_FACTOR = 12
Y_SCALE_FACTOR = 10

MIN_RECT_SIDE_FOR_TEXT = 0.03


class Rectangle:
    """
    Simple class for representing rectangles.

    Public attributes:
        origin: (Tuple[float, float]) x and y coordinates of the
          rectangle's origin
        size: (Tuple[float, float]) the width and height of the
          rectangle.
        label (str): text label for the rectangle
        color_code (str): a code used to choose the color
          of the rectangle
    """

    @staticmethod
    def __validate_tuple_param(pair, name):
        """
        Validate a tuple parameter.  This method is used by the constructor
        and should not be used in student code.
        """
        assert isinstance(pair, (list, tuple)) and len(pair) == 2, (
            name + " parameter to Rectangle must be a tuple or list of two floats"
        )

        x, y = pair

        assert isinstance(x, float) and isinstance(y, float), (
            name + " parameter to Rectangle must be a tuple or list of two floats"
        )

        assert x >= 0.0 and y >= 0.0, (
            "Incorrect value for rectangle {}: ({}, {}) ".format(name, x, y)
            + "(both values must be >= 0)"
        )

    def __init__(self, origin, size, label="", color_code=""):
        """
        Constructs a new Rectangle.

        Args:
            origin: (Tuple[float, float]) x and y coordinates of the
                rectangle's origin
            size: (Tuple[float, float]) the width and height of the
              rectangle.
            label (str): a label for the rectangle
            color_code (str): a code used to choose the color
              of the rectangle
        """
        # Validate parameters
        Rectangle.__validate_tuple_param(origin, "origin")
        Rectangle.__validate_tuple_param(size, "size")
        assert label is not None, "Rectangle label can't be None"
        assert isinstance(label, str), "Rectangle label must be a string"
        assert isinstance(color_code, str), "Rectangle color_code must be a string"

        self.origin = origin
        self.size = size
        self.label = label
        self.color_code = color_code

    def draw(self, canvas, color_key):
        """
        Draw a rectangle on a canvas

        Args:
            canvas (ChiCanvas): a canvas to draw on
            color_key (ColorKey): a color key object
        """
        fill_color = color_key.get_color(self.color_code)
        x, y = self.origin
        width, height = self.size
        canvas.draw_rectangle(
            x, y, x + width, y + height, fill=fill_color, outline="black"
        )

        if (width > MIN_RECT_SIDE_FOR_TEXT) and (height > MIN_RECT_SIDE_FOR_TEXT):
            if width >= height:
                canvas.draw_text(x + width / 2.0, y + height / 2.0, width, self.label)
            else:
                canvas.draw_text_vertical(
                    x + width / 2.0, y + height / 2.0, width, self.label
                )

    def __str__(self):
        """Construct a client-facing string for the rectangle"""
        x, y = self.origin
        width, height = self.size
        return (
            f"RECTANGLE origin: ({x:.4f}, {y:.4f})\n"
            f"          width & height: ({width:.4f}, {height:.4f})\n"
            f"          label: {repr(self.label)}\n"
            f"          color code: {repr(self.color_code)}"
        )

    def __repr__(self):
        """Construct a developer-facing string for the rectangle"""
        x, y = self.origin
        width, height = self.size
        return (
            f"Rectangle(({x}, {y}), ({width}, {height}), "
            f"{repr(self.label)}, {repr(self.color_code)})"
        )

        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False

        """Are the two rectangles equal?"""
        my_x, my_y = self.origin
        other_x, other_y = other.origin
        my_w, my_h = self.size
        other_w, other_h = other.size

        return (
            math.isclose(my_x, other_x)
            and math.isclose(my_y, other_y)
            and math.isclose(my_w, other_w)
            and math.isclose(my_h, other_h)
            and (self.label == other.label)
            and (self.color_code == other.color_code)
        )
