import machine
import time

class Velocimetro(object):
    
    def __init__(self):
        self.pulse = 0
        self.speed = 0.0
        self.diametro= 0.55 #esta en metros diametro de rueda 
        self.circunferencia= 0.55 * 3.14 #circunferencia es igual al diametro por pi
        self.relacion = 8.9 #relacion entre el moto r y rueda. cuantas veces gira el motor para que la rueda gire una vuelta
        self.cant_imanes = 4
