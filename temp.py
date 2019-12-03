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

img_size        = (200,90)
screen_size     = (1280,720)
warn_size     = (1260,700)
temp_text_pos   = (1050,500)
heart_text_pos  = (1050,580)
thermo_pos      = (980,510)
heart_pos       = (980,590)
warning_x       = (1160)
font_size       = 50

font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
img         = Image.new('RGBA',img_size,color=Color4.transparent)
temp_text   = ImageDraw.Draw(img)
img2        = Image.new('RGBA',img_size,color=Color4.transparent)
heart_text  = ImageDraw.Draw(img2)

warn        = Image.new('RGBA',screen_size,color=Color4.transparent)
warn_draw   = ImageDraw.Draw(warn)
warn_draw.rectangle([(10,10),warn_size],fill=None, outline=Color3.yellow)

heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
warning     = Image.open("warning.png").resize((55,50))
pad         = Image.new('RGBA', screen_size)

masks       = []
for i in range(10):
    masks.append(Image.open("mask"+str(i)+".png").resize((55,50)).convert("L"))

prev_temperature    = -1
prev_heartrate      = -1
doInit              = True
#---------- setup ----------#


#while(True):
# Get ADC value and convert to temperature
# ADC_value = readAdc(channel, CLK, MISO, MOSI, CS)
temperature         = str(random.randint(150,160))
heartrate           = str(random.randint(160,170))

sleep(0.1)

# clear and redraw
temp_text.rectangle([(0,0),img_size],fill=Color4.transparent)
temp_text.text((0,0),str(int(temperature)), font=font, fill=Color3.black)
heart_text.rectangle([(0,0),img_size],fill=Color4.transparent)
heart_text.text((0,0),str(int(heartrate)), font=font, fill=Color3.black)

# create overlay using drawing
pad.paste(warn, (0,0))
pad.paste(img, temp_text_pos)
pad.paste(img2, heart_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
warning.putalpha(masks[3])
pad.paste(warning, (warning_x,thermo_pos[1]))
warning.putalpha(masks[7])
pad.paste(warning, (warning_x,heart_pos[1]))
pad.save("new.png")

prev_temperature = temperature
prev_heartrate = heartrate
