import picamera
from PIL import Image
from time import sleep

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 24
camera.start_preview()

# Load the arbitrarily sized image
img = Image.open('heart.png')
# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGBA', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
# Paste the original image into the padded one
pad.paste(img, (0, 0))

pad2 = Image.new('RGBA', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
# Paste the original image into the padded one
pad2.paste(img, (300, 0))

pad2 = Image.new('RGBA', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
# Paste the original image into the padded one
pad2.paste(img, (-300, 0))


# Add the overlay with the padded image as the source,
# but the original image's dimensions
o = camera.add_overlay(pad.tobytes(), size=img.size)
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
o.alpha = 128
o.layer = 3
c = 0
# Wait indefinitely until the user terminates the script
while True:
    c = 1-c
    camera.remove_overlay(o)
    o = camera.add_overlay([pad,pad2][c].tobytes(), size=img.size)
    o.alpha = 128
    o.layer = 3
    sleep(1)
