import time
import machine

sensor_pin = machine.Pin(20, machine.Pin.IN)
pulse_count = 0

def on_pulse(pin):
    global pulse_count
    pulse_count += 1
    
    
sensor_pin.irq(trigger=machine.Pin.IRQ_RISING,handler=on_pulse)
t= machine.Timer()
t.init(period=100, mode=machine.timer.PERIODIC, callback=calculate_speed)

while True:
    
    print (pulse_count)
    print (speed)
    pwm2.duty_u16(duty)
