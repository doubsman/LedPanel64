#!/usr/bin/env python
from os import listdir, path
from imageio import mimread
from PIL import Image
from time import sleep
import cv2
from image_scroller import ImageScroller


class ImagesPath():

    def __init__(self, matrix, size, durationimg, durationgif, passgif = 4):
        super(ImagesPath, self).__init__()
        self.matrix = matrix
        self.pathimg = ""
        self.size = size
        self.durationimg = durationimg
        self.durationgif = durationgif
        self.passgif = passgif
        self.listimages = []
        self.tempo = []
    
    def display_image(self, imgpath):
       img = Image.open(imgpath)
       self.matrix.SetImage(img.convert('RGB'))
    
    def display_images(self, imgdefiled = True, imgscrolled = False, imgmyscrolled = True):
        indice = 0
        for img in self.listimages:
            if self.tempo[indice] == self.durationimg:
                if imgscrolled:
                    # Then scroll image across matrix...
                    for n in range(-64, 65):  # Start off top-left, move off bottom-right
                        self.matrix.Clear()
                        self.matrix.SetImage(img, n, n)
                        sleep(0.05)
                if imgmyscrolled:
                    ImageScroller(self.matrix, self.size, img).image_scroller()
            if imgdefiled:
                self.matrix.SetImage(img)
                sleep(self.tempo[indice])
                indice += 1

    def preload_list(self, pathimg):
        """Build list Images + list tempo for the reading."""
        self.pathimg = pathimg
        print('build list images :' + self.pathimg)
        listfiles = self.get_list_files(self.pathimg)
        listfiles.sort(key=lambda v: v.upper())
        for imgpath in listfiles:
            if imgpath.endswith('gif'):
               listgif = self.build_list_gif(imgpath)
               self.listimages += listgif * self.passgif
               self.tempo += [self.durationgif] * len(listgif) * self.passgif
            else:
               img = Image.open(imgpath)
               self.listimages.append(img.convert('RGB'))
               self.tempo += [self.durationimg]
        print("   duration: {}s, {} Images".format(int(sum(self.tempo, 0)), len(self.listimages)))
   
    def build_list_gif(self, pathgif):
        """Convert file Gif to list images cv2."""
        dsize = (self.size, self.size)
        gif = mimread(pathgif)
        nums = len(gif)
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



class ImageTransition():

    def __init__(self, matrix, pathimg, size, durationimg, durationgif, durationtra, passgif = 4, fadestep = 10):
        super(ImageTransition, self).__init__()
        self.matrix = matrix
        self.pathimg = pathimg
        self.size = size
        self.durationimg = durationimg
        self.durationgif = durationgif
        self.durationtra = durationtra
        self.listimages = []
        self.listimgcv2 = []
        self.tempo = []
        # build list images carroussel
        print('build list images transition :' + pathimg)
        self.build_transitions(passgif, fadestep)
        self.convert_list_images()
        print("   duration: {}s, {} Images".format(int(sum(self.tempo, 0)), len(self.listimages)))

    def display_carousel(self):
        indice = 0
        for img in self.listimages:
            self.matrix.SetImage(img)
            sleep(self.tempo[indice])
            indice += 1

    def build_transitions(self, passgif, fadestep):
        """Build list Images + list tempo for the reading."""
        listfiles = self.get_list_files()
        listfiles.sort(key=lambda v: v.upper())
        indimg1 = 0
        while indimg1 < len(listfiles):
            if indimg1 + 1 == len(listfiles):
                indimg2 = 0
            else:
                indimg2 = indimg1 + 1
            if indimg1 == indimg2:
               listgif = self.builCV2Gif(listfiles[indimg1])
               self.listimgcv2 += listgif * passgif
               self.tempo += [self.durationgif] * len(listgif) * passgif
               break
            print('   ' + ('0' + str(indimg1))[-2:], ('0' + str(indimg2))[-2:], listfiles[indimg1], listfiles[indimg2])
            if listfiles[indimg1].endswith('gif'):
               listgif = self.builCV2Gif(listfiles[indimg1])
               self.listimgcv2 += listgif * passgif
               self.tempo += [self.durationgif] * len(listgif) * passgif
               img1 = listgif[0]
               if listfiles[indimg2].endswith('gif'):
                   listgif2 = self.builCV2Gif(listfiles[indimg2])
                   img2 = listgif2[0]
               else:
                   img2 = listfiles[indimg2]
               self.tempo += [self.durationgif] + [self.durationtra] * 10
            elif listfiles[indimg2].endswith('gif'):
               listgif = self.builCV2Gif(listfiles[indimg2])
               img1 = listfiles[indimg1]
               img2 = listgif[0]
               self.tempo += [self.durationimg] + [self.durationtra] * 10
            else:
               img1 = listfiles[indimg1]
               img2 = listfiles[indimg2]
               self.tempo += [self.durationimg] + [self.durationtra] * 10
            self.listimgcv2 += self.fadeIn(img1, img2, fadestep)
            indimg1 += 1

    def get_list_files(self):
        return [path.join(self.pathimg, f) for f in listdir(self.pathimg) if path.isfile(path.join(self.pathimg, f))]
    
    def fadeIn(self, pathimg1, pathimg2, fadestep):
        """"Build transition with 2 images cv2."""
        dsize = (self.size, self.size)
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
        for seq in range(0, fadestep): 
            fadein = seq/float(fadestep) 
            dst = cv2.addWeighted(img1, 1 - fadein, img2, fadein, 0)
            yield(dst)

    def builCV2Gif(self, pathgif, first = True):
        """Convert file Gif to list images cv2."""
        dsize = (self.size, self.size)
        gif = mimread(pathgif)
        nums = len(gif)
        # convert form RGB to BGR
        listcv2  = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
        listgif = []
        for img in listcv2:
            listgif.append(cv2.resize(img, dsize))
        return listgif
    
    def convert_list_images(self):
        """Convert Images cv2 to Images PIL."""
        indice = 0
        for imgcv2 in self.listimgcv2:
            img = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            #cv2.imshow('window', imgcv2)
            #cv2.waitKey(1) 
            #sleep(tempo[indice])
            self.listimages.append(im_pil.convert('RGB'))
            indice += 1
        self.listimgcv2.clear()

    def create_gif(self, pathfile = 'carousel.gif'):
        self.listimages[0].save(pathfile, save_all=True, append_images=self.listimages[1:], optimize=False, duration=len(self.tempo)/50, loop=0)



