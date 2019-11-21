import picamera
import spi
from spi import ReadChannel, getTemperature, heartRate
from PIL import Image, ImageDraw, ImageFont
from time import sleep,time
from colors import Color3, Color4
import random

#---------- setup ----------#
rref    = 1000                 #reference resistance value 
lowestHR = 40
highestHR = 200

img_size        = (500,90)     
screen_size     = (1280,720)
temp_text_pos   = (1050,500)
hr_text_pos     = (1050,580)
heart_pos       = (980,510)
thermo_pos      = (980,590)
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


heart       = Image.open("heart.png").resize((50,50))
thermo      = Image.open("thermo.png").resize((50,50))
pad         = Image.new('RGBA', screen_size)

#initialize image overlay
pad.paste(img, hr_text_pos)
pad.paste(img2, temp_text_pos)
pad.paste(heart, heart_pos)
pad.paste(thermo, thermo_pos)
overlay = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
temperature = 0

heartRates = []         #list of heart rates values
HR_len = 0
#---------- setup ----------#

while(True):
    initialTime = time()    #start of sampling interval for HR
    totalSum = 0
    count = 0
    
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

    # create overlay using drawing
    pad.paste(img, hr_text_pos)
    pad.paste(img2, temp_text_pos)
    pad.paste(thermo, thermo_pos)
    pad.paste(heart, heart_pos)

    overlay_temp = camera.add_overlay(pad.tobytes(),format="rgba",size=pad.size)
    overlay_temp.alpha = 128
    overlay_temp.layer = 3

    # remove previous overlay
    camera.remove_overlay(overlay)
    overlay=overlay_temp
