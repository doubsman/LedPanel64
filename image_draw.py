#!/usr/bin/env python
from PIL import Image, ImageFont, ImageDraw
from time import sleep
from random import randint, shuffle
from image_hour import ImageHour

class ImageDrawing():
    """Draw a panel canvas."""

    def __init__(self, matrix, size):
        super(ImageDrawing, self).__init__()
        self.matrix = matrix
        self.size = size

    def image_draw_demo(self):
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

    def image_draw_text(self, mytext, textcolor = (255,99,71), textfont = "DejaVuSerif", textsize = 26):
        img = Image.new('RGB', (self.size, self.size), 'black')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(textfont, textsize)
        draw.text((0, 10),mytext, textcolor, font=font)