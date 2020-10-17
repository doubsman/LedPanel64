#!/usr/bin/env python
from PIL import Image, ImageFont, ImageDraw
from random import randint
from image_hour import ImageHour
# list fonts ttf
# fc-list -f '%{file}\n' :lang=fr


class ImageDrawing():
    """Draw a panel canvas."""

    def __init__(self, matrix):
        super(ImageDrawing, self).__init__()
        self.matrix = matrix
        self.size = self.matrix.width

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

    def image_draw_text_reggae(self, mytext, textfont = "DejaVuSerif", textsize = 42):
        img = Image.new('RGB', (self.size, self.size), 'black')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(textfont, textsize)
        draw.text((4, 9),mytext,  (0,128,0), font=font)
        draw.text((6, 11),mytext, (255,255,0), font=font)
        draw.text((8, 13),mytext, (255,0,0), font=font)
        self.matrix.SetImage(img)

    def image_draw_text_test(self, mytext, textcolorfont = (51, 102, 204), textfont = "DejaVuSerif", textsize = 42):
        img = Image.new('RGB', (self.size, self.size), 'black')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(textfont, textsize)
        draw.text((6, 11),mytext, textcolorfont, font=font)
        tfont = ImageFont.truetype(textfont, textsize - 1)
        draw.text((7, 12),mytext, (255, 255, 0), font=tfont)
        self.matrix.SetImage(img)