from os import listdir, path
from imageio import mimread
from PIL import Image
from time import sleep
#from rgbmatrix import RGBMatrix, RGBMatrixOptions
import cv2


def getlistfiles(mypath):
    return [path.join(mypath, f) for f in listdir(mypath) if path.isfile(path.join(mypath, f))]

def fadeIn(pathimg1, pathimg2, dsize, len=10):
    """"Build transition with 2 images cv2."""
    if isinstance(pathimg1, str):
        img1 = cv2.imread(pathimg1)
    else:
        img1 = pathimg1
    img1 = cv2.resize(img1, dsize)
    if isinstance(pathimg2, str):
        img2 = cv2.imread(pathimg2)
    else:
        img2 = pathimg2
    img2 = cv2.resize(img2, dsize)
    yield(img1)
    for seq in range(0,len): 
        fadein = seq/float(len) 
        dst = cv2.addWeighted(img1, 1-fadein, img2, fadein, 0)
        yield(dst)

def buildtransitions(pathimg, dsize, duration, duranim, durtrans, passgif = 4):
    """Build list Images + list tempo for the reading."""
    listfiles = getlistfiles(pathimg)
    indimg1 = 0
    listtrans = []
    tempo = []
    while indimg1 < len(listfiles):
        if indimg1 + 1 == len(listfiles):
            indimg2 = 0
        else:
            indimg2 = indimg1 + 1
        print(('0' + str(indimg1))[-2:], ('0' + str(indimg2))[-2:], listfiles[indimg1], listfiles[indimg2])
        if listfiles[indimg1].endswith('gif'):
           listgif = builCV2Gif(listfiles[indimg1], dsize)
           listtrans += listgif * passgif
           tempo += [duranim] * len(listgif) * passgif
           if listfiles[indimg2].endswith('gif'):
               listgif2 = builCV2Gif(listfiles[indimg2], dsize)
               img1 = listgif[0]
               img2 = listgif2[0]
           else:
               img1 = listgif[0]
               img2 = listfiles[indimg2]
           tempo += [duranim] + [durtrans] * 10
        elif listfiles[indimg2].endswith('gif'):
           listgif = builCV2Gif(listfiles[indimg2], dsize)
           img1 = listfiles[indimg1]
           img2 = listgif[0]
           tempo += [duration] + [durtrans] * 10
        else:
           img1 = listfiles[indimg1]
           img2 = listfiles[indimg2]
           tempo += [duration] + [durtrans] * 10
        listtrans += fadeIn(img1, img2, dsize)
        indimg1 += 1
    return listtrans, tempo


def builCV2Gif(pathgif, dsize):
    """Convert file Gif to list images cv2."""
    gif = mimread(pathgif)
    nums = len(gif)
    #print("Total {} frames in the gif".format(nums))
    # convert form RGB to BGR
    listcv2  = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    listgif = []
    for img in listcv2:
        listgif.append(cv2.resize(img, dsize))
    return listgif


def normalizeListimages(listimages):
    """Convert Images cv2 to Images PIL."""
    indice = 0
    listresult = []
    for imgcv2 in listimages:
        img = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        #cv2.imshow('window', imgcv2)
        #cv2.waitKey(1) 
        #sleep(tempo[indice])
        listresult.append(im_pil.convert('RGB'))
        indice += 1
    return listresult

# Configuration matrix for the matrix
# options = RGBMatrixOptions()
# options.rows = 32
# options.cols = 64
# options.chain_length = 2
# options.parallel = 1
# options.hardware_mapping = 'adafruit-hat'
# options.pixelmapper = "U-mapper;Rotate:180"

# matrix = RGBMatrix(options = options)

dsize = 64, 64
durimage = 5 
durtrans = 0.2
durangif = 0.05
pathimg = r'.\album'
listimagescv2, tempo = buildtransitions(pathimg, dsize, durimage, durangif, durtrans)
listimages = normalizeListimages(listimagescv2)
# save gif file result
listimages[0].save('pillow_imagedraw.gif', save_all=True, append_images=listimages[1:], optimize=False, duration=sum(tempo, 0) * 5, loop=0)

# display panel
print("duration: {}s, {} Images: Press CTRL-C to stop.".format(int(sum(tempo, 0)), len(listimages)))
step = 1
while True:
    indice = 0
    for img in listimages:
        #if tempo[indice] == durimage:
        #    img.show()
        #print(tempo[indice])
        #matrix.SetImage(img)
        sleep(tempo[indice])
        indice += 1

# problem: 
#    resize 48 to 64
