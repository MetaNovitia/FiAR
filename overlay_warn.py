import picamera
import spi
from spi import ReadChannel, getTemperature, heartRate
from PIL import Image, ImageDraw, ImageFont
from time import sleep,time
from colors import Color3, Color4
from gps import getGPS
import random

#---------- setup ----------#
rref    = 1000                 #reference resistance value 
lowestHR = 40
highestHR = 200

img_size        = (500,90)     
screen_size     = (1280,720)
temp_text_pos   = (1050,500)
hr_text_pos     = (1050,580)
loc_text_pos    = (0,0)
heart_pos       = (980,510)
thermo_pos      = (980,590)
warn_size       = (1270,710)
warning_x       = (1160)
font_size       = 50

#initialze camera
camera = picamera.PiCamera()
camera.resolution = screen_size
camera.exposure_mode = "sports"
camera.start_preview()


font        = ImageFont.truetype("OpenSans-Regular.ttf",size=font_size)
img         = Image.new('RGBA',img_size,color=Color4.transparent)
temp_text   = ImageDraw.Draw(img)
img2        = Image.new('RGBA',img_size,color=Color4.transparent)
hr_text     = ImageDraw.Draw(img2)

img3        = Image.new('RGBA',img_size,color=Color4.transparent)
loc_text    = ImageDraw.Draw(img3)

warn        = Image.new('RGBA',screen_size,color=Color4.transparent)
warn_draw   = ImageDraw.Draw(warn)
warn_draw.rectangle([(10,10),warn_size],fill=None, outline=Color3.yellow)

heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
warning     = Image.open("warning.png").resize((55,50))
pad         = Image.new('RGBA', screen_size)

#initialize image overlay
pad.paste(img, hr_text_pos)
pad.paste(img2, temp_text_pos)
pad.paste(img3, loc_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
overlay = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
temperature         = 0
location            = ""
temp_thresh         = 100   # TODO
hr_thresh           = 100   # TODO
flip                = 1

heartRates = []         #list of heart rates values
HR_len = 0
location_counter = 0

#---------- setup ----------#
while(True):
    initialTime = time()    #start of sampling interval for HR
    totalSum = 0
    count = 0
    
    location_counter+=1
    location_counter%=20
    if location_counter == 0:
        location = getGPS()
    for i in range(500):
        sleep(0.001)
        currentTime = time()               #end of sampling interval for HR
        heartRate(currentTime-initialTime)
        initialTime = currentTime
        
        if spi.BPM > lowestHR and spi.BPM < highestHR:
            totalSum += spi.BPM
            count +=1
    
    heartRates.append(totalSum//[count,1][count==0]) #add newest HR, avoid zero division
    if HR_len>10: heartRates.pop(0) #throw old data
    elif HR_len<10: HR_len += 1 #increment until 10
        
    ADC_temp = ReadChannel(1)
    heartrate   = sum(heartRates)//HR_len
    try: temperature = getTemperature(ADC_temp, rref)
    except ZeroDivisionError: pass
    
    
    # clear and redraw
    temp_text.rectangle([(0,0),img_size],fill=Color4.transparent)
    temp_text.text((0,0),str(int(temperature)), font=font, fill=Color3.black)
    hr_text.rectangle([(0,0),img_size],fill=Color4.transparent)
    hr_text.text((0,0),str(int(heartrate)), font=font, fill=Color3.black)
    
    loc_text.rectangle([(0,0),img_size],fill=Color4.transparent)
    loc_text.text((0,0),location, font=font, fill=Color3.black)

    # create overlay using drawing
    if temperature > temp_thresh or heartrate > hr_thresh:
        pad.paste(warn, (0,0))
    pad.paste(img, hr_text_pos)
    pad.paste(img2, temp_text_pos)
    pad.paste(img3, loc_text_pos)
    pad.paste(thermo, thermo_pos)
    pad.paste(heart, heart_pos)
    if temperature > temp_thresh and flip:
        pad.paste(warning, (warning_x,thermo_pos[1]))
    if heartrate > hr_thresh and flip:
        pad.paste(warning, (warning_x,heart_pos[1]))
    flip = 1-flip       # makes blinking effect

    overlay_temp = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
    overlay_temp.alpha = 128
    overlay_temp.layer = 3

    # remove previous overlay
    camera.remove_overlay(overlay)
    overlay=overlay_temp

