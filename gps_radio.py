import time
import board
import serial
import adafruit_gps

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

def getGPS():
	gps.update()
	if not gps.has_fix: return -1
	return (gps.latitude,gps.longitude)