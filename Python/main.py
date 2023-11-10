import machine
import utime
import time
import ads1115
import _thread
from machine import Pin, I2C, PWM


### parametros dedicados del pwm estator 

def map(var, low_min, low_max, high_min, high_max):
    low_range = low_max - low_min
    per = var / low_range
    high_range = high_max - high_min
    result = high_range * per
    return int(result)

pwm1 = PWM(Pin(22)) # pwm del estator
pwm1.freq(2800)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) # direc i2c del adc externo
adc = ads1115.ADS1115(i2c, 72, 0) # adc externo

### parametros y funciones dedicados del velocimetro

servo_pin = 13

pwm2 = machine.PWM(machine.Pin(servo_pin))
pwm2.freq(50)

sensor_pin = machine.Pin(20, machine.Pin.IN)

pulse_count = 0
speed = 0.0
diametro= 0.55
circunferencia= 0.55 * 3.14
relacion = 8.9
cant_imanes = 4


servo_duty_0 = 8000
servo_duty_180 = 1333

duty = servo_duty_0

m = (1333-8000) / 80

def calculate_speed(t):
    global pulse_count, speed, duty
    speed = pulse_count * 10 / (relacion * cant_imanes) * circunferencia * 3.6
    duty = int (m * speed + servo_duty_0)
    pulse_count = 0
    print("velocidad: {:.1f} km?h" .format(speed))
    
    
def on_pulse(pin):
    global pulse_count
    pulse_count += 1

###

def pwm_stator():

    value = adc.raw_to_v(adc.read(7,1))
    reading = value
    res = map(reading,0,3.3,0,84000)
    if value < 1:
        res = 19500
    print("ADC: ", value)
    print("PWM: ", res )
    pwm1.duty_u16(res - 19500)
    utime.sleep(0.05)

def velocimetro():
    print (pulse_count)
    print (speed)
    pwm2.duty_u16(duty)

def main():
    while True: 
        try: # safeguard por si se llena la queue de threads, evito crasheos
            _thread.start_new_thread(pwm_stator)
        except:
            pass
        try:
            _thread.start_new_thread(velocimetro)
        except:
            pass

main()