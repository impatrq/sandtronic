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
    
    def medir_autonomia():
    global consumo_promedio
    
    if index == 0:
        consumo_promedio = 0
    # Lee el valor del ADC
    valor_adc = adc.read_u16()  # Lee el valor del ADC en formato de 16 bits
    # Convierte el valor del ADC a voltaje
    voltaje = valor_adc * 3.3 / 65535  # 65535 es el valor máximo de ADC en 16 bits, 3.3 es la referencia de voltaje
     corriente = voltaje / (15 * 0.00025) #a partir de voltaje medido en el adc se saca la corriente 
    consumo_promedio += corriente 
    index += 1
       
    tiempo2 = time.ticks_ms()
    
    if (tiempo2 - tiempo1)/1000 >= 60:
        consumo_promedio = consumo_promedio / index
        index = 0
        tiempo1 = time.ticks_ms()
        return consumo_promedio 
    
    