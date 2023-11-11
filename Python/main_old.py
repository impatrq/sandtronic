import machine
import utime
import time
import ads1115
def map(var, low_min, low_max, high_min, high_max):
    low_range = low_max - low_min
    per = var / low_range
    high_range = high_max - high_min
    result = high_range * per
    return int(result)

from machine import Pin,I2C, PWM
pwm = PWM(Pin(22))
pwm.freq(2800)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
adc = ads1115.ADS1115(i2c, 72, 0)
while (1):
    value = adc.raw_to_v(adc.read(7,1))
    reading = value
    
    res = map(reading,0,3.3,0,84000)
    if value < 1:
        res = 19500
    print("ADC: ", value)
    print("PWM: ", res )
    pwm.duty_u16(res - 19500)
    utime.sleep(0.05)

    
