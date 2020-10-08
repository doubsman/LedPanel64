import time
import cv2

def fadeIn (pathimg1, pathimg2, len=10):
    img1 = cv2.imread(pathimg1)
    img2 = cv2.imread(pathimg2)
    #while True: 
    for seq in range(0,len): 
        fadein = seq/float(len) 
        dst = cv2.addWeighted(img1, 1-fadein, img2, fadein, 0) 
        cv2.imshow('window', dst)
        filename = r"E:\Download\python\test" + str(seq) + ".jpg"
        cv2.imwrite(filename, dst)
        cv2.waitKey(1) 
        print(fadein) 

img1 = r"E:\Download\python\album\download.png"
img2 = r"E:\Download\python\album\downloadt.png"
fadeIn(img1, img2)