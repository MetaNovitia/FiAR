import RPi.GPIO as GPIO
import time, math
import sys

CLK = 18
MISO = 23
MOSI = 24
CS = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def setupSpiPins(clkPin, misoPin, mosiPin, csPin):
    ''' Set all pins as an output except MISO (Master Input, Slave Output)'''
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(misoPin, GPIO.IN)
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)
     

def readAdc(channel, clkPin, misoPin, mosiPin, csPin):
    if (channel < 0) or (channel > 7):
        print("Invalid ADC Channel number, must be between [0,7]")
        return -1
        
    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(csPin, GPIO.HIGH)
    
    # Start the read with both clock and chip select low
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.HIGH)
    
    # read command is:
    # start bit = 1
    # single-ended comparison = 1 (vs. pseudo-differential)
    # channel num bit 2
    # channel num bit 1
    # channel num bit 0 (LSB)
    read_command = 0x18
    read_command |= channel
    
    sendBits(read_command, 5, clkPin, mosiPin)
    
    adcValue = recvBits(12, clkPin, misoPin)
    
    # Set chip select high to end the read
    GPIO.output(csPin, GPIO.HIGH)
  
    return adcValue
    
def sendBits(data, numBits, clkPin, mosiPin):
    ''' Sends 1 Byte or less of data'''
    
    data <<= (8 - numBits)
    
    for bit in range(numBits):
        # Set RPi's output bit high or low depending on highest bit of data field
        if data & 0x80:
            GPIO.output(mosiPin, GPIO.HIGH)
        else:
            GPIO.output(mosiPin, GPIO.LOW)
        
        # Advance data to the next bit
        data <<= 1
        
        # Pulse the clock pin HIGH then immediately low
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)

def recvBits(numBits, clkPin, misoPin):
    '''Receives arbitrary number of bits'''
    retVal = 0
    
    for bit in range(numBits):
        # Pulse clock pin 
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)
        
        # Read 1 data bit in
        if GPIO.input(misoPin):
            retVal |= 0x1
        
        # Advance input to next bit
        retVal <<= 1
    
    # Divide by two to drop the NULL bit
    return (retVal/2)

def toFarenheit(temp_c):
    return (temp_c * 9 / 5) + 32

def getTemperature(ADC_value,rref):
    #T0 = 
    temperature = 1/( (1/(273+25))+(1/(3830))*math.log(((1023/ADC_value - 1) * rref)/5000))-273
    return toFarenheit(temperature)


if __name__ == '__main__':
    try:
    
        ADC_sum = 0
        ADC_count = 0
        period = 0.1
        rref = 1000
        
        setupSpiPins(CLK, MISO, MOSI, CS)
        
        while True:
            
            ADC_value = readAdc(0, CLK, MISO, MOSI, CS)
            
            ADC_sum += ADC_value
            ADC_count += 1
            ADC_average = ADC_sum/ADC_count
            temperature = getTemperature(ADC_value,rref)
            avg_temperature = getTemperature(ADC_average,rref)
            
            print("ADC Result: ", str(ADC_value), " Average: ", str(ADC_average)[:5])
            print("Temperature Result: ", str(temperature), " Temperature Average: ", str(avg_temperature)[:5])
            print()
            
            time.sleep(period)
            
    except KeyboardInterrupt:       # stop when pressing control + C
        GPIO.cleanup()
        sys.exit(0)
