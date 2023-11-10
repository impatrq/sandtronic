from machine import Pin, UART
import utime
import time
import _thread
from micropyGPS import MicropyGPS

destno = "Número en formato +xxxxxxxxxxx"
msg = "Mensaje, sobreescrito por el loop del programa"

class sim():
        
    def __init__(self):
        self.uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))  

        #self.destno = destno
        #self.msg = msg

        self.uart.write('ATE0\n')         # command echo off
        self.uart.write('AT+CRSL=99\n')   # ringer level
        self.uart.write('AT+CMIC=0,10\n') # microphone gain
        self.uart.write('AT+CLIP=1\n')    # caller line identification
        self.uart.write('AT+CMGF=1\n')    # plain text SMS
        self.uart.write('AT+CALS=3,0\n')  # set ringtone
        self.uart.write('AT+CLTS=1\n')    # enabke get local timestamp mode
        self.uart.write('AT+CSCLK=0\n')   # disable automatic sleep

    def send_sms(self, phone_number, message):
        # activa modo sms
        self.uart.write('AT+CMGF=1\r\n')
        time.sleep(1)
        response = self.uart.read().decode('utf-8')
        print(response)
        
        if "OK" not in response:
            print("Fallo al establecer modo texto.")
            return

        # setea número
        self.uart.write(f'AT+CMGS="{phone_number}"\r\n')
        time.sleep(1)
        response = self.uart.read().decode('utf-8')
        print(response)

        if ">" not in response:
            print("Fallo al establecer número de destino.")
            return

        # envía el mensaje
        self.uart.write('{}\r\n'.format(message))
        time.sleep(1)

        # envía ctrl z para finalizar el envío
        self.uart.write('\x1A')
        time.sleep(1)

        # espera al envío de mensaje
        response = self.uart.read().decode('utf-8')
        print(response)

        if "OK" not in response:
            print("Fallo al enviar SMS.")
        else:
            print("SMS enviado con éxito.")


class gps():

    def __init__(self): # Inicializar modulo GPS
        self.gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
        time_zone = -3
        self.gps = MicropyGPS(time_zone)
    
    def convert_coordinates(self, sections):
        if sections[0] == 0:  # sections[0] contains the degrees
            return None
    
        # sections[1] contains the minutes
        data = sections[0] + (sections[1] / 60.0)
    
        # sections[2] contains 'E', 'W', 'N', 'S'
        if sections[2] == 'S':
            data = -data
        if sections[2] == 'W':
            data = -data
    
        data = '{0:.6f}'.format(data)  # 6 decimal places
        return str(data)
 
while True:
    length = gps.gps_module.any()
    if length > 0:
        data = gps.gps_module.read(length)
        for byte in data:
            message = gps.update(chr(byte))
 
    latitude = gps.convert_coordinates(gps.latitude)
    longitude = gps.convert_coordinates(gps.longitude)
 
    if latitude is None or longitude is None:
         print("Data no disponible")
         print("No hay coordenadas")
         continue
    print('Lat: ' + latitude)
    print('Lon: ' + longitude)
    msg = ('Lat: ' + latitude + " Lon: " + longitude)
    sim.send_sms(destno, msg)