import png, array
import os, sys
from colors import Color4

color = (20,20,20,255)
fname = "warning.png"
result = "mask"

reader = png.Reader(filename=fname)
w, h, pixels, metadata = reader.read_flat()
newpix = [[] for _ in range(10)]

for i in range(h):
    for j in range(w):
        vals = pixels[((i*w)+j)*4:((i*w)+j)*4+4]
        if vals[3]!=0 and ((i*w)+j)*4+3 < len(pixels):
            for p in range(10):
                for k in range(3):
                    newpix[p].append(color[k]*p)
                    #pixels[((i*w)+j)*4+k] = color[k]
                newpix[p].append(255)
        elif vals[3]==0 and ((i*w)+j)*4+3 < len(pixels):
            for p in range(10):
                for k in range(4):
                    newpix[p].append(0)
                    #pixels[((i*w)+j)*4+k] = 0

for p in range(10):
    output = open(result+str(p)+".png", 'wb')
    writer = png.Writer(w, h, greyscale=False, alpha=True)
    writer.write_array(output, newpix[p])
    output.close()