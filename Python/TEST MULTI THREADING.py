import _thread

def imprimir_valores_velocidad():
    print('soy veloz')
    
def imprimir_valores_autonomia_corriente():
    while True:
        print('soy autonomo nashei')
    
_thread.start_new_thread(imprimir_valores_autonomia_corriente, ())
while True:
    imprimir_valores_velocidad()
    
    
