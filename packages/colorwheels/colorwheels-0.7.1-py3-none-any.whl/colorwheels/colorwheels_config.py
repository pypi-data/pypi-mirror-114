"""ColorwheelsConfig is a configuration helper for :doc:`colorwheels`, implemented
as a singleton.

The helper loads a configuration YAML file and serves the colors by name to
a Colorwheels generator."""

import logging

import yaml

from .config import LOG_LEVEL, LOG_FORMAT
from .singleton import Singleton
from .color_item import ColorItem
from .wheel_item import WheelItem

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

class ColorwheelsConfig(metaclass=Singleton):
    """ helper"""

    def __init__(self):
        """ Initialize configuration helper for :doc:`colorwheels`.

        The constructor creates the most simple configuration, and we expect
        a configuration file to be loaded later by code.

        The initial wheels available are primitives: 'red', 'green', 'blue'"""

        self._wheel_items = list() # list of WheelItem objects

        self.release = "unknown"

        self._wheel_items.append(
            WheelItem("default", [
                ColorItem(255, 0, 0),
                ColorItem(0, 255, 0),
                ColorItem(0, 0, 255)]))

# -- Configuration Handling --------------------------------------------------

    @property
    def first_wheel(self):
        """Get the first wheel available"""

        # should be always available.... no need to raise
        return self._wheel_items[0]

    def find_wheel(self, name):
        """Find wheelitem by name. None if not found"""

        items = [item for item in self._wheel_items if item.name == name]
        return items[0] if items else None

    def wheel_names(self):
        """Return list of wheel names available in configuration"""

        names = list()
        for wheel in self._wheel_items:
            names.append(wheel.name)
        return names

    def add_wheel_item(self, item):
        """Adds a :doc:`wheel_item` to definitions list.

        Raises
        ------
        ValueError
            Raises error if item name already exists
        """

        if not isinstance(item, WheelItem):
            raise ValueError("cannot add object. Not of type WheelItem")

        if self.find_wheel(item.name) is None:
            self._wheel_items.append(item)
        else:
            raise ValueError("Item '%s' cannot be added. Already exists" % item.name)

    def create_wheel_item(self, name, colors):
        """Create a :doc:`wheel_item` from parts. Function returns the created item"""

        new_item = WheelItem(name=name, colors=colors)
        return new_item

# -- Loading Configuration ---------------------------------------------------

    def _check_release(self):
        """Validate the version of the configuration file."""

        # First version doesn't need any validation. Reserved for future
        logger.info("Color definition file is at version '%s'", self.release)

    def _create_wheel_items(self, yaml_data):
        """Convert yaml data to wheel items"""

        self._wheel_items.clear()

        # handle metadata
        self.release = yaml_data["meta"]["release"]
        self._check_release()

        # handle wheel elements
        for wheel_def in yaml_data["wheels"]:

            color_list = list()

            name = wheel_def["wheel"]["name"]
            element_type = wheel_def["wheel"]["type"] \
                if "type" in wheel_def["wheel"] else "sequence"

            if element_type == "sequence":
                for color_def in wheel_def["wheel"]["colors"]:
                    col = ColorItem(color_def["rgb"][0], color_def["rgb"][1], color_def["rgb"][2])
                    color_list.append(col)

                new_def = WheelItem(name, color_list)
                self.add_wheel_item(new_def)

            elif element_type == "rainbow":
                new_def = WheelItem(name, color_list)
                # Read rainbow parameters and use sensible defaults if not available
                rainb_size = wheel_def["wheel"]["size"] \
                    if "size" in wheel_def["wheel"] else 32
                rainb_amplitude = wheel_def["wheel"]["amplitude"] \
                    if "amplitude" in wheel_def["wheel"] else 127
                rainb_center = wheel_def["wheel"]["center"] \
                    if "center" in wheel_def["wheel"] else 128
                rainb_frequency = wheel_def["wheel"]["frequency"] \
                    if "frequency" in wheel_def["wheel"] else 0.3
                new_def.generate_rainbow(rainb_size, rainb_amplitude, rainb_center, rainb_frequency)

                self.add_wheel_item(new_def)
            else:
                raise ValueError(f"Unknown wheel type {element_type}")

    def load_wheels(self, filename):
        """loads YAML color definition file. The loaded file is converted to a list of
        :doc:`wheel_item` objects.

        Raises ``FileNotFoundError``, or ``YAMLError`` if loading fails.

        When loading a new definition from YAML, make sure colorwheels activates whatever wheel
        is required!"""

        try:
            with open(filename, 'r') as stream:
                try:
                    yml = yaml.safe_load(stream)
                    self._create_wheel_items(yml)
                except yaml.YAMLError as exc:
                    logger.fatal("Loading configuration file '%s' failed: %s", filename, exc)
                    raise exc

        except FileNotFoundError as exc:
            logger.fatal("File '%s' not found ...", filename)
            raise exc
