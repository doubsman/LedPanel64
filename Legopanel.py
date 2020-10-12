from sys import argv, stdin
from time import sleep
from yaml import full_load
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import select
from images_transitions import ImagesTransitions
from images_display import ImagesDisplay
from image_scroller import ImageScroller
from image_hour import ImageHour
from image_draw import ImageDrawing
from text_scroller import TextScroller
from colors_pulsing import ColorsPulsing


def keyinput(step, keydefault):
    i, _, _ = select.select( [stdin], [], [], step)
    if (i):
       k = stdin.readline().strip()
       return(k)
    else:
       # all demo
       return(keydefault)

if len(argv) < 2:
    pathvid = r'./video'
    pathimg = r'./images'
else:
    pathimg = argv[1]
    pathvid = argv[2]

with open(r'./config.yaml') as file:
    configyaml = full_load(file)

# Configuration matrix leds
options = RGBMatrixOptions()
options.rows = configyaml['Matrix']['rows']
options.cols = configyaml['Matrix']['cols']
options.chain_length = configyaml['Matrix']['chain_length']
options.hardware_mapping = configyaml['Matrix']['hardware_mapping']
options.pixel_mapper_config = configyaml['Matrix']['pixel_mapper_config']

matrix = RGBMatrix(options = options)
size = matrix.width

version = configyaml['version']
durimage = configyaml['Duration']['image']
durtrans = configyaml['Duration']['transition']
durangif = configyaml['Duration']['gif']
durvideo = configyaml['Duration']['video']
mytext = configyaml['Options']['text']
bigfont =  configyaml['Options']['bigfont']
imgintro = configyaml['Options']['image_intro']

print('LEGO DISPLAY PANEL version : {}'.format(version))
ImagePanel = ImagesDisplay(matrix, size, durimage, durangif)
ImageDrawPanel = ImageDrawing(matrix, size)

tim=5
while tim >= 0:
    ImageDrawPanel.image_draw_text_reggae(('0'+str(tim)[-2:]))
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

    What would you like to do? : """, end='', flush=True)
    ans=keyinput(20, "8")
    print('')
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
