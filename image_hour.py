#!/usr/bin/env python
from PIL import Image, ImageFont, ImageDraw
from time import sleep, strftime, localtime
from random import randint, shuffle
import math

class ImageHour():

    def __init__(self, matrix, size, duration, typeclock = 'analog'):
        super(ImageHour, self).__init__()
        self.matrix = matrix
        self.size = size
        self.duration = duration
        self.typeclock = typeclock
        self.display_hour()

    def display_hour(self):
        for ind in range(0, self.duration):
            if self.typeclock == 'analog':
                self.matrix.SetImage(self.build_image_analog_hour(ind))
            else:
                self.matrix.SetImage(self.build_image_digital_hour(ind))
            sleep(1)

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

    def build_image_analog_hour(self, indice):
        """ Draw an analogue clock face."""
        
        now = localtime()
        
        img = Image.new('RGB', (self.size, self.size), 'black')
        draw = ImageDraw.Draw(img)

        colour_white = 192

        draw.ellipse((2,2,63,63), outline=colour_white)
        draw.ellipse((3,3,62,62), outline=colour_white)
        
        for i in range(0, 60): 
            # drawing background lines 
            if (i % 5) == 0: 
                #draw.drawLine(, 0,, 0)
                pass
        draw.line(self.clockhand(now.tm_hour * 30 + now.tm_min / 2, 20), fill=colour_white, width=4)
        draw.line(self.clockhand(now.tm_min * 6 + now.tm_sec / 10, 22), fill=colour_white, width=3)
        draw.line(self.clockhand(now.tm_sec * 6, 25), fill=colour_white, width=2)
        
        img.save('Legopanel.jpg')
        return img

    def clockhand(self, angle, length):
        """
        Calculate the end point for the given vector.
        Angle 0 is 12 o'clock, 90 is 3 o'clock.
        Based around (32,32) as origin, (0,0) in top left.
        """
        radian_angle = math.pi * angle / 180.0
        x = 32 + length * math.cos(radian_angle)
        y = 32 + length * math.sin(radian_angle)
        return [(32,32),(x,y)]