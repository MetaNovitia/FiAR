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

img_size        = (500,90)
screen_size     = (1280,720)
temp_text_pos   = (1050,500)
hr_text_pos     = (1050,580)
heart_pos       = (980,510)
thermo_pos      = (980,590)
font_size       = 50

camera = picamera.PiCamera()
camera.resolution = screen_size
camera.exposure_mode = "sports"
camera.start_preview()

font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
img         = Image.new('RGBA',img_size,color=Color4.transparent)
temp_text   = ImageDraw.Draw(img)
img2        = Image.new('RGBA',img_size,color=Color4.transparent)
hr_text     = ImageDraw.Draw(img2)


heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
pad         = Image.new('RGBA', screen_size)
pad.paste(img, hr_text_pos)
pad.paste(img2, temp_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
overlay = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
#---------- setup ----------#


while(True):
    # Get ADC value and convert to temperature
    # ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
    ADC_value = random.randint(160,170)
    heartrate   = str(random.randint(160,170))
    temperature = str(random.randint(160,170))
    sleep(0.5)
    
    # clear and redraw
    temp_text.rectangle([(0,0),img_size],fill=Color4.transparent)
    temp_text.text((0,0),str(int(temperature)), font=font, fill=Color3.black)
    hr_text.rectangle([(0,0),img_size],fill=Color4.transparent)
    hr_text.text((0,0),str(int(heartrate)), font=font, fill=Color3.black)

    # create overlay using drawing
    pad.paste(img, hr_text_pos)
    pad.paste(img2, temp_text_pos)
    pad.paste(heart, heart_pos)
    pad.paste(thermo, thermo_pos)

    overlay_temp = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
    overlay_temp.alpha = 128
    overlay_temp.layer = 3

    # remove previous overlay
    camera.remove_overlay(overlay)
    overlay=overlay_temp
