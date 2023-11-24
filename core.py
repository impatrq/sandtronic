# Desde el velocimetro
from pps import pwm, duty, velocimetro_init
# Desde el medidor de autonomia
from autonomia import medidor_autonomia_init, medir_autonomia

def core_1():
    # Inicializo todo lo necesario para la autonomia
    medidor_autonomia_init()
    consumo_promedio = medir_autonomia()
    
    if consumo_promedio != None:
        print("Consumo promedio %.2f" % consumo_promedio)