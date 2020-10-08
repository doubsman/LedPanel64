import cv2
import imageio
import pathlib

def fadeInGif(pathimg1, pathimg2, filegif, len=10, frames_per_second=2):
    img1 = cv2.imread(pathimg1)
    img2 = cv2.imread(pathimg2)
    listimg = []
    for seq in range(0,len): 
        fadein = seq/float(len) 
        dst = cv2.addWeighted(img1, 1-fadein, img2, fadein, 0) 
        listimg.append(dst)
        cv2.waitKey(1)
        print(fadein) 
    imageio.mimsave(filegif.as_posix(), listimg, fps=frames_per_second)

img1 = r"E:\Download\python\album\download.png"
img2 = r"E:\Download\python\album\downloadt.png"
fadeInGif(img1, img2, pathlib.Path('E:/Download/python/final.gif'))