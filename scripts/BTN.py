import RPi.GPIO as GPIO

global usdPago, pin1Btn,pin05Btn,pin025Btn
pin1Btn=0;pin05Btn=0;pin025Btn=0
#creo un dict para guardar los pagos
usdPago={'pago':0}

class BTN(object):
    def btn1Usd(usdPago):
        usdPago['pago'] +=1.0
        clicks=usdPago['pago']
        print(f'pago: {clicks}')
        return usdPago
    def btn05Usd(usdPago):
        usdPago['pago'] +=0.5
        clicks=usdPago['pago']
        print(f'pago: {clicks}')
    def btn025Usd(usdPago):
        usdPago['pago'] +=0.25
        clicks=usdPago['pago']
        print(f'pago: {clicks}')
        return usdPago


def button_pressed(usdPago):
    usdPago += 1

#configuro pin 37
BUTTON_PIN = 37  
# Set GPIO mode to BOARD to use pin numbers
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
# Detect button event on rising edge
GPIO.add_event_detect(  
    BUTTON_PIN, GPIO.RISING,
    # Use lambda to pass parameters
    callback=lambda x: BTN.btn1Usd(usdPago),
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
    callback=lambda x: BTN.btn05Usd(usdPago),
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
    callback=lambda x: BTN.btn025Usd(usdPago),
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