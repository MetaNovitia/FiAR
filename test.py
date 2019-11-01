import RPi.GPIO as GPIO
import time
import spidev


"""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for i in range():
	GPIO.setup(i, GPIO.IN)

while True:
	GPIO.input(18)
	time.sleep(2)
"""

spi = spidev.SpiDev() 			# create spi object
spi.open(0, 0) 					# open spi port 0, device (CS) 1

spi.mode = 3

try:
	while True:
		resp = spi.readbytes(3)
		print(resp)
		time.sleep(1) 			# sleep for 0.1 seconds
 
except KeyboardInterrupt:		# Ctrl+C pressed, so
	spi.close() 				# close the port before exit
