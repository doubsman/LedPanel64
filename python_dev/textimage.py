import time
import os
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def buil_hour(size = 64 ):
    img = Image.new('RGB', (size, size), 'black')
    draw = ImageDraw.Draw(img)
    for _ in range(0,100):
        draw.point((random.randint(0, size), random.randint(0, size)), random_color())
    font = ImageFont.truetype("calibri", 16)
    draw.text((0, 3),time.strftime("%x"), (255,99,71),font=font)
    draw.text((5,23),time.strftime("%H:%M:%S"), (255,99,71),font=font)
    draw.text((10,43),"BIDOU", (255,99,71),font=font)
    return img

while True:
    (buil_hour()).save('hour.jpg')
    os.system('imcat hour.jpg')
    time.sleep(1)


