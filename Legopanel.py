from sys import argv, stdout
from time import sleep
from keyboard import is_pressed
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from images_transitions import ImagesTransitions
from images_display import ImagesDisplay
from image_scroller import ImageScroller
from image_hour import ImageHour
from image_draw import ImageDrawing
from text_scroller import TextScroller
from colors_pulsing import ColorsPulsing

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

matrix = RGBMatrix(options = options)
size = matrix.width

version = 0.81
durimage = 10 
durtrans = 0.3
durangif = 0.1
durvideo = 0.05
mytext = "Vieillir c'est une obligation, grandir c'est un choix."
bigfont = "./fonts/texgyre-27.bdf"
imgintro = "./images/Qberq_64.png"

print('LEGO DISPLAY PANEL version : {}'.format(version))
ImagePanel = ImagesDisplay(matrix, size, durimage, durangif)
ImageDrawPanel = ImageDrawing(matrix, size)

tim=9
while tim > 0:
    ImageDrawPanel.image_draw_text(('0'+str(tim)[-2:]))
    tim -=1
    sleep(1)    
ImagePanel.display_image(imgintro)

while True:
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
    a colors pulsing
    """)
    ans=input("What would you like to do? ")
    if ans=="1":
        #1 intro
        TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
    elif ans=="2":
        #2 demo drawing pixel panel
        ImageDrawPanel.image_draw_demo()
    elif ans=="3":
        #3 display large image
        Imagebigforma2 = ImageScroller(matrix, size, r'./imagesbigwidth/qberk.png')
        Imagebigforma2.image_scroller()
    elif ans=="4":
        #4 display hour
        ImageHour(matrix, size, 60)
    elif ans=="5":
        #5 display carroussel folder
        ImageCarousel = ImagesTransitions(matrix, pathimg, size, durimage, durangif, durtrans)
        ImageCarousel.display_imagesTransitions()
    elif ans=="6":
        #6 display scoll list images
        ImagePanel.preload_list(pathimg)
        ImagePanel.display_images()
    elif ans=="7":
        #7 display large image
        Imagebigforma1 = ImageScroller(matrix, size, r'./imagesbigwidth/Leagues_1792.png')
        Imagebigforma1.image_scroller()
    elif ans=="8":
        #8 display video
        VideosGif = ImagesTransitions(matrix, pathvid, size, durimage, durvideo, durtrans, 1, 0)
        VideosGif.display_imagesTransitions()
    elif ans=="9":
        #9 scroll text
        TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
    elif ans=="a":
        #a colors demo
        ColorsPulsing(matrix)
    elif ans=="0":
        TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
        # build out while, no read sdcard for the demo
        ImageCarousel = ImagesTransitions(matrix, pathimg, size, durimage, durangif, durtrans)
        ImagePanel.preload_list(pathimg)
        VideosGif = ImagesTransitions(matrix, pathvid, size, durimage, durvideo, durtrans, 1, 0)
        Imagebigforma1 = ImageScroller(matrix, size, r'./imagesbigwidth/Leagues_1792.png')
        Imagebigforma2 = ImageScroller(matrix, size, r'./imagesbigwidth/qberk.png')
        print('start demo... : Press CTRL-C to stop.')
        while True:
            #2 drawing pixel panel
            ImageDrawPanel.image_draw_demo()
            #3 display large image
            Imagebigforma2.image_scroller()
            #4 display hour
            ImageHour(matrix, size, 60)
            #5 display carroussel folder
            ImageCarousel.display_imagesTransitions()
            #6 display scoll list images
            ImagePanel.display_images()
            #7 display large image
            Imagebigforma1.image_scroller()
            #8 display video
            VideosGif.display_imagesTransitions()
            #9 scroll text
            TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
            #1 intro
            TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
            #a colors demo
            ColorsPulsing(matrix)
