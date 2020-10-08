#!/usr/bin/env python
from time import sleep
from random import randint, shuffle
from image_hour import ImageHour

class ImageDraw():
    """Draw a panel canvas."""

    def __init__(self, matrix):
        super(ImageDraw, self).__init__()
        self.matrix = matrix
        self.image_draw()

    def image_draw(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        for x in range(0, self.matrix.width):
            offset_canvas.SetPixel(x, x, 255, 255, 255)
            offset_canvas.SetPixel(offset_canvas.height - 1 - x, x, 255, 0, 255)
            self.matrix.SwapOnVSync(offset_canvas)
        
        for x in range(0, offset_canvas.width):
            offset_canvas.SetPixel(x, 0, 255, 0, 0)
            offset_canvas.SetPixel(x, offset_canvas.height - 1, 255, 255, 0)
            self.matrix.SwapOnVSync(offset_canvas)
        
        for y in range(0, offset_canvas.height):
            offset_canvas.SetPixel(0, y, 0, 0, 255)
            offset_canvas.SetPixel(offset_canvas.width - 1, y, 0, 255, 0)
            self.matrix.SwapOnVSync(offset_canvas)
        
        for _ in range(0, 2000):
            r, g, b = ImageHour.random_color(self)
            offset_canvas.SetPixel(randint(0, self.matrix.width), randint(0, self.matrix.height), r, g, b)
            self.matrix.SwapOnVSync(offset_canvas)
        self.matrix.SwapOnVSync(offset_canvas)
