from machine import Pin, UART
import utime
from micropyGPS import MicropyGPS
 
# Inicializar modulo GPS
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
time_zone = -3
gps = MicropyGPS(time_zone)
 
def convert_coordinates(sections):
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
    length = gps_module.any()
    if length > 0:
        data = gps_module.read(length)
        for byte in data:
            message = gps.update(chr(byte))
 
    latitude = convert_coordinates(gps.latitude)
    longitude = convert_coordinates(gps.longitude)
 
    if latitude is None or longitude is None:
         print("Data unavailable")
         print("No coordinates")
         continue
    print('Lat: ' + latitude)
    print('Lon: ' + longitude)