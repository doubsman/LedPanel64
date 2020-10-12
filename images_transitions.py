#!/usr/bin/env python
from time import sleep
import cv2
from images_display import ImagesDisplay


class ImagesTransitions(ImagesDisplay):

    def __init__(self, matrix, pathimg, size, durationimg, durationgif, durationtra, passgif = 4, fadestep = 10):
        self.matrix = matrix
        self.pathimg = pathimg
        self.size = size
        self.durationimg = durationimg
        self.durationgif = durationgif
        self.durationtra = durationtra
        self.listimages = []
        self.tempo = []
        # build list images
        print('build list images transitions :' + pathimg)
        self.build_transitions(passgif, fadestep)
        print("   duration: {}s, {} Images".format(int(sum(self.tempo, 0)), len(self.listimages)))

    def display_imagesTransitions(self):
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
            print('   ' + ('0' + str(indimg1))[-2:], ('0' + str(indimg2))[-2:], listfiles[indimg1], listfiles[indimg2])
            if listfiles[indimg1].endswith('gif'):
                listgif = self.build_list_gif(listfiles[indimg1])
                self.listimages += listgif * passgif
                self.tempo += [self.durationgif] * len(listgif) * passgif
                img1 = listgif[0]
                if listfiles[indimg2].endswith('gif') and indimg1 != indimg2:
                    listgif2 = self.build_list_gif(listfiles[indimg2])
                    img2 = listgif2[0]
                elif indimg1 != indimg2:
                    img2 = listfiles[indimg2]
                else:
                    img2 = img1
                self.tempo += [self.durationgif] + [self.durationtra] * 10
            elif listfiles[indimg2].endswith('gif'):
                listgif = self.build_list_gif(listfiles[indimg2])
                img1 = listfiles[indimg1]
                img2 = listgif[0]
                self.tempo += [self.durationimg] + [self.durationtra] * 10
            else:
                img1 = listfiles[indimg1]
                img2 = listfiles[indimg2]
                self.tempo += [self.durationimg] + [self.durationtra] * 10
            if indimg1 != indimg2:
                self.listimages += self.fadeIn(img1, img2, fadestep)
            indimg1 += 1

    def fadeIn(self, pathimg1, pathimg2, fadestep):
        """"Build transition with 2 images cv2."""
        img1 = self.prepare_imagecv2(pathimg1)
        img2 = self.prepare_imagecv2(pathimg2)
        listfadecv2 = [img1]
        for seq in range(0, fadestep): 
            fadein = seq/float(fadestep) 
            dst = cv2.addWeighted(img1, 1 - fadein, img2, fadein, 0)
            listfadecv2.append(dst)
        return self.convert_list_images(listfadecv2)

    def prepare_imagecv2(self, imgpath):
        dsize = (self.size, self.size)
        if isinstance(imgpath, str):
            img = cv2.imread(imgpath)           
        else:
            img = imgpath
        return cv2.resize(img, dsize)




