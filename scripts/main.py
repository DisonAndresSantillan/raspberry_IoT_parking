import DB
import LCD
import RPi.GPIO as GPIO
import random 
from time import sleep 
"""Código principal 
""" 
dataB={'idAgent':'agentTran92','idSudo':'superU051','idUser':0,'llegadaHora':0,'pagoUsd':0,'placaAuto':''} 
global btn1Usd, act, contPago, btn05Usd, btn025Usd, usdPago, contDetectPlaca
act = 0;
usdPago={'pago':0}
contDetectPlaca=1*30
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



def btn1Usd(usdPago):
    usdPago['pago'] +=1.0
    clicks=usdPago['pago']
    LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    sleep(1)
    LCD.LCD.clean()
    sleep(2)
    
def btn05Usd(usdPago):
    usdPago['pago'] +=0.5
    clicks=usdPago['pago']
    LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    sleep(2)
    LCD.LCD.clean()
    sleep(2)
    
def btn025Usd(usdPago):
    usdPago['pago'] +=0.25
    clicks=usdPago['pago']
    LCD.LCD.showPago(usdPago)
    print(f'pago: {clicks}')
    sleep(1)
    LCD.LCD.clean()
    sleep(2)

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
     
     
if __name__ == '__main__': 
    #Actualizo todos los datos 
    updateData(dataB) 
    #crear un usuario 
    #-------------------------------------------------
    
    LCD.LCD.showDisponible()
    #detecto si aparecio un auto y se esta estacionanado 
    accion=input('placa detectada (si/no): ')
    detectPlaca=False
    if(accion=='si'):
        LCD.LCD.showDetectando()
        #Obtengo los valores de la placa mediante la camara
        while(detectPlaca==False):
            LCD.LCD.showDetectando()
            #Aqui debo registrar la placa y el reconocimiento de la misma con Open CV
            contDetectPlaca-=1
            sleep(1)
            print(contDetectPlaca)
            if(contDetectPlaca<=0):
                detectPlaca=True
                #Creo el usuario y lo cuardo en la base de datos 
                idU=crearUser()
                sleep(2)
                LCD.LCD.showplacaDetectada(idU,'ABC',123)
                
    else:
        LCD.LCD.showDisponible()
        
    p=usdPago['pago']
    print(f'El pago es: {p}')
        
    """
        print('placa detectada: ABC-123') 
        idU=crearUser() 
        placa='ABC-123' 
        #DB.fireBase.upIdUser(idU) 
        #DB.fireBase.upPlacaAuto(placa) 
        #DB.fireBase.upHoraIn() 
        while(contPago>=0): 
            contPago,contM,contS=contPagoMin(contPago) 
            if(contM>=2): 
                print('placa registrada, tiene 5 minutos') 
                print('para realizar el pago') 
            else: 
                print('Notificando Agente de transito cercano') 
            if(btn1Usd==1): 
                pagoUsd+=1 
            elif(btn05Usd==1): 
                pagoUsd+=0.50 
            elif(btn025Usd==1): 
                pagoUsd+=0.25 
            print(f'tiempo: {contM} : {contS}') 
        else:
           pass
    """ 
             
    """ 
    btn=int(input('ingresa un comando: ')) 
    if(btn==1): 
        print('----------------') 
        print('realizar pago:') 
        print 
    """