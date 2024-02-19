import DB
import LCD
import RPi.GPIO as GPIO
import random
import time
from time import sleep
"""Código principal 
""" 
dataB={'idAgent':'agentTran92','idSudo':'superU051','idUser':0,'llegadaHora':0,'pagoUsd':0,'placaAuto':''}
global btn1Usd, btn05Usd, btn025Usd, act, usdPago, auxHora, distanAuto
act = {'opt':1};
usdPago={'pago':0}
auxHora=0
contHora=0
distanAuto=0

# CONFIG INTERRUPCIONES
# 1usd
BUTTON_PIN = 26 
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn1Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=500  
)

#-----------------------------------------------------------
# 0.50ctvs
BUTTON_PIN = 19
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn05Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=500  
)

#--------------------------------------------------------
# 0.25ctv
BUTTON_PIN = 5
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btn025Usd(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=500  
)

#-----------------------------------------------------------
# Salir
BUTTON_PIN = 13
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btnSalir(act),
    # Use bouncetime to avoid extra clicks
    bouncetime=500 
)


#-----------------------------------------------------------
# Opciones
BUTTON_PIN = 6
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: btnOpt(act),
    # Use bouncetime to avoid extra clicks
    bouncetime=500
)


# CONFIGURO EL SENSOR ULTRASONICO ---------------------------
#set GPIO Pins
GPIO_TRIGGER = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

GPIO_ECHO = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_ECHO, GPIO.IN)


# FUNCIONES -------------------------------------------------
def btn1Usd(usdPago):
    usdPago['pago'] +=1.0
    clicks=usdPago['pago']
    DB.fireBase.upPago(usdPago['pago'])
    print(f'pago: {clicks}')

    
def btn05Usd(usdPago):
    usdPago['pago'] +=0.5
    clicks=usdPago['pago']
    DB.fireBase.upPago(usdPago['pago'])
    print(f'pago: {clicks}')

    
def btn025Usd(usdPago):
    usdPago['pago'] +=0.25
    clicks=usdPago['pago']
    DB.fireBase.upPago(usdPago['pago'])
    print(f'pago: {clicks}')


def btnSalir(act):
    act['opt']=0
    print('press Salir')
    LCD.LCD.clean()
    sleep(1)

def btnOpt(act):
    act['opt']+=1
    if(act['opt']>3):
        act['opt']=1
    clicks=act['opt']
    print(f'opciones: {clicks}')
    
def distancia():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


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


     
def horaNow():
    nowH=int(time.strftime("%H"))
    nowM=int(time.strftime("%M"))
    nowS=int(time.strftime("%S"))
    return nowH,nowM,nowS
     
def main():
    global auxHora,contHora
    initH=0; initM=0
    #-------------------------------------------------
    p=usdPago['pago']
    dist=distancia()
    distanAuto=DB.fireBase.getDistAuto()
    if(dist<=distanAuto):
        
        #Detecto el auto, entonces tomo el tiempo de registro del auto
        DB.fireBase.upHoraIn()
        initH,initM=LCD.LCD.getHora()
        #Tiempo de espera mientras reconozco
        #obtengo los valores de la camara
        detectPlaca=False
        #Aqui obtengo la matricula de los autos
        while(detectPlaca==False):
            LCD.LCD.showDetectando()
            if(act['opt']==2):
                detectPlaca==True
                nPlaca=4079
                aPlaca='GCB'
                DB.fireBase.upPlacaAuto('GCB-4079')
                break
            
        #Creo un nuevo usuario
        idU=crearUser()
        DB.fireBase.upIdUser(idU)
        #Aqui registro el pago
        while(True): #detectPlaca==True
            if(act['opt']==3):
                break
            LCD.LCD.showPlacaDetectada(idU,aPlaca,nPlaca,usdPago['pago'])
        
        #Muestro el panel de usuario 4/4
        sleep(1)
        LCD.LCD.clean()
        sleep(1)
        act['opt']=1
        while(True):
            LCD.LCD.showDataUser(idU,aPlaca,nPlaca)
            LCD.LCD.clean()
            sleep(10)
            costoH,costoM=LCD.LCD.showDataTarifa(usdPago['pago'])
            LCD.LCD.clean()
            sleep(10)
            LCD.LCD.showAutor()
            LCD.LCD.clean()
            sleep(10)
            endH,endM=LCD.LCD.getHoraEnd(initH,initM,costoH,costoM)
            nowH,nowM,nowS=horaNow()
            LCD.LCD.showContTiempo(endH,endM,nowH,nowM,nowS,initH,initM)
            LCD.LCD.clean()
            sleep(10)
                
            
        #finalizo y reinicio el sistema nuevamente    
        LCD.LCD.clean()
        sleep(1)
        #Reinicio el sistema
        auxHora=0
        contHora=0
        updateData(dataB)       
    else:
        LCD.LCD.showDisponible()
 
        
#Inicialización
LCD.LCD.clean()
updateData(dataB)
distanAuto=DB.fireBase.getDistAuto()
    
if __name__ == '__main__':
    while(True):
        main()
        
        
    """
    #detecto si aparecio un auto y se esta estacionanado 
    detectPlaca=False
    if(act['opt']>=1):
        #Obtengo los valores de la placa mediante la camara
        while(True):
            if(act['opt']==2):

                break
            LCD.LCD.showDetectando()
        #creo el nuevo usuario
        idU=crearUser()
        DB.fireBase.upIdUser(idU) 
        #Aqui debo registrar el pago ------------------------------------
        while(True): #detectPlaca==True
            sleep(1)
            if(act['opt']==3):
                break
            LCD.LCD.showPlacaDetectada(idU,aPlaca,nPlaca,usdPago['pago'])
            
        #Muestro el panel de usuario ------------------------------------
        LCD.LCD.clean()
        sleep(1)
        while(True):
            if(act['opt']==4):
                break
            pass
            #LCD.LCD.showDataUser(idU,aPlaca,nPlaca)
            #costoH,costoM=LCD.LCD.showDataTarifa(usdPago['pago'])
            #LCD.LCD.showHoraIn(initH,initM)
            #endH,endM=LCD.LCD.showHoraEnd(initH,initM,costoH,costoM)
            # Contador del tiempo restante, transformo todo a seguntos
            #contHora=1
            #while(contHora>=0):
                #nowH=int(time.strftime("%H"))
                #nowM=int(time.strftime("%M"))
                #nowS=int(time.strftime("%S"))
                #contHora=LCD.LCD.showContTiempo(endH,endM,nowH,nowM,nowS)
            #break
        #------------------------------------------------------------------------------------------------
                
    """ 