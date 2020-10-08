#!/usr/bin/env python
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def splitcolImage(img, heigth, start, end, step):
    box = (start, 0, end, heigth)  
    im2 = img.crop(box)
    res = im2.copy()
    img = Image.new('RGBA', (step, step), 'black')
    img.paste(res)
    return img

def buildImage(img, step):
    listimages = []
    img = Image.open(img)
    [x,y] = img.size
    end = 0
    while x >= end:
        if end <= step:
            # first frame
            result = splitcolImage(img, y, x - end, x, step)
        else:
            # middle frames
            result = splitcolImage(img, y, x - end, x - end + step, step)
        listimages.append(result)
        end += 1
    # last frame
    for ind in range(0, step):
        result = splitcolImage(img, y, 0 - ind, end - ind, step)
        listimages.append(result)
    return listimages

def Imagescroller(img, step):
    listimages = buildImage(img, step)
    print(len(listimages))
    # save gif file result
    #listimages[0].save('Leagues_1792.gif', save_all=True, append_images=listimages[1:], optimize=False, duration=len(listimages)/50, loop=0)
    double_buffer = matrix.CreateFrameCanvas()
    for image in listimages:
        xpos = 0
        image.resize((matrix.width, matrix.height), Image.ANTIALIAS)
        img_width, img_height = image.size
        matrix.SetImage(image)
        double_buffer.SetImage(image, -xpos)
        double_buffer.SetImage(image, -xpos + img_width)
        #double_buffer = matrix.SwapOnVSync(double_buffer)
        time.sleep(0.01)


# Configuration matrix for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.pixel_mapper_config="U-mapper;Rotate:180"

matrix = RGBMatrix(options = options)

Imagescroller('Leagues_1792.png', 64)



