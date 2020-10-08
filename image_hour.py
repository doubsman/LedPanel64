#!/usr/bin/env python
from PIL import Image, ImageFont, ImageDraw
from time import sleep, strftime
from random import randint, shuffle


class ImageHour():

    def __init__(self, matrix, size, duration):
        super(ImageHour, self).__init__()
        self.matrix = matrix
        self.size = size
        self.duration = duration
        self.display_hour()

    def display_hour(self):
        for ind in range(0, self.duration):
            self.matrix.SetImage(self.build_image_hour(ind))
            sleep(1)

    def build_image_hour(self, counter, stars = 100):
        img = Image.new('RGB', (self.size, self.size), 'black')
        draw = ImageDraw.Draw(img)
        for _ in range(0, stars):
            draw.point((randint(0, self.size), randint(0, self.size)), self.random_color())
        font = ImageFont.truetype("DejaVuSerif", 14)
        draw.text((0, 3),strftime("%x"), (255,99,71), font=font)
        draw.text((0, 23),strftime("%H:%M:%S"), (255,99,71), font=font)
        draw.text((6 + counter % 2, 43),"BIDOU", (255,99,71), font=font)
        return img

    def random_color(self):
        rgbl=[255,0,0]
        shuffle(rgbl)
        return tuple(rgbl)


