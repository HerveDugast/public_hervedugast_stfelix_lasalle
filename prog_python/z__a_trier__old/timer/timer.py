import threading 
import time 
  
def MyTimer(tempo = 1.0): 
    threading.Timer(tempo, MyTimer, [tempo]).start() 
    print(time.strftime('%H:%M:%S'))
    ## Reste du traitement 
  
MyTimer(1.0)
