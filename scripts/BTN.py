import RPi.GPIO as GPIO

global usdPago, pin1Btn,pin05Btn,pin025Btn
pin1Btn=0;pin05Btn=0;pin025Btn=0
#creo un dict para guardar los pagos
usdPago={'pago':0}
act = {'opt':0};


def btn1Usd(usdPago):
    usdPago['pago'] +=1.0
    clicks=usdPago['pago']
    print('1')
    return usdPago
def btn05Usd(usdPago):
    usdPago['pago'] +=0.5
    clicks=usdPago['pago']
    print('0.5')
def btn025Usd(usdPago):
    usdPago['pago'] +=0.25
    clicks=usdPago['pago']
    print('0.25')
    return usdPago
    
def btnSalir(usdPago):
    print('Salir')
    return usdPago

def btnOpt(act):
    act['opt']+=1
    if(act['opt']>4):
        act['opt']=0
    clicks=act['opt']
    print(f'opciones: {clicks}')


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
    bouncetime=250  
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
    bouncetime=250  
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
    bouncetime=250  
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
    callback=lambda x: btnSalir(usdPago),
    # Use bouncetime to avoid extra clicks
    bouncetime=250  
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
    bouncetime=250  
)


def main():
    print("Mostrar pago cuando se presione los botones.")

    while(1):
        pass
    GPIO.cleanup()  # Clear GPIO
    pass
if __name__ == '__main__':
    main()