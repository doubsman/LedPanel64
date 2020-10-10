#!/usr/bin/env python

from rgbmatrix import graphics
from time import sleep
from image_hour import ImageHour


class TextScroller():
    """Display a runtext with double-buffering."""

    def __init__(self, matrix, mytext, myfont, mycolor=(255, 255, 0), positiony = 10, modecolors = False):
        super(TextScroller, self).__init__()
        self.matrix = matrix
        self.mytext = mytext
        self.myfont = myfont
        self.mycolor =  mycolor
        self.positiony = positiony
        self.modecolors = modecolors
        self.text_scroller()

    def text_scroller(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.myfont)
        textColor = graphics.Color(self.mycolor[0],self.mycolor[1],self.mycolor[2])
        pos = offscreen_canvas.width
        while True:
            offscreen_canvas.Clear()
            if self.modecolors:
                self.mycolor = ImageHour.random_color(self)
                textColor = graphics.Color(self.mycolor[0],self.mycolor[1],self.mycolor[2])
            len = graphics.DrawText(offscreen_canvas, font, pos, self.positiony, textColor, self.mytext)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            if pos == 64:
                break
