from math import floor

class PrinterPaper:
    '''
    A class that represents a piece of paper that would have an image printed on it.

    Attributes:
        width (float): Width of paper in inches.
        height (float): Height of paper in inches.
        dpi (tuple): DPI of printer in form (width, height).
    '''

    def __init__(self,width: float, height: float, dpi: tuple):
        """
        PrinterPaper constructor.

        Arguments:
            width (float): Width of paper in inches.
            height (float): Height of paper in inches.
            dpi (tuple): DPI of printer in form (x,y).
        """

        self.width = width
        self.height = height
        self.dpi = dpi

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
    def width(self,value:float):
        '''Set width of paper in inches.
        
        Arguments:
            value (float): New width in inches.
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
    def height(self,value:float):
        '''Set height of paper in inches.

        Arguments:
            value (float): New height in inches.
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
    def dpi(self) -> tuple:
        '''DPI of printer in form (width,height).'''

        return self.__dpi

    @dpi.setter
    def dpi(self,value:tuple):
        '''Set DPI of printer.

        Arguments:
            value (tuple): New DPI in form (width,height).
        '''

        if isinstance(value,tuple):
            if len(value) == 2:
                try:
                    x = float(value[0])
                    y = float(value[1])
                except:
                    raise TypeError(f"dpi should be a tuple of types (float,float), not tuple of types ({value[0].__class__.__name__},{value[1].__class__.__name__}).")
                else:
                    self.__dpi = (x,y)
            else:
                raise ValueError(f"Length of dpi should be 2, not {len(value)}.")
        else:
            raise TypeError(f"dpi should be type tuple, not type {value.__class__.__name__}.")

    # If the user has PIL installed, we should include a helper method for fitting an image onto
    # a PrinterPaper.

    try:
        import PIL.Image as Image
    except:
        pass
    else:

        def fill_image(self,image: Image.Image) -> Image.Image:
            '''
            Scale an image to fill the PrinterPaper while keeping the image's aspect ratio.

            Arguments:
                image (PIL.Image.Image): The image to scale.

            Returns:
                new_image (PIL.Image.Image): The image scaled.
            '''

            w,h = image.size
            if (w*self.pixel_width) >= (h*self.pixel_height):
                ratio = (self.pixel_width)/w
            else:
                ratio = (self.pixel_height)/h

            nw = floor(w*ratio)
            nh = floor(h*ratio)

            return image.resize((nw,nh))