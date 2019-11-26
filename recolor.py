import png, array
import os, sys
from colors import Color4

color = Color4.l_red
fname = "heart.png"
result = "heart.png"

reader = png.Reader(filename=fname)
w, h, pixels, metadata = reader.read_flat()

for i in range(h):
    for j in range(w):
        vals = pixels[((i*w)+j)*4:((i*w)+j)*4+4]
        if vals[3]!=0 and ((i*w)+j)*4+3 < len(pixels):
            for k in range(4):
                pixels[((i*w)+j)*4+k] = color[k]

output = open(result, 'wb')
writer = png.Writer(w, h, greyscale=False, alpha=True)
writer.write_array(output, pixels)
output.close()