
import time
import machine

servo_pin = 13
pwm = machine.PWM(machine.Pin(servo_pin))
pwm.freq(50)

sensor_pin = machine.Pin(26, machine.Pin.IN)
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
    speed = pulse_count * 10 / (relacion * cant_imanes) * circuferencia * 3.6
    duty = int (m * speed + servo_duty_0)
    pulse_count = 0
    print("velocidad: {:.1f} km?h" .format(speed))
    
    
def on_pulse(pin):
    global pulse_count
    pulse_count += 1
    
    
sensor_pin.irq(trigger=machine.Pin.IRQ_RISING,handler=on_pulse)
t= machine.Timer()
t.init(period=100, mode=machine.timer.PERIODIC, callback=calculate_speed)

while True:
    
    print (pulse_count)
    print (speed)
    pwm.duty_u16(duty)






















