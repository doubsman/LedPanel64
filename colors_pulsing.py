#!/usr/bin/env python
from time import sleep


class ColorsPulsing():
    """Display all colors."""

    def __init__(self, matrix):
        super(ColorsPulsing, self).__init__()
        self.matrix = matrix
        self.colors_pulsing()

    def colors_pulsing(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        continuum = 0

        while continuum + 1 < 255 * 3:
            sleep((5 * 1000) / 1000000.0)
            continuum += 1
            continuum %= 3 * 255

            red = 0
            green = 0
            blue = 0

            if continuum <= 255:
                c = continuum
                blue = 255 - c
                red = c
            elif continuum > 255 and continuum <= 511:
                c = continuum - 256
                red = 255 - c
                green = c
            else:
                c = continuum - 512
                green = 255 - c
                blue = c

            self.offscreen_canvas.Fill(red, green, blue)
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
