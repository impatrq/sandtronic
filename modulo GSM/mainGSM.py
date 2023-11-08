from machine import UART, Pin
import time
gsm = UART(0, baudrate=9600, rx=Pin(13), tx=Pin(12))

#uart1.read()
gsm.write('AT+CMGS="+6xxxxxxxxx68"'+'\r\n')
rcv = gsm.read()
print(rcv)
time.sleep(1)

gsm.write('HOLA'+'\r\n')
rcv = gsm.read()
print(rcv)