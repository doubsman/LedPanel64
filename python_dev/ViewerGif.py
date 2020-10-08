#!/usr/bin/env python

import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageSequence, GifImagePlugin

# Matrix size
size = 64, 64

# Open source
if len(sys.argv) < 2:
  sys.exit("Require an image argument")
else :
  image_file = sys.argv[1]

im = Image.open(image_file)

# Get gif frames
frames = ImageSequence.Iterator(im)

# Resize gif frames to matrix
def thumbnails(frames):
  for frame in frames:
      thumbnail = frame.copy()
      thumbnail.thumbnail(size, Image.ANTIALIAS)
      yield thumbnail

frames = thumbnails(frames)

# Save output
om = next(frames)# Handle first frame separately
om.info = im.info# Copy sequence info
om.save("out.gif", save_all = True, append_images = list(frames))

# Pull back in resized gif
image = Image.open("out.gif")

# Configuration matrix for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.pixelmapper = "U-mapper;Rotate:180"

matrix = RGBMatrix(options = options)

# Loop through gif frames and display on matrix.
while True:
  for frame in range(0, image.n_frames):
      print(image.n_frames)
      image.seek(frame)
      matrix.SetImage(image.convert('RGB'))
      time.sleep(1)

# Handle quiting
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)