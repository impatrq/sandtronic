import machine
import time

class Velocimetro(object):
    
    def __init__(self):
        self.pulse = 0
        self.speed = 0.0
        self.diametro= 0.55 #esta en metros diametro de rueda 
        self.circunferencia= 0.55 * 3.14 #circunferencia es igual al diametro por pi
        self.relacion = 8.9 #relacion entre el moto r y rueda. cuantas veces gira el motor para que la rueda gire una vuelta
        self.cant_imanes = 4

        self.servo_duty_0 = 8000  #menor cantidad de pulsos en la ventana de tiempo equivalente a 5km/h
        self.servo_duty_180 = 1333 #maxima cantidad de pulsos en la ventana de tiempo eqiuvalente a vel max 80km/h
        self.velocidad_max = 80
        # Ancho de pulsoz
        self.duty = self.servo_duty_0
        # pendiente de la recta pulsos(v)
        self.m = (self.servo_duty_180 - self.servo_duty_0) / self.velocidad_max 
        self.pulse_count = 0
        # GPIO para el servo de la aguja del velocimetro
       
        #aca habia un global pwm
       
        self.servo_pin = 20
        
        def iniciar(self):
        self.pwm = machine.PWM(machine.Pin(self.servo_pin))
        self.pwm.freq(50)
        # GPIO de entrada para el sensor de efecto hall
        self.sensor_pin = machine.Pin(16, machine.Pin.IN)
        self.sensor_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.on_pulse)
        # Timer para ventana de tiempo velocimetro
        self.t = machine.Timer()
        self.t.init(period=100, mode=machine.Timer.PERIODIC, callback=self.calculate_speed)