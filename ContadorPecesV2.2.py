##import RPi.GPIO as GPIO
import multiprocessing
import numpy as np
import time
import cv2
import random as r
from multiprocessing import Lock

## FACTORES
XMIN = 0
XMAX = 350
FACTOR_PESO = 200/62500
HMIN = 80
HMAX = 165
SMIN = 0
SMAX = 260
VMIN = 0
VMAX = 260
##

def Peso_pez():
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    _,img = cap.read() ##BGR
    img = img[XMIN:XMAX,:,:]
    img_HSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([HMIN,SMIN,VMIN], dtype = "uint16")
    upper_hsv = np.array([HMAX,SMAX,VMAX], dtype = "uint16")
    mask_hsv = cv2.inRange(img_HSV,lower_hsv,upper_hsv)
    kernel = np.ones((6,6), np.uint8)
    img_d = cv2.dilate(mask_hsv, kernel)
    img_e = cv2.erode(img_d, kernel)
    img_final = img_e
    contours,_= cv2.findContours(img_final,
                                 cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        momento = cv2.moments(c)
        area = momento['m00']
        if (area>40000):
            print ('Peso: ',"{0:.2f}".format(area*FACTOR_PESO),'g')
    cap.release()
    cv2.destroyAllWindows()

def contador_1(l,contador_a,contador_b,contador_c,contador_total):
    ##DESCOMENTAR ESTO EN RASPBERRY
    ##GPIO.setmode(GPIO.BOARD)
    ##GPIO.setup(11,GPIO.IN)

    ##while (1):
    for _ in range(10):
        
##        channel = GPIO.wait_for_edge(11,GPIO.FALLING,timeout=3000) ## DESCOMENTAR EN RASPBERRY
        
        channel1 = r.randrange(2)
        if channel1 is None:
            print('Timeout')
        else :
            l.acquire()
            try:
                print('CH1',channel1)
                if channel1: ##GPIO.input(11)==0:
                    print('Translape Carril 1')
                    with contador_a.get_lock():
                        contador_a.value += 1
                print('--------------------------------')
                print('cuenta 1',contador_a.value)
                print('cuenta 2',contador_b.value)
                print('cuenta 3',contador_c.value)
                contador_total.value = contador_a.value + contador_b.value + contador_c.value
                print('cuenta total:',contador_total.value)
                print('--------------------------------')
            finally:
                l.release()
        time.sleep(0.5)
        if cv2.waitKey(30) & 0xFF == ord('q'):
          break

def contador_2(l,contador_a,contador_b,contador_c,contador_total):
    ##GPIO.setmode(GPIO.BOARD)
    ##GPIO.setup(12,GPIO.IN)
    ##while 1:
    for _ in range(10):
        
	##channel2 = GPIO.wait_for_edge(12,GPIO.FALLING,timeout=3000)

        channel2 = r.randrange(2)
        if channel2 is None:
            print('Timeout')
        else:
            l.acquire()
            try:
                print('CH2',channel2)
                if channel2:##GPIO.input(12)==0:
                    print('Translape Carril 2')
                    with contador_b.get_lock():
                        contador_b.value += 1
                print('--------------------------------')
                print('cuenta 1',contador_a.value)
                print('cuenta 2',contador_b.value)
                print('cuenta 3',contador_c.value)
                contador_total.value = contador_a.value + contador_b.value + contador_c.value
                print('cuenta total:',contador_total.value)
                print('--------------------------------')
            finally:
                l.release()
        time.sleep(0.5)
        if cv2.waitKey(30) & 0xFF == ord('q'):
          break
def contador_3(l,contador_a,contador_b,contador_c,contador_total,f):
    ##GPIO.setmode(GPIO.BOARD)
    ##GPIO.setup(12,GPIO.IN)
    ##while 1:
    for _ in range(10):
        
	##channel3 = GPIO.wait_for_edge(12,GPIO.FALLING,timeout=3000)

        channel3 = r.randrange(2)
        if channel3 is None:
            print('Timeout')
        else:
            l.acquire()
            try:
                print('CH3',channel3)
                if channel3:##GPIO.input(13)==0:
                    print('Translape Carril 3')
                    Peso_pez()
                    with contador_c.get_lock():
                        contador_c.value += 1
                    with f.get_lock():
                        f.value = 1
                print('--------------------------------')
                print('cuenta 1',contador_a.value)
                print('cuenta 2',contador_b.value)
                print('cuenta 3',contador_c.value)
                contador_total.value = contador_a.value + contador_b.value + contador_c.value
                print('cuenta total:',contador_total.value)
                print('--------------------------------')
            finally:
                l.release()
        time.sleep(0.5)
        if cv2.waitKey(30) & 0xFF == ord('q'):
          break
        
##def almacena_datos(contador_c,f):
    
    
            
if __name__ == '__main__':
    ##Crea Variables compartidas tipo 'i'=signed int
    contador_a = multiprocessing.Value('i')
    contador_b = multiprocessing.Value('i')
    contador_c = multiprocessing.Value('i')
    contador_total = multiprocessing.Value('i')
    ##Bandera de datos
    flag = multiprocessing.Value('i')
    ##Asigna valores iniciales
    contador_a.value = 0
    contador_b.value = 0
    contador_c.value = 0
    contador_total.value = 0
    flag.value = 0
    lock = Lock()

    ##CONFIGURACION GPIO
    
    #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    ##
    while (1):
        ##start = GPIO.input(channel)
        start = 1
        if start
            break
    
    print('Creo hilos')
    hilo1 = multiprocessing.Process(target=contador_1,args =(lock,contador_a,contador_b,contador_c,contador_total))
    hilo2 = multiprocessing.Process(target=contador_2,args =(lock,contador_a,contador_b,contador_c,contador_total))
    hilo3 = multiprocessing.Process(target=contador_3,args =(lock,contador_a,contador_b,contador_c,contador_total,flag))
    print('Inicio hilos')
    hilo1.start()
    hilo2.start()
    hilo3.start()
    while (1):
        
        
          break
