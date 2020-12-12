#módulo de subprocesamiento
import threading
#Tiempo
import time

clientes = threading.Semaphore(6) #Numero asientos vacios en la sala de espera
barberoListo = threading.Semaphore(0) #barbero Despieto o Dormido.
sillasAccesible = threading.Semaphore(1) #Buffer
#Si un esta colocando primero debe esperar a que saquen y al reves
bff=[] #Numero de clientes

# acquire() y release()/P()V()
# Contador interno que es reducido por cada llamada acquire()
# Incrementado por cada llamada release().

#P suele denominarse "wait" o "espera" y la operación V "signal" o "señal".

def cliente():
    while(True):
        barberoListo.release()
        if clientes._value <= 6 and sillasAccesible._value == 1:
            bff.append('*')
            print("LLega un cliente y espera")
            print(len(bff))
            clientes.acquire()
        #else:
        #    print("Un cliente llega y no puede esperar")
        #    print(len(bff))
        barberoListo.acquire()
        time.sleep(1)

def barbero():
    while(True):
        if clientes._value < 6:
            barberoListo.release() #Barbero Despierta   
            sillasAccesible.acquire()
            bff.pop()
            print("Un cliente se ha atendido")
            print(len(bff))
            sillasAccesible.release()
            clientes.release() #Sillas vacias incrementa
            barberoListo.acquire() #Barbero se duerme
            time.sleep(3)

def main():
    hilo1 = threading.Thread(target=cliente)
    hilo2 = threading.Thread(target=barbero)
    hilo1.start()
    hilo2.start()

main()
