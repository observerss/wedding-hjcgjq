#!/usr/bin/env python
# -*- coding: utf-8
from PIL import Image, ImageChops
from StringIO import StringIO
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import ImageFormatter

def trim(im, padding=5):
    """
    trim image, leave padding width
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    obbox = im.getbbox()
    x0,y0 = max(bbox[0]-padding, obbox[0]), max(bbox[1]-padding, obbox[1])
    x1,y1 = min(bbox[2]+padding, obbox[2]), min(bbox[3]+padding, obbox[3])
    return im.crop((x0,y0,x1,y1))

def number2image(number):
    return trim(Image.open(StringIO(highlight(
                                        unicode(number), HtmlLexer(), 
                                        ImageFormatter(
                                            image_format="png",
                                            style='default',
                                            font_name='Arial',
                                            font_size=18,
                                            line_numbers=False)))))


def _test_number2image():
    number2image('13611825698').show()

# _test_number2image()
