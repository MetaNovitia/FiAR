import time
import board
import serial
import adafruit_gps

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()

def getGPS():
	'''
					print('Latitude: {0:.6f} degree'.format(gps.latitude))
					print('Longitude: {0:6f} degrees'.format(gps.longitude))
					print('Fix quality: {}'.format(gps.fix_quality))
				
				if gps.satellites is not None:
					print('# satellites: {}'.format(gps.satellites))
				if gps.altitude_m is not None:
					print('Altitude: {} meter'.format(gps.altitude_m))
	while True:
			current = time.monotonic()
			if current - last_print >= 10.0:'''
	gps.update()
	#last_print = current
	if not gps.has_fix:
		return ('Waiting for fix...')
		#continue
	
	return ('Latitude: {0:.6f} degree'.format(gps.latitude) + '\n' +
			'Longitude: {0:6f} degrees'.format(gps.longitude))
					
				
