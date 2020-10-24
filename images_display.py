#!/usr/bin/env python

from os import listdir, path
from imageio import mimread
from PIL import Image
from time import sleep
import cv2
from image_scroller import ImageScroller


class ImagesDisplay():

    def __init__(self, matrix, durationimg, durationgif, passgif = 6):
        super(ImagesDisplay, self).__init__()
        self.matrix = matrix
        self.pathimgs = ""
        self.size = self.matrix.width
        self.durationimg = durationimg
        self.durationgif = durationgif
        self.passgif = passgif
        self.listimages = []
        self.tempo = []
    
    def display_image(self, imgpath, indice = -1):
        img = self.prepare_image(imgpath)
        self.matrix.SetImage(img)
        if indice > -1: 
            sleep(self.tempo[indice])

    def display_scrollimage(self, imgpath, speed = 0.05):
        img = self.prepare_image(imgpath)
        # Then scroll image across matrix...
        for n in range(-64, 65):  # Start off top-left, move off bottom-right
            self.matrix.Clear()
            self.matrix.SetImage(img, n, n)
            sleep(speed)

    def display_rotateimage(self, imgpath, speed = 0.02):
        img = self.prepare_image(imgpath)
        for n in range(0, 360):
            rotated = img.rotate(n)
            self.matrix.SetImage(rotated)
            sleep(speed)

    def display_psyrotateimage(self, imgpath, sens = 1, speed = 0.02):
        img = self.prepare_image(imgpath)
        for n in range(0, 360, 18):
            percent = abs(sens - (n/360)) 
            nwidth, nheight = img.size
            nwidth = max((nwidth * percent) , 1)
            nheight = max((nheight * percent) , 1)
            imgtemp = img.resize((int(nwidth), int(nheight)), Image.ANTIALIAS)
            img_w, img_h = imgtemp.size
            rotated = Image.new('RGB', (self.size, self.size), 'black')
            bg_w, bg_h = rotated.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            rotated.paste(imgtemp, offset)
            rotated = rotated.rotate(n)
            self.matrix.SetImage(rotated)
            sleep(speed)

    def prepare_image(self, imgpath):
        if isinstance(imgpath, str):
            img = Image.open(imgpath)
        else:
            img = imgpath
        return img.convert('RGB')

    def display_images(self, imgscrolled = False, imgmyscrolled = True):
        #self.create_gif()
        indice = 0
        for img in self.listimages:
            # not for gifs
            if self.tempo[indice] == self.durationimg and imgscrolled:
                self.display_scrollimage(img)
            if self.tempo[indice] == self.durationimg and imgmyscrolled:
                imgscro = ImageScroller(self.matrix, img)
                imgscro.image_scroller(0, 2)
            self.display_image(img, indice)
            if self.tempo[indice] == self.durationimg and imgmyscrolled:
                imgscro.image_scroller(1, 2)
            indice += 1

    def preload_pathimgs(self, pathimgs):
        """Build list Images + list tempo for the reading."""
        self.pathimgs = pathimgs
        print('build list images :' + self.pathimgs)
        listfiles = self.get_list_files()
        listfiles.sort(key=lambda v: v.upper())
        for imgpath in listfiles:
            if imgpath.endswith('gif'):
               listgif = self.build_list_gif(imgpath)
               self.listimages += listgif * self.passgif
               self.tempo += [self.durationgif] * len(listgif) * self.passgif
            else:
               img = Image.open(imgpath)
               img = img.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
               self.listimages.append(img.convert('RGB'))
               self.tempo += [self.durationimg]
        print("   duration: {}s, {} Images".format(int(sum(self.tempo, 0)), len(self.listimages)))
   
    def build_list_gif(self, pathgif, nocv2 = True):
        """Convert file Gif to list images cv2."""
        dsize = (self.size, self.size)
        gif = mimread(pathgif)
        # convert form RGB to BGR
        listcv2  = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
        listgif = []
        for img in listcv2:
            listgif.append(cv2.resize(img, dsize))
        if nocv2:
            return self.convert_list_images(listgif)
        else:
            return listgif
    
    def convert_list_images(self, listcv2):
        """Convert Images cv2 to Images PIL."""
        indice = 0
        listimg = []
        for imgcv2 in listcv2:
            img = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            #cv2.imshow('window', imgcv2)
            #cv2.waitKey(1) 
            #sleep(tempo[indice])
            listimg.append(im_pil.convert('RGB'))
            indice += 1
        return listimg
    
    def get_list_files(self):
        return [path.join(self.pathimgs, f) for f in listdir(self.pathimgs) if path.isfile(path.join(self.pathimgs, f))]
    
    def create_gif(self, pathfile = '/tmp/display_images.gif'):
        self.listimages[0].save(pathfile, save_all=True, append_images=self.listimages[1:], optimize=False, duration=len(self.tempo)/50, loop=0)
