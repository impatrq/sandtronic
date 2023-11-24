from machine import Pin, ADC
from machine import Timer 
import time

index = 1
promediominuto = 0
indexminutos = 0

adc = 0
consumo_promedio = 0

def medidor_autonomia_init():
    global adc
    # Configura el ADC
    adc = ADC(0)  # Usamos ADC(0) para el pin GP26
    tiempo1 = time.ticks_ms() #Toma tiempo actual en ms del procesador    
    