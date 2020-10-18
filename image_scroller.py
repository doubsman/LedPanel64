#!/usr/bin/env python
from PIL import Image
from time import sleep


class ImageScroller():

    def __init__(self, matrix, img):
        super(ImageScroller, self).__init__()
        self.step = matrix.width
        self.matrix = matrix
        self.listimg = []
        if isinstance(img, str):
            print('build list images scrolling image : ' + img)
            self.img = Image.open(img)
        else:
            self.img = img
        self.width, self.heigth = self.img.size
        self.build_images()
        #print("   {} Images".format(len(self.listimg)))

    def image_scroller(self, numpart = 0, lenpart = 1):
        """Display to panel (step, step) scroll image."""
        double_buffer = self.matrix.CreateFrameCanvas()
        slide = int(len(self.listimg)/lenpart)
        for img in self.listimg[slide * numpart:(slide * numpart) + slide]:
            xpos = 0
            img = img.convert('RGB')
            img_width, img_height = img.size
            double_buffer.SetImage(img, -xpos)
            double_buffer.SetImage(img, -xpos + img_width)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            sleep(0.01)

    def build_images(self):
        end = 0
        while self.width >= end:
            if end <= self.step:
                # first frame
                result = self.extract_part_image(self.width - end, self.width)
            else:
                # middle frames
                result = self.extract_part_image(self.width - end, self.width - end + self.step)
            self.listimg.append(result)
            end += 1
        # last frame
        for ind in range(0, self.step):
            result = self.extract_part_image(0 - ind, end - ind)
            self.listimg.append(result)

    def extract_part_image(self, start, end):
        box = (start, 0, end, self.heigth)  
        im2 = self.img.crop(box)
        par = im2.copy()
        img = Image.new('RGB', (self.step, self.step), 'black')
        img.paste(par)
        return img

    def create_gif(self, pathfile = 'Leagues_1792.gif'):
        self.listimg[0].save(pathfile, save_all=True, append_images=self.listimg[1:], optimize=False, duration=len(self.listimg)/50, loop=0)


