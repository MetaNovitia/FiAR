import picamera
from spi import readAdc, getTemperature
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from colors import Color3, Color4
import random

#---------- setup ----------#
CLK     = 18
MISO    = 23
MOSI    = 24
CS      = 25
channel = 0
rref    = 1000

img_size        = (500,200)
screen_size     = (1280,720)
temp_text_pos   = (0,0)
font_size       = 70

camera = picamera.PiCamera()
camera.resolution = screen_size
camera.exposure_mode = "sports"
camera.start_preview()

img     = Image.new('RGBA',img_size,color=Color4.transparent)
font    = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
drawing = ImageDraw.Draw(img)
pad     = Image.new('RGBA', screen_size)
overlay = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
#---------- setup ----------#


while(True):
    # Get ADC value and convert to temperature
    # ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
    ADC_value = random.randint(160,170)
    temperature = getTemperature(ADC_value, rref)
    print(ADC_value, temperature)
    sleep(0.1)
    
    # clear and redraw
    drawing.rectangle([(0,0),img_size],fill=Color4.transparent)
    drawing.text((0,0),str(int(temperature)), font=font, fill=Color3.black)

    # create overlay using drawing
    pad.paste(img, temp_text_pos)
    overlay_temp = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
    overlay_temp.alpha = 128
    overlay_temp.layer = 3

    # remove previous overlay
    camera.remove_overlay(overlay)
    overlay=overlay_temp
