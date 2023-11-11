import machine
import utime
import time
import ads1115
import _thread
from machine import Pin, I2C, PWM

### parametros dedicados del pwm rotor 

### multithread para separar el velocímetro del código del acelerador

#print("HOLA")
pin_encendido = Pin(7, Pin.IN, Pin.PULL_DOWN)
pin_a1_reversa = Pin(9, Pin.IN, Pin.PULL_DOWN)
pin_reversa = Pin(21, Pin.OUT)
#pin_led = Pin(12, Pin.OUT)
boton_presionado = None

class rotor(): 
    def __init__(self):               
        self.pwm = PWM(Pin(22)) # pwm del rotor
        self.pwm.freq(2800)

        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) # direc i2c del adc externo - sensa señal del acelerador 
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

        self.pwm = PWM(Pin(self.servo_pin))
        self.pwm.freq(50)

        self.sensor = Pin(self.sensor_pin, Pin.IN) # sensor de pulsos de motor

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

def pwm_rotor():
    while True:
        if pin_a1_reversa.value() == 1:
            pin_reversa.value(1)
        else:
            pin_reversa.value(0)
        value = rotor.adc.raw_to_v(rotor.adc.read(7,1))
        reading = value
        res = rotor.map(reading,0,3.3,0,84000)
        if value < 1:
            res = 19500
        print("ADC: ", value)
        print("PWM: ", res )
        rotor.pwm.duty_u16(res - 19500)
        utime.sleep(0.05)

def velocimetro():
    velocimeter.sensor_pin.irq(trigger=machine.Pin.IRQ_RISING,handler=velocimeter.on_pulse)
    t= machine.Timer()
    t.init(period=100, mode=machine.timer.PERIODIC, callback=velocimeter.calculate_speed)

    while True:       
        print(velocimeter.calculate_speed())
        print(velocimeter.on_pulse())
        velocimeter.pwm.duty_u16(velocimeter.duty)

def main():
    print("Start main")
    global rotor
    global velocimeter
    rotor = rotor()
    velocimeter = velocimeter()
    _thread.start_new_thread(pwm_rotor, ())
    velocimetro()
    # safeguard por si se llena la queue de threads, evito crasheos

def boton_encendido():
    global pin_encendido
    #global pin_led
    global boton_presionado
    if pin_encendido.value() == 1:
        if boton_presionado is None:
            boton_presionado = time.ticks_ms()
        else:
            if time.ticks_diff(time.ticks_ms(), boton_presionado) > 2000:
                print("Encendido.")
                #pin_led.value(1)
                main()        
    else:
        print("El botón está en posición de apagado.")
        return

while True:
    #print("Test")
    if pin_encendido.value() == 1:
        print("Encendiendo . . .")
        boton_encendido()

