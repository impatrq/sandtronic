from machine import UART, Pin
import time
from sim800l import SIM800L

sim800l = SIM800L()
sim800l.setup()

mensaje = "hola"

sim800l.send_sms('25475491128857582', mensaje)

#gsm = UART(0, baudrate=9600, rx=Pin(13), tx=Pin(12))
#
##uart1.read()
#gsm.write("AT+CMGF=1\r") # set to text mode
#time.sleep(1)
#
#gsm.write('AT+CMGS="+5491128857582"'+'\r\n')
#rcv = gsm.read()
#print(rcv)
#time.sleep(1)
#
#gsm.write('HOLA'+'\r\n')
#rcv = gsm.read()
#print(rcv)