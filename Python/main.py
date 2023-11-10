import machine
import utime
import time
import ads1115
import _thread
from machine import Pin, I2C, PWM


### parametros dedicados del pwm estator 

class stator(): 
    def __init__(self):               
        self.pwm1 = PWM(Pin(22)) # pwm del estator
        self.pwm1.freq(2800)

        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) # direc i2c del adc externo
        self.adc = ads1115.ADS1115(self.i2c, 72, 0) # adc externo

    def map(self, var, low_min, low_max, high_min, high_max):
        low_range = low_max - low_min
        per = var / low_range
        high_range = high_max - high_min
        result = high_range * per
        return int(result)


### parametros y funciones dedicados del velocimetro

class velocimeter():
    def __init__(self):   
        self.servo_pin = 13 # Pin del servo del velocimetro
        self.sensor_pin = 20 # Pin del sensor 

        self.pwm2 = machine.PWM(machine.Pin(self.servo_pin))
        self.pwm2.freq(50)

        self.sensor = machine.Pin(self.sensor_pin, machine.Pin.IN) # sensor de pulsos de motor

        self.pulse_count = 0
        self.speed = 0.0
        self.diametro= 0.55
        self.circunferencia= 0.55 * 3.14
        self.relacion = 8.9
        self.cant_imanes = 4

        self.servo_duty_0 = 8000
        self.servo_duty_180 = 1333

        self.duty = self.servo_duty_0

        self.m = (1333-8000) / 80

    def calculate_speed(self):
        #global pulse_count, speed, duty
        self.speed = self.pulse_count * 10 / (self.relacion * self.cant_imanes) * self.circunferencia * 3.6
        self.duty = int (self.m * self.speed + self.servo_duty_0)
        self.pulse_count = 0
        self.speed_str = "velocidad: {:.1f} km?h" .format(self.speed)
        return self.speed_str

    def on_pulse(self):
        #global pulse_count
        self.pulse_count += 1
        return self.pulse_count

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
    print(calculate_speed())
    print (on_pulse())
    pwm2.duty_u16(duty)

def main():
    stator_setup()
    velocimeter_setup()
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