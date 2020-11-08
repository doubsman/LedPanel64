from sys import argv, stdin
from time import sleep
from yaml import full_load
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import select
from images_transitions import ImagesTransitions
from images_display import ImagesDisplay
from images_concat import ImagesConcat
from image_scroller import ImageScroller
from image_hour import ImageHour
from image_draw import ImageDrawing
from text_scroller import TextScroller
from colors_pulsing import ColorsPulsing
from starboard import playstarboard

def keyinput(step, keydefault):
    i, _, _ = select.select( [stdin], [], [], step)
    if (i):
       k = stdin.readline().strip()
       return(k)
    else:
       # all demo
       return(keydefault)

with open(r'./config.yaml') as file:
    configyaml = full_load(file)


if len(argv) < 2:
    pathvid = configyaml['Demo']['path_video']
    pathimg = configyaml['Demo']['path_images']
else:
    pathimg = argv[1]
    pathvid = argv[2]

# Configuration matrix leds
options = RGBMatrixOptions()
options.rows = configyaml['Matrix']['rows']
options.cols = configyaml['Matrix']['cols']
options.chain_length = configyaml['Matrix']['chain_length']
options.hardware_mapping = configyaml['Matrix']['hardware_mapping']
options.pixel_mapper_config = configyaml['Matrix']['pixel_mapper_config']
options.brightness = configyaml['Matrix']['brightness']
#options.disable_hardware_pulsing = 0
# raspberry0
#options.gpio_slowdown = 0
#options.pwm_dither_bits 
options.pwm_lsb_nanoseconds = 100
#options.show_refresh_rate = 1
print(dir(options))
matrix = RGBMatrix(options = options)

version = configyaml['version']
durimage = configyaml['Duration']['image']
durtrans = configyaml['Duration']['transition']
durangif = configyaml['Duration']['gif']
durvideo = configyaml['Duration']['video']
mytext = configyaml['Demo']['text']
bigfont =  configyaml['Demo']['bigfont']
imgintro = configyaml['Demo']['image_intro']

print('LEGO DISPLAY PANEL version : {}'.format(version))
ImagePanel = ImagesDisplay(matrix, durimage, durangif)
ImageDrawPanel = ImageDrawing(matrix)

tim=5
while tim >= 0:
    img = ImageDrawPanel.image_draw_text_reggae(("{:02d}".format(tim)))
    tim -=1
    sleep(1)
ImagePanel.display_psyrotateimage(img)
ImagePanel.display_psyrotateimage(imgintro, 0)
ImagePanel.display_rotateimage(imgintro)
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
    b star board
    c images banner
    d babe banner

    What would you like to do? : """, end='', flush=True)
    ans=keyinput(20, "0")
    #print('')
    ImagePanel.display_psyrotateimage(imgintro)
    ImagePanel.display_image('./wait.png')
    if ans=="1":
        print("#1 intro")
        TextScroller(matrix, 'LEGO DISPLAY PANEL version : {}'.format(version), bigfont, (0,255,0), 40, True)
    elif ans=="2":
        print("#2 demo drawing pixel panel")
        ImageDrawPanel.image_draw_demo()
    elif ans=="3":
        print("#3 display large image")
        Imagebigforma2 = ImageScroller(matrix, r'./imagesbigwidth/qberk.png')
        Imagebigforma2.image_scroller()
    elif ans=="4":
        print("#4 display hour")
        ImageHour(matrix, 60)
        ImageHour(matrix, 60, 'digital')
    elif ans=="5":
        print("#5 display carroussel folder")
        ImageCarousel = ImagesTransitions(matrix, pathimg, durimage, durangif, durtrans)
        ImageCarousel.display_imagesTransitions()
    elif ans=="6":
        print("#6 display scoll list images")
        ImagePanel.preload_pathimgs(pathimg)
        ImagePanel.display_images()
    elif ans=="7":
        print("#7 display large image")
        Imagebigforma1 = ImageScroller(matrix, r'./imagesbigwidth/Leagues_1792.png')
        Imagebigforma1.image_scroller()
    elif ans=="8":
        print("#8 display video")
        VideosGif = ImagesTransitions(matrix, pathvid, durimage, durvideo, durtrans, 1, 0)
        VideosGif.display_imagesTransitions()
    elif ans=="9":
        print("#9 scroll text")
        TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
    elif ans=="a":
        print("#a colors demo")
        ColorsPulsing(matrix)
    elif ans=="b":
        print("#b star board")
        playstarboard(matrix, 120, 1000, 0)
    elif ans=="c":
        print("#c images banner")
        Banner = ImagesConcat(matrix, pathimg)
        Banner.display_concatimages()
    elif ans=="d":
        print("#d babe banner")
        Banner = ImagesConcat(matrix, r'./babe')
        Banner.display_concatimages()
    elif ans=="0":
        # build out while, no read sdcard for the demo
        ImageCarousel = ImagesTransitions(matrix, pathimg, durimage, durangif, durtrans)
        ImagePanel.preload_pathimgs(pathimg)
        VideosGif = ImagesTransitions(matrix, pathvid, durimage, durvideo, durtrans, 1, 0)
        Imagebigforma1 = ImageScroller(matrix, r'./imagesbigwidth/Leagues_1792.png')
        Imagebigforma2 = ImageScroller(matrix, r'./imagesbigwidth/qberk.png')
        Banner = ImagesConcat(matrix, pathimg)
        print('start demo... : Press CTRL-C to stop.')
        while True:
            #1 intro
            TextScroller(matrix, 'LEGO DISPLAY PANEL 64x64 version : {}'.format(version), bigfont, (0,255,0), 40, False)
            #2 drawing pixel panel
            ImageDrawPanel.image_draw_demo()
            #3 display large image
            Imagebigforma2.image_scroller()
            #4 display hour
            ImageHour(matrix, 60)
            #5 display carroussel folder
            ImageCarousel.display_imagesTransitions()
            #7 display large image
            Imagebigforma1.image_scroller()
            #8 display video
            VideosGif.display_imagesTransitions()
            #4 display hour
            ImageHour(matrix, 60, 'digital')
            #9 scroll text
            TextScroller(matrix, mytext, bigfont, (128,0,128), 40)
            #a colors demo
            ColorsPulsing(matrix)
            #6 display scoll list images
            ImagePanel.display_images()
            #b star board
            playstarboard(matrix, 120, 1000, 0)
            #c banner images
            Banner.display_concatimages()