

import machine
from machine import Pin, ADC, PWM
import utime
import time
def map(var, low_min, low_max, high_min, high_max):
    low_range = low_max - low_min
    per = var / low_range
    high_range = high_max - high_min
    result = high_range * per
    return int(result)
adc = ADC(28)
pwm = PWM(Pin(7)) 
pwm.freq(2500)


while (1):
    reading = adc.read_u16() - 19500
    print(adc.read_u16())
    res = map(reading,0,3.3,0,74000)
    if adc.read_u16() < 20000:
        res = 0
    print("ADC: ", res)
    utime.sleep(0.01)
    pwm.duty_u16(res)