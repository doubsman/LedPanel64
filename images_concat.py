#!/usr/bin/env python

from os import listdir, path
from PIL import Image
from image_scroller import ImageScroller
from time import sleep


class ImagesConcat():

    def __init__(self, matrix, pathimgs):
        super(ImagesConcat, self).__init__()
        self.matrix = matrix
        self.pathimgs = pathimgs
        self.listscroll = []
        listfiles = self.get_list_files()
        listfiles.sort(key=lambda v: v.upper())
        listfiles = [i for i in listfiles if not i.endswith('gif')]
        indice = 0
        for pathimg in listfiles:
            img = self.prepare_pathimg(pathimg)
            if indice > 0:
                self.concatimgs = self.get_concat_h(self.concatimgs, img)
            else:
                self.concatimgs = img
            indice += 1
        print('build Banner list scrolling images : ' + pathimgs)
        self.listscroll = ImageScroller(self.matrix, self.concatimgs)
        #self.concatimgs.save('concat.png')

    def display_concatimages(self, seconds = 10):
        double_buffer = self.matrix.CreateFrameCanvas()
        indice = 0
        for img in self.listscroll.listimg:
            xpos = 0
            img_width, _ = img.size
            double_buffer.SetImage(img, -xpos)
            double_buffer.SetImage(img, -xpos + img_width)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            if (indice % self.matrix.width) == 0:
                sleep(seconds)
            else:
                sleep(0.01)
            indice +=1            

    def prepare_pathimg(self, pathimg):
        imgtemp = Image.open(pathimg)
        imgtemp = imgtemp.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        return imgtemp.convert('RGB')

    def get_concat_h(self, im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    def get_concat_v(self, im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    def get_list_files(self):
        return [path.join(self.pathimgs, f) for f in listdir(self.pathimgs) if path.isfile(path.join(self.pathimgs, f))]
