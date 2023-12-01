from machine import UART, Pin 
import time

uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))  

destno = "+5491154637770"
msg = "HOLA"


uart.write('ATE0\n')         # command echo off
time.sleep(1)
print(uart.read())
uart.write('AT+CRSL=99\n')   # ringer level
time.sleep(1)
print(uart.read())
uart.write('AT+CMIC=0,10\n') # microphone gain
time.sleep(1)
print(uart.read())
uart.write('AT+CLIP=1\n')    # caller line identification
time.sleep(1)
print(uart.read())
uart.write('AT+CMGF=1\n')    # plain text SMS
time.sleep(1)
print(uart.read())
uart.write('AT+CALS=3,0\n')  # set ringtone
time.sleep(1)
print(uart.read())
uart.write('AT+CLTS=1\n')    # enabke get local timestamp mode
time.sleep(1)
print(uart.read())
uart.write('AT+CSCLK=0\n')   # disable automatic sleep
time.sleep(1)
print(uart.read())

def send_sms(phone_number, message):
    # activa modo sms
    uart.write('AT+CMGF=1\n')
    time.sleep(1)
    response = uart.read().decode('utf-8')
    print(response)
    
    if "OK" not in response:
        print("Fallo al establecer modo texto.")
        return

    # setea número
    uart.write(f'AT+CMGS="{phone_number}"\n')
    time.sleep(1)
    response = uart.read().decode('utf-8')
    print(response)

    if ">" not in response:
        print("Fallo al establecer número de destino.")
        return

    # envía el mensaje
    uart.write('{}\n'.format(message))
    time.sleep(1)

    # envía ctrl z para finalizar el envío
    uart.write('\x1A')
    time.sleep(1)

    # espera al envío de mensaje
    response = uart.read().decode('utf-8')
    print(response)

    if "OK" not in response:
        print("Fallo al enviar SMS.")
    else:
        print("SMS enviado con éxito.")

send_sms(destno, msg)