'''Module for the printer paper class.'''

from math import floor
from typing import Tuple
import logging
try:
    import PIL.Image as Image
except ImportError:
    logging.info("PIL not installed. PrinterPaper class will not have fill_image method.")
    PIL_SUPPORTED = False
else:
    PIL_SUPPORTED = True

class PrinterPaper:
    '''
    A class that represents a piece of paper that would have an image printed on it.

    :ivar width: Width of paper in inches.
    :vartype width: float
    :ivar height: Height of paper in inches.
    :vartype height: float
    :ivar dpi: DPI of printer.
    :vartype dpi: tuple(int, int)
    '''

    def __init__(self, width: float, height: float, dpi: Tuple[int, int]):

        self.width: float = width
        self.height: float = height
        self.dpi: Tuple[int, int] = dpi

    @property
    def pixel_width(self) -> float:
        '''Width of paper in pixels.'''

        return self.width * self.dpi[0]

    @property
    def pixel_height(self) -> float:
        '''Height of paper in pixels.'''

        return self.height * self.dpi[1]

    @property
    def width(self) -> float:
        '''Width of paper in inches.'''

        return self.__width

    @width.setter
    def width(self, value: float):
        '''Set width of paper in inches.

        :param value: New width
        :type value: float
        '''

        try:
            value = float(value)
        except:
            raise TypeError(f"width should be type float, not type {value.__class__.__name__}.")
        else:
            if value > 0:
                self.__width = value
            else:
                raise ValueError(f"width should be greater than zero, not {value}.")

    @property
    def height(self) -> float:
        '''Height of paper in inches.'''

        return self.__height

    @height.setter
    def height(self, value: float):
        '''Set height of paper in inches.

        :param value: New height.
        :type value: float
        '''

        try:
            value = float(value)
        except:
            raise TypeError(f"height should be type float, not type {value.__class__.__name__}.")
        else:
            if value > 0:
                self.__height = value
            else:
                raise ValueError(f"height should be greater than zero, not {value}.")

    @property
    def dpi(self) -> Tuple[int, int]:
        '''DPI of printer in form (width,height).'''

        return self.__dpi

    @dpi.setter
    def dpi(self, value: Tuple[int, int]):
        '''Set DPI of printer.

        :param value: New DPI
        :type value: tuple(int, int)
        '''

        if isinstance(value, tuple):
            if len(value) == 2:
                try:
                    x = int(value[0])
                    y = int(value[1])
                except:
                    raise TypeError(f"dpi should be a tuple of types (int, int),\
                         not tuple of types ({value[0].__class__.__name__},\
                             {value[1].__class__.__name__}).")
                else:
                    self.__dpi = (x, y)
            else:
                raise ValueError(f"Length of dpi should be 2, not {len(value)}.")
        else:
            raise TypeError(f"dpi should be type tuple, not type {value.__class__.__name__}.")

    # If the user has PIL installed, we should include a helper method for fitting an image onto
    # a PrinterPaper.


    if PIL_SUPPORTED:
        def fill_image(self, image: Image.Image) -> Image.Image:
            '''
            Scale an image to fill the PrinterPaper while keeping the image's aspect ratio.

            :param image: Image to fill
            :type image: Image
            :returns: Filled image
            :rtype: Image
            '''

            w, h = image.size
            if (w*self.pixel_width) >= (h*self.pixel_height):
                ratio = (self.pixel_width)/w
            else:
                ratio = (self.pixel_height)/h

            new_width = floor(w*ratio)
            new_height = floor(h*ratio)

            return image.resize((new_width, new_height))
