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
temp_text_pos   = (1050,500)
heart_pos       = (980,510)
thermo_pos      = (980,590)
font_size       = 50

img         = Image.new('RGBA',img_size,color=Color4.transparent)
font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
temp_text   = ImageDraw.Draw(img)

img         = Image.new('RGBA',img_size,color=Color4.transparent)
font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
heart_text  = ImageDraw.Draw(img)

heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
pad         = Image.new('RGBA', screen_size)
#---------- setup ----------#


#while(True):
# Get ADC value and convert to temperature
# ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
heartrate   = str(random.randint(160,170))
temperature = str(random.randint(160,170))

sleep(0.1)

# clear and redraw
temp_text.rectangle([(0,0),img_size],fill=Color4.transparent)
temp_text.text((0,0),str(int(temperature)), font=font, fill=Color3.black)

# create overlay using drawing
pad.paste(img, temp_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
pad.save("new.png")
