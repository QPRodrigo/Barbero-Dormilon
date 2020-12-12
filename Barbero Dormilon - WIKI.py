#módulo de subprocesamiento
import threading
#Tiempo
import time

barberoListo = threading.Semaphore(0) #Mutex solo 0 y 1
sillasAccesibles = threading.Semaphore(1) #Buffer, cuadno sea 1, el numero de sillas
clientes = threading.Semaphore(0) #Numero de clientes en la sala de espera
bff=["*","*","*","*","*"] #Numero total de sillas

# acquire() y release()/P()V()
# Contador interno que es reducido por cada llamada acquire()
# Incrementado por cada llamada release().

#P suele denominarse "wait" o "espera" y la operación V "signal" o "señal".

def cliente():
    while(True):
        sillasAccesibles.acquire() #Espera la señal para poder acceder a sillasLibres.
        if len(bff)>0: #Si hay alguna silla libre, se sienta en una.
            bff.pop() #Decrementando el valor de sillasLibres en 1.
            clientes.release() #Manda señal al barbero de que hay un cliente disponible.
            print("llega un cliente")
            print(len(bff))
            sillasAccesibles.release() #Manda señal para desbloquear el acceso a sillasLibres.
            barberoListo.acquire() #El cliente espera a que el barbero esté listo para atenderlo.
            #Se le corta el pelo al cliente.
        else:
            sillasAccesibles.acquire() #Manda señal para desbloquear el acceso a sillasLibres.
            #El cliente se va de la barbería y no manda la señal de cliente disponible.
        time.sleep(1)

def barbero():
    while(True): #Bucle infinito
        clientes.acquire() #Espera la señal de un hilo cliente para despertar
        sillasAccesibles.acquire() #(Ya está despierto) Espera señal para poder modificar sillasLibres.
        bff.append('*') #Aumenta en uno el número de sillas libres.
        barberoListo.release() #El barbero está listo para cortar y manda señal al hilo cliente.
        print("Se atiende un cliente")
        print(len(bff))
        sillasAccesibles.release() #Manda señal para desbloquear el acceso a sillasLibres
        time.sleep(2)
        
def main():
    hilo1 = threading.Thread(target=barbero)
    hilo2 = threading.Thread(target=cliente)
    hilo1.start()
    hilo2.start()

main()
