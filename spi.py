import time, math
import sys
import spidev

#set up for SPI
spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz = 1000000


# Setup for heartrate variables
BPM = 0
IBI = 600                  # 600ms per beat = 100 Beats Per Minute (BPM)
Pulse = False
sampleCounter = 0
lastBeatTime = 0
P = 512                    # peak at 1/2 the input range of 0..1023
T = 512                    # trough at 1/2 the input range.
thresh = 550               # threshold a little above the trough
threshSetting = 550
amp = 100                  # beat amplitude 1/10 of input range.
firstBeat = True           # looking for the first beat
secondBeat = False         # not yet looking for the second beat in a row


def ReadChannel(channel):
    ''' Read input at ADC channel
    @param channel: channel of ADC to read
    @return: processed digital data
    
    channel 0: heart rate sensor
    channel 1: thermistor
    '''

    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]

    return data

def heartRate(sampleInterval):
    ''' Processes digital data from function ReadChannel(),
    creates heart rate info, and then outputs to global
    var BPM

    '''
    global BPM, IBI, Pulse, sampleCounter, lastBeatTime
    global P, T, thresh, amp, firstBeat, secondBeat, threshSetting

    Signal = ReadChannel(0)
    sampleCounter += sampleInterval*1000        # keep track of the time in mS with this variable
    N = int(sampleCounter - lastBeatTime)    # monitor the time since the last beat to avoid noise

    #  find the peak and trough of the pulse wave
    if (Signal < thresh and N > (IBI / 5) * 3) : # avoid dichrotic noise by waiting 3/5 of last IBI
        if (Signal < T) :                         
            T = Signal                            

    if (Signal > thresh and Signal > P) :       # thresh condition helps avoid noise
        P = Signal                              

    if (N > 250):                            # avoid high frequency noise
        if ( (Signal > thresh) and (Pulse == False) and (N > (IBI / 5) * 3) ):
            Pulse = True                          
            IBI = int(sampleCounter - lastBeatTime)    # measure time between beats in mS
            lastBeatTime = sampleCounter          # keep track of time for next pulse

            if (secondBeat) :                      
                secondBeat = False                 

            if (firstBeat) :                  
                firstBeat = False                   
                secondBeat = True                  
            # IBI value is unreliable so discard it
                return
            
            BPM = 60000 / IBI

    if (Signal < thresh and Pulse == True):
        Pulse = False
        amp = P - T
        thresh = amp / 2 + T
        P = thresh
        T = thresh
        
    if (N > 2500):
        thresh = threshSetting
        P = 512
        T = 512
        lastBeatTime = sampleCounter
        firstBeat = True
        secondBeat = False
        BPM = 0
        IBI = 600
        Pulse = False
        amp = 0

def toFahrenheit(temp_c):
    ''' Returns temperature as Fahrenheit
    @param temp_c: temperature in Celcius
    @return: temperature in Fahrenheit
    '''
    return (temp_c * 9 / 5) + 32

def getTemperature(ADC_value,rref = 1000):
    ''' Converts ADC temperature value into degrees Fahrenheit
    @param ADC_value: digital value from ADC
    @param rref: reference resistance value (default value: 1000)
    @return: temperature in degrees Fahrenheit
    '''
    temperature = 1/( (1/(273+25))+(1/(3434))*math.log(((1023/ADC_value - 1) * rref)/5000))-273
    return toFahrenheit(temperature)


if __name__ == '__main__':
    try:

        ADC_sum = 0
        ADC_count = 0
        period = 0.1
        rref = 1000
        
        while True:
            
            ADC_value = ReadChannel(0)
            
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
        sys.exit(0)
