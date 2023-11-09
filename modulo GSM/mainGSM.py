import machine
import urequests

# Configurar UART para comunicarse con el módulo SIM800L
uart = machine.UART(0, baudrate=9600)  # Puedes necesitar ajustar el número de puerto y la velocidad.
uart.init(tx=12, rx=13)  # Ajusta los pines TX y RX según tu configuración.

# Comando AT para verificar la comunicación
uart.write("AT\r\n")
response = uart.read(100)
print(response)
# Comando AT para configurar el número de destino
uart.write('AT+CMGS="+5491128857582"\r\n')
response = uart.read(100)

# Comando AT para escribir el mensaje
uart.write("Holaa\r\n")
response = uart.read(100)

# Enviar Ctrl+Z para finalizar el mensaje
uart.write(chr(26))
response = uart.read(100)
