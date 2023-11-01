import DB
import LCD
import RPi.GPIO as GPIO
import random
import time
from time import sleep 
"""Código principal 
""" 
dataB={'idAgent':'agentTran92','idSudo':'superU051','idUser':0,'llegadaHora':0,'pagoUsd':0,'placaAuto':''} 
global btn1Usd, act, contPago, btn05Usd, btn025Usd, usdPago, auxHora, contHora
act = {'opt':0};
usdPago={'pago':0}
auxHora=1
contHora=0
contPago = 5*60 #10 minutos

#Configuracion interrupciones (botones)
#configuro pin 37
BUTTON_PIN = 37  
# Set GPIO mode to BOARD to use pin numbers
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn1Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=250  
)

#-----------------------------------------------------------
#configuro pin 35
BUTTON_PIN = 35
# Set GPIO mode to BOARD to use pin numbers
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn05Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=250  
)

#-----------------------------------------------------------
#configuro pin 33
BUTTON_PIN = 33
# Set GPIO mode to BOARD to use pin numbers
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn025Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=250  
)

#-----------------------------------------------------------
#configuro pin 31
BUTTON_PIN = 31
# Set GPIO mode to BOARD to use pin numbers
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: status(act),
    # Use bouncetime to avoid extra clicks
    bouncetime=250  
)



def btn1Usd(usdPago):
    usdPago['pago'] +=1.0
    clicks=usdPago['pago']
    #LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    #sleep(2)
    #LCD.LCD.clean()
    #sleep(2)
    
def btn05Usd(usdPago):
    usdPago['pago'] +=0.5
    clicks=usdPago['pago']
    #LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    #sleep(2)
    #LCD.LCD.clean()
    #sleep(2)
    
def btn025Usd(usdPago):
    usdPago['pago'] +=0.25
    clicks=usdPago['pago']
    #LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    #sleep(2)
    #LCD.LCD.clean()
    #sleep(2)

def status(act):
    act['opt']+=1
    if(act['opt']>4):
        act['opt']=0
    clicks=act['opt']
    print(f'opciones: {clicks}')


def updateData(db): 
    DB.fireBase.upIdAgent(db['idAgent']) 
    DB.fireBase.upIdSudo(db['idSudo']) 
    DB.fireBase.upIdUser(db['idUser']) 
    DB.fireBase.upPago(db['pagoUsd']) 
    DB.fireBase.upPlacaAuto(db['placaAuto']) 
 
def crearUser(): 
    user=random.randint(100, 999) 
    print(f'Codigo de Usuario: {user}') 
    return user

def contPagoMin(contPago): 
    contPagoM=int(contPago/60) 
    contPagoS=int(contPago-contPagoM*60) 
    contPago=contPago-1 
    sleep(1) 
    #print(f'tiempo: {contPagoM} : {contPagoS}') 
    return contPago,contPagoM,contPagoS 
     
     
def main():
    global auxHora,contHora
    initH=0; initM=0
    #-------------------------------------------------
    LCD.LCD.showDisponible()
    #detecto si aparecio un auto y se esta estacionanado 
    detectPlaca=False
    if(act['opt']>=1):
        if(auxHora==1):
            initH,initM=LCD.LCD.getHora()
            auxHora+=1
        
        #Actualizo todos los datos
        print('Actualizando datos ')
        #updateData(dataB) 
        #Obtengo los valores de la placa mediante la camara
        while(True):
            if(act['opt']==2):
                #Aqui debo registrar la placa y el reconocimiento de la misma con Open CV
                detectPlaca==True
                nPlaca=123
                aPlaca='ABR'
                break
            LCD.LCD.showDetectando()
        #creo el nuevo usuario
        idU=crearUser()
        while(True): #detectPlaca==True
            sleep(1)
            if(act['opt']==3):
                #Aqui debo registrar el pago
                break
            LCD.LCD.showPlacaDetectada(idU,aPlaca,nPlaca,usdPago['pago'])
            
        #Muestro el panel de usuario
        LCD.LCD.clean()
        sleep(1)
        while(True):
            if(act['opt']==4):
                break
            
            LCD.LCD.showPlaca(aPlaca,nPlaca)
            costoH,costoM=LCD.LCD.showTarifa(usdPago['pago'])
            LCD.LCD.showHora(initH,initM)
            # Contador del tiempo restante, transformo todo a seguntos
            contHora=costoH*3600+costoM*60
            while(contHora>=0):
                contHora-=1
                sleep(1)
                contH,contM,contS=LCD.LCD.contTiempo(contHora)
            break
        #------------------------------------------------------------------------------------------------
                
            
        LCD.LCD.clean()
        sleep(1)
        #Reinicio el sistema
        auxHora=0
        contHora=0
                
    else:
        LCD.LCD.showDisponible()
    
    
 
        

    
    
if __name__ == '__main__':
    while(1):
        main()
        