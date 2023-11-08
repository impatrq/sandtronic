from machine import UART, Pin
uart1 = UART(1, baudrate=9600, rx=Pin(13), tx=Pin(12))

#uart1.read()