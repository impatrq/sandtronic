import classvelocimetro
ECO = 0
DRIVE = 1

class Sandtronic:
    
    VELOCIDAD_MAXIMA = 70 # Esta en km/h
   
   def __init__(self, velocidad):
        self.modo = ECO
        self.reversa = False
        self.encendido = False
        self.velocidad = 0
        self.velocidad_max = velocidad
        self.velocimetro = classvelocimetro.Velocimetro()
        
          def mostrarVelocidad(self):
        self.velocimetro.calculate_speed()
    
    def encenderMotor(self):
        self.velocidad = 0
        self.encendido = True
        
    def acelerar(self, delta): # Delta seria la variacion de velocidad
        self.velocidad += delta # self.velocidad = self.velocidad + delta
        
    def frenar(self, delta):
        self.acelerar(-delta)
        