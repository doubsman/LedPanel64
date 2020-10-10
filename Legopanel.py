from sys import argv, stdout
from os import system, listdir, path
from time import sleep
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from images_transition import ImageTransition
from images_display import ImagesDisplay
from image_scroller import ImageScroller
from image_hour import ImageHour
from image_draw import ImageDraw
from text_scroller import TextScroller
from colors_pulsing import ColorsPulsing

def mountcursor(step=10):
    for _ in range(0,step):
        stdout.write("\033[F") 

if len(argv) < 2:
    pathvid = r'./video'
    pathimg = r'./images'
else:
    pathimg = argv[1]
    pathvid = argv[2]

# Configuration matrix leds
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.pixel_mapper_config="U-mapper;Rotate:180"
#print(dir(options))
matrix = RGBMatrix(options = options)
size = matrix.width

version = 0.8
durimage = 10 
durtrans = 0.3
durangif = 0.1
durvideo = 0.05
mytext = "Vieillir c'est une obligation, grandir c'est un choix."
bigfont = "./fonts/texgyre-27.bdf"
imgintro = "./images/Qberq_64.png"
# debug: image viewer terminal part6
imgterm = True

# test list fonts
# from os import listdir, path
# def get_list_files(pathimg):
    # return [path.join(pathimg, f) for f in listdir(pathimg) if path.isfile(path.join(pathimg, f))]
# listfonts = get_list_files('./fonts')
# for myfont in listfonts:
    # TextScroller(matrix, 'testicule\r' + myfont, myfont)


print('LEGO DISPLAY PANEL version : {}'.format(version))

ImagePanel = ImagesDisplay(matrix, size, durimage, durangif)
ImagePanel.display_image(imgintro)


tim=60
while tim>0:
    print("""
    0 all
    1 intro
    2 drawing pixel panel
    3 display large image
    4 display hour
    5 display carroussel folder
    6 display scoll list images
    7 display large image Leagues_1792
    8 display video
    9 scroll text
    """)
    ans=input("What would you like to do? ")
    if ans=="1":
        #1 intro
        TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
    elif ans=="2":
        #2 drawing pixel panel
        ImageDraw(matrix)
    elif ans=="3":
        #3 display large image
        Imagebigforma2 = ImageScroller(matrix, size, r'./imagesbigwidth/qberk.png')
        Imagebigforma2.image_scroller()
    elif ans=="4":
        #4 display hour
        ImageHour(matrix, size, 60)
    elif ans=="5":
        #5 display carroussel folder
        ImageCarousel = ImageTransition(matrix, pathimg, size, durimage, durangif, durtrans)
        ImageCarousel.display_carousel()
    elif ans=="6":
        #6 display scoll list images
        ImagePanel.build_list(pathimg)
        ImagePanel.display_images()
        mountcursor()
    elif ans=="7":
        #7 display large image
        Imagebigforma1 = ImageScroller(matrix, size, r'./imagesbigwidth/Leagues_1792.png')
        Imagebigforma1.image_scroller()
    elif ans=="8":
        #8 display video
        VideosGif = ImageTransition(matrix, pathvid, size, durimage, durvideo, durtrans, 1, 0)
        VideosGif.display_carousel()
    elif ans=="9":
        #9 scroll text
        TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
    tim -=1


TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
# build out while, no read sdcard for the demo
ImageCarousel = ImageTransition(matrix, pathimg, size, durimage, durangif, durtrans)
VideosGif = ImageTransition(matrix, pathvid, size, durimage, durvideo, durtrans, 1, 0)
Imagebigforma1 = ImageScroller(matrix, size, r'./imagesbigwidth/Leagues_1792.png')
Imagebigforma2 = ImageScroller(matrix, size, r'./imagesbigwidth/qberk.png')
print('start demo... : Press CTRL-C to stop.')
while True:
    #2 drawing pixel panel
    ImageDraw(matrix)
    #3 display large image
    Imagebigforma2.image_scroller()
    #4 display hour
    ImageHour(matrix, size, 60)
    #5 display carroussel folder
    ImageCarousel.display_carousel()
    #6 display scoll list images
    indice = 0
    for img in ImageCarousel.listimages:
        if ImageCarousel.tempo[indice] == durimage:
            ImageScroller(matrix, size, img).image_scroller()
            if imgterm:
                img.save('/tmp/Legopanel.jpg')
                system('./tools/imcat /tmp/Legopanel.jpg')
        indice += 1
    #7 display large image
    Imagebigforma1.image_scroller()
    #8 display video
    VideosGif.display_carousel()
    #9 scroll text
    TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
    #1 intro
    TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
