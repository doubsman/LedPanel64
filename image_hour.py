#!/usr/bin/env python
from PIL import Image, ImageFont, ImageDraw
from time import sleep, strftime, localtime
from random import randint, shuffle
import math

class ImageHour():

    def __init__(self, matrix, duration, typeclock = 'analog'):
        super(ImageHour, self).__init__()
        self.matrix = matrix
        self.size = self.matrix.width
        self.duration = duration
        self.typeclock = typeclock
        self.display_hour()

    def display_hour(self):
        for ind in range(0, self.duration):
            if self.typeclock == 'analog':
                self.matrix.SetImage(self.build_image_analog_hour(ind))
            else:
                self.matrix.SetImage(self.build_image_digital_hour(ind))
            sleep(0.15)

    def build_image_digital_hour(self, counter, stars = 100):
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

    def build_image_analog_hour(self, indice=1):
        """ Draw an analogue clock face."""
        now = localtime()
        img = Image.open('clock64.png').convert('RGB')
        draw = ImageDraw.Draw(img)
        #draw.ellipse((1, 1, self.size - 2, self.size - 2), fill="white")
        draw.line(self.clockhand(now.tm_hour * 30 + now.tm_min / 2, 15), fill="red", width=5)
        draw.line(self.clockhand(now.tm_min * 6 + now.tm_sec / 10, 20), fill="blue", width=3)
        draw.line(self.clockhand(now.tm_sec * 6, 25), fill="yellow", width=1)
        return img.resize((self.size, self.size),Image.ANTIALIAS)

    def clockhand(self, angle, length):
        """
        Calculate the end point for the given vector.
        Angle 0 is 12 o'clock, 90 is 3 o'clock.
        Based around (32,32) as origin, (0,0) in top left.
        """
        center = ((self.size) / 2)
        radian_angle = math.pi * (angle - 90) / 180.0
        x = center + length * math.cos(radian_angle)
        y = center + length * math.sin(radian_angle)
        return [(center,center),(x,y)]

#ImageHour('',64,4).build_image_analog_hour()