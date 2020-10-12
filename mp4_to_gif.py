from imageio import get_reader,  get_writer
from sys import stdout
from os import path

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, targetFormat):
    """Reference: http://imageio.readthedocs.io/en/latest/examples.html#convert-a-movie"""
    outputpath = path.splitext(inputpath)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        stdout.write("\rframe {0}".format(i))
        stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")

convertFile(r'coquine_online.mp4', TargetFormat.GIF)
