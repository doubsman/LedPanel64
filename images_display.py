#!/usr/bin/env python

from os import listdir, path
from imageio import mimread
from PIL import Image
from time import sleep
import cv2
from image_scroller import ImageScroller


class ImagesDisplay():

    def __init__(self, matrix, size, durationimg, durationgif, passgif = 4):
        super(ImagesDisplay, self).__init__()
        self.matrix = matrix
        self.pathimg = ""
        self.size = size
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

    def display_scrollimage(self, imgpath):
        img = self.prepare_image(imgpath)
        # Then scroll image across matrix...
        for n in range(-64, 65):  # Start off top-left, move off bottom-right
            self.matrix.Clear()
            self.matrix.SetImage(img, n, n)
            sleep(0.05)

    def prepare_image(self, imgpath):
        if isinstance(imgpath, str):
            img = Image.open(imgpath)
        else:
            img = imgpath
        return img.convert('RGB')

    def display_images(self, imgdefiled = True, imgscrolled = True, imgmyscrolled = True):
        indice = 0
        for img in self.listimages:
            # not for gifs
            if self.tempo[indice] == self.durationimg:
                if imgscrolled:
                    self.display_scrollimage(img)
                if imgmyscrolled:
                    ImageScroller(self.matrix, img).image_scroller()
            if imgdefiled:
                self.display_image(img, indice)
                indice += 1

    def preload_list(self, pathimg):
        """Build list Images + list tempo for the reading."""
        self.pathimg = pathimg
        print('build list images :' + self.pathimg)
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
   
    def build_list_gif(self, pathgif):
        """Convert file Gif to list images cv2."""
        dsize = (self.size, self.size)
        gif = mimread(pathgif)
        # convert form RGB to BGR
        listcv2  = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
        listgif = []
        for img in listcv2:
            listgif.append(cv2.resize(img, dsize))
        return self.convert_list_images(listgif)
    
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
        return [path.join(self.pathimg, f) for f in listdir(self.pathimg) if path.isfile(path.join(self.pathimg, f))]
    
    def create_gif(self, pathfile = 'carousel.gif'):
        self.listimages[0].save(pathfile, save_all=True, append_images=self.listimages[1:], optimize=False, duration=len(self.tempo)/50, loop=0)
