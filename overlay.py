import picamera
from spi import readAdc, getTemperature
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import random

#---------- setup ----------#

CLK = 18
MISO = 23
MOSI = 24
CS = 25
channel = 0
rref = 1000

img_size = (500,500)
txt_size = (300,300)
screen_size = (1280,720)
txt_pos = (0,0)

camera = picamera.PiCamera()
camera.resolution = screen_size
camera.exposure_mode = "sports"
camera.start_preview()

img = Image.new('RGBA',img_size,color=(0,0,0,0))
font = ImageFont.truetype("OpenSans-Regular.ttf",size=100)
d = ImageDraw.Draw(img)
pad = Image.new('RGBA', screen_size)
overlay1 = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)    
#---------- setup ----------#
ct = 0
while(True):
    #ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
    ADC_value = 1+(ct%1022)
    ct+=1
    temperature = getTemperature(ADC_value, rref)
    print(ADC_value, temperature)
    sleep(0.1)
    
    d.rectangle([(0,0),img_size],fill=(255,255,255,0))
    d.text(txt_pos,str(int(temperature)), font=font, fill=(255,255,0))

    pad.paste(img, (100, 100))
    overlay2 = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
    overlay2.alpha = 128
    overlay2.layer = 3
    camera.remove_overlay(overlay1)
    overlay1=overlay2
