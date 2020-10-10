
#!/usr/bin/env python
from os import system



class MatrixSim64():

    def __init__(self, size):
        super(MatrixSim64, self).__init__()
        self.size = size
	
    def SetImage(self, img, x=0, y=0):
        img.save('/tmp/Legopanel.jpg')
        system('./tools/imcat /tmp/Legopanel.jpg')