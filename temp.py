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
heart_text_pos  = (1050,580)
thermo_pos      = (980,510)
heart_pos       = (980,590)
font_size       = 50

font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
img         = Image.new('RGBA',img_size,color=Color4.transparent)
temp_text   = ImageDraw.Draw(img)
img2        = Image.new('RGBA',img_size,color=Color4.transparent)
heart_text  = ImageDraw.Draw(img2)

heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
pad         = Image.new('RGBA', screen_size)

prev_temperature    = -1
prev_heartrate      = -1
doInit              = True
#---------- setup ----------#


#while(True):
# Get ADC value and convert to temperature
# ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
temperature         = str(random.randint(150,160))
heartrate           = str(random.randint(160,170))
if doInit:
    prev_temperature    = temperature
    prev_heartrate      = heartrate
temperature_delta   = temperature-prev_temperature
heartrate_delta     = heartrate-prev_heartrate

sleep(0.1)

# clear and redraw
temp_text.rectangle([(0,0),img_size],fill=Color4.transparent)
temp_text.text((0,0),str(int(temperature)), font=font, fill=Color3.black)
heart_text.rectangle([(0,0),img_size],fill=Color4.transparent)
heart_text.text((0,0),str(int(heartrate)), font=font, fill=Color3.black)

# create overlay using drawing
pad.paste(img, temp_text_pos)
pad.paste(img2, heart_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
pad.save("new.png")

prev_temperature = temperature
prev_heartrate = heartrate
