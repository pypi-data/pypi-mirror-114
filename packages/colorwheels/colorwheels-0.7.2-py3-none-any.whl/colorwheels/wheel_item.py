"""WheelItem: a dataclass containing one ColorWheel definition

The object contains the following values:

* name: ColorWheel name. The name is used to retrieve a named color sequence
* colors: List of ColorItem colors

WheelItem encapsulates a colorwheel selection and is used internally by
colorwheels.
"""

import math
from dataclasses import dataclass
from typing import List

from .color_item import ColorItem

@dataclass
class WheelItem:
    """Content of one colorwheel"""

    name: str
    colors: List[ColorItem]

    def generate_rainbow(self, size, amplitude, center, frequency):
        """Generate colors with a Rainbow palette. Overwrites colors list.

        Uses a simplified algorithm.

        Tip: If you don't wish to experiment with the algorithm, you can
        decide on the rainbow size (number of colors), and use these values
        as a starting point:

        amplitude=127, center=128, frequency=0.3
        """

        self.colors.clear()

        for i in range(size):
            red = math.sin(frequency*i + 0) * amplitude + center
            green = math.sin(frequency*i + 2) * amplitude + center
            blue = math.sin(frequency*i + 4) * amplitude + center
            self.colors.append(ColorItem(red=int(red), green=int(green), blue=int(blue)))

    def from_float_list(self, color_list):
        """Convert a list of float RGB tuples to native format

        This method comes in handy, if you use libraries like 'Colour' in your
        code.

        The Colour library uses RGB float values, encoded in tuples ranging
        from 0.0-1.0. We convert these values to an int tuple, i.e. int values
        ranging from 0-255
        """

        self.colors.clear()

        for color in color_list:
            new_color = ColorItem(0, 0, 0)
            new_color.from_float(color)
            self.colors.append(new_color)
