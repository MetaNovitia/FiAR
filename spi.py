import RPi.GPIO as GPIO
import time, sys, math

# --- SETUP --- #
CLK = 18
MISO = 23
MOSI = 24
CS = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
# --- SETUP --- #


def readAdc(channel, clkPin, misoPin, mosiPin, csPin):
    
    if channel < 0 or channel > 7:
        print("ERROR: Invalid ADC Channel number: " + str(channel))
        return -1
    
    GPIO.output(csPin, GPIO.HIGH)
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.HIGH)

    read_command = 0x18 | channel
    
    sendBits(read_command, 5, clkPin, mosiPin)
    adcValue = recvBits(12, clkPin, misoPin)
    
    GPIO.output(csPin, GPIO.HIGH)
  
    return adcValue

def sendBits(data, numBits, clkPin, mosiPin):
    
    data = data << (8 - numBits)
    
    for bit in range(numBits):
    
        if data & 0x80: GPIO.output(mosiPin, GPIO.HIGH)
    else: GPIO.output(mosiPin, GPIO.LOW)
        
    data <<= 1
        
    GPIO.output(clkPin, GPIO.HIGH)
    GPIO.output(clkPin, GPIO.LOW)

def toFarenheit(temp_c):
    return (temp_c * 9 / 5) + 32

def getTemperature(ADC_value,rref):
    #T0 = 
    temperature = 1/( (1/(273+25))+(1/(3830))*math.log(((1023/ADC_value - 1) * rref)/5000))-273
    return toFarenheit(temperature)

def recvBits(numBits, clkPin, misoPin):
    
    retVal = 0
    
    for bit in range(numBits):
    
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)
        
        if GPIO.input(misoPin): retVal |= 1
        retVal = retVal << 1

    return (retVal/2)


if __name__ == '__main__':
    try:
    
        ADC_sum = 0
        ADC_count = 0
        period = 0.1
        rref = 1000
        
        while True:
            
            ADC_value = readAdc(0, CLK, MISO, MOSI, CS)
            
            ADC_sum += ADC_value
            ADC_count += 1
            ADC_average = ADC_sum/ADC_count
            #temperature = getTemperature(ADC_value,rref)
            #avg_temperature = getTemperature(ADC_average,rref)
            
            print("ADC Result: ", str(ADC_value), " Average: ", str(ADC_average)[:5])
            #print("Temperature Result: ", str(temperature), " Temperature Average: ", str(avg_temperature)[:5])
            print()
            
            time.sleep(period)
            
    except KeyboardInterrupt:       # stop when pressing control + C
        GPIO.cleanup()
        sys.exit(0)
