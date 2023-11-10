from machine import UART, Pin
from sim800l import SIM800L
#import urequests

uartno = 0
baudrate = 9600

destno = "+5491154637770"
msg = "HOLA"

sim800l = SIM800L(uartno)

# Configurar UART para comunicarse con el módulo SIM800L
#uart = machine.UART(0, baudrate=9600)  # Puedes necesitar ajustar el número de puerto y la velocidad.
#uart.init(tx=Pin(12), rx=Pin(13))  # Ajusta los pines TX y RX según tu configuración.

sim800l.setup()
print(sim800l.network_name())
# sim800l.test()
sim800l.send_sms(destno, msg)

