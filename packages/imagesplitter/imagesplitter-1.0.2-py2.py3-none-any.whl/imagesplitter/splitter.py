'''Module responsible for splitting images.'''
from math import ceil
from typing import List
from PIL import Image

def split_image(image: Image.Image, columns: int, rows: int, *, alpha: bool = False)\
     -> List[Image.Image]:
    '''
    Split an image into (cols * rows) images, with "cols" columns and "rows" rows.

    :param image: Input image
    :type image: Image
    :param columns: Number of columns to split into.
    :type columns: int
    :param rows: Number of rows to split into.
    :type rows: int
    :param alpha: Keyword Argument. Allow alpha in splits if true. Default false.

    :returns: List of images.
    :rtype: List[Image]

    :raises TypeError: If types do not match.
    :raises ValueError: If rows are less than 0 or greater than width of image, \
        or if columns are less than 0 or greater than height of image.
    '''

    if isinstance(image, Image.Image):
        pass
    else:
        raise TypeError(f"image should be type PIL.Image.Image, \
            not type {image.__class__.__name__}.")

    try:
        columns = int(columns)
    except:
        raise TypeError(f"cols should be type int, \
            not type {columns.__class__.__name__}.")

    try:
        rows = int(rows)
    except:
        raise TypeError(f"rows should be type int, \
            not type {rows.__class__.__name__}.")

    image_width, image_height = image.size

    if columns > image_width or columns < 1:
        raise ValueError(f"Invalid column value {columns}.\
             Value must be 1 <= n < {image_width} (Image Width).")
    if rows > image_height or rows < 1:
        raise ValueError(f"Invalid row value {rows}.\
             Value must be 1 <= n < {image_height} (Image Height).")
    images = []

    dx = ceil(image_width / columns)
    dy = ceil(image_height / rows)
    for y in range(0, image_height, dy):
        for x in range(0, image_width, dx):
            if alpha:
                base = Image.new('RGBA', (dx, dy), (0, 0, 0, 0))
            else:
                base = Image.new('RGB', (dx, dy), "WHITE")
            # If the border isn't perfect, paste it onto
            # a blank image so we retain the same size
            crop = image.crop(\
                (x, y, min(x+dx-1, image_width), min(y+dy-1, image_height)\
                    ))
            base.paste(crop, (0, 0))

            images.append(base)

    return images
