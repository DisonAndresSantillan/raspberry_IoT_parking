import time
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
"""
Este es el codigo principal para el funcionamiento
del LCD
"""

global cont,initH,initM
cont = 0
initH = 0
initM = 0

# limpio el LCD
lcd.clear()
lcd.home()
placaUno = (
  0b00011,
  0b00110,
  0b01110,
  0b11000,
  0b10000,
  0b11111,
  0b10100,
  0b11100
    )
placaMitad = (
  0b11111,
  0b01110,
  0b00000,
  0b00000,
  0b00000,
  0b11111,
  0b01110,
  0b00000
    )
placaDos = (
  0b11000,
  0b01100,
  0b00110,
  0b00011,
  0b00001,
  0b11111,
  0b00101,
  0b00111
    )
placaTres = (
  0b00001,
  0b01110,
  0b10000,
  0b01110,
  0b00001,
  0b01110,
  0b10000,
  0b00000
    )

horaInitUno = (
  0b01111,
  0b10000,
  0b10000,
  0b10000,
  0b10000,
  0b10000,
  0b10000,
  0b01111

)
horaInitMitad = (
  0b11111,
  0b00100,
  0b00100,
  0b00100,
  0b00111,
  0b00000,
  0b00000,
  0b11111
    )
horaInitDos = (
  0b11110,
  0b00001,
  0b00001,
  0b00001,
  0b11111,
  0b00001,
  0b00001,
  0b11110
    )
costoHora = (
  0b01010,
  0b11111,
  0b11010,
  0b11010,
  0b11111,
  0b01011,
  0b11111,
  0b01010
    )
horaEnd = (
  0b01110,
  0b10001,
  0b10001,
  0b10011,
  0b10101,
  0b10101,
  0b10101,
  0b01110
)

framebuffer = [
        '',
        '',
        ]
class LCD(object):
    
    def write_to_lcd(lcd, framebuffer, num_cols):
        lcd.home()
        for row in framebuffer:
            lcd.cursor_pos = (0, 7)
            lcd.write_string('TESIS:')
            lcd.cursor_pos=(1,0)
            lcd.write_string(row.ljust(num_cols)[:num_cols])
            lcd.write_string('\r\n')
    def long_text(text):
        if len(text)<20:
            lcd.write_string(text)      
        for i in range(len(text) - 20 + 1):
            framebuffer[1] = text[i:i+20]
            LCD.write_to_lcd(lcd, framebuffer, 20)
            sleep(0.4)
    def showDataUser(idU,abc,num):
        lcd.cursor_pos = (0, 2)
        lcd.write_string(f'DATOS DE USUARIO:')
        lcd.cursor_pos = (1, 6)
        lcd.write_string(f'ID:   {idU}')
        lcd.cursor_pos = (2, 2)
        lcd.write_string(f' Placa: {abc}-{num}')
        lcd.cursor_pos = (3, 8)
        lcd.create_char(1, placaUno)
        lcd.write_string('\x01')
        lcd.create_char(2, placaMitad)
        lcd.write_string('\x02')
        lcd.create_char(3, placaDos)
        lcd.write_string('\x03')
        lcd.create_char(4, placaTres)
        lcd.write_string('\x04')
        lcd.cursor_pos = (3, 17)
        lcd.write_string('1/4')
        
    def showPlacaDetectada(user,abc,num,pago):
        lcd.create_char(4, placaTres)
        lcd.cursor_pos = (1, 0)
        lcd.create_char(1, placaUno)
        lcd.write_string('\x01')
        lcd.create_char(2, placaMitad)
        lcd.write_string('\x02')
        lcd.create_char(3, placaDos)
        lcd.write_string('\x03')
        lcd.create_char(4, placaTres)
        lcd.write_string('\x04')
        lcd.write_string(f' Placa: {abc}-{num} ')
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f'   Usuario No.{user}   ')
        lcd.cursor_pos = (2, 0)
        lcd.write_string('--------------------')
        lcd.cursor_pos = (3, 0)
        lcd.write_string(f'PAGO PARKING $:{pago}    ')

    
    def getHora():
        initH=int(time.strftime("%H"))
        initM=int(time.strftime("%M"))
        return initH,initM

    def showDataTarifa(usd):
        lcd.cursor_pos = (0, 2)
        lcd.write_string('DATOS TARIFARIOS')
        lcd.cursor_pos = (1, 4)
        lcd.write_string(f'Pago : {usd} USD')
        costoH=int(usd)
        #print(f'costoH={costoH}')
        lcd.cursor_pos = (2,3)
        costoM=int((usd-costoH)*100*30/50)
        if(usd<1.0):
            lcd.write_string(f'Tiempo:  {costoM} mins')
        else:
            lcd.write_string(f'Tiempo: {costoH}h{costoM}mins')
        lcd.cursor_pos = (3, 9)
        lcd.create_char(5, horaInitUno)
        lcd.write_string('\x05')
        lcd.create_char(6, horaInitMitad)
        lcd.write_string('\x06')
        lcd.create_char(7, horaInitDos)
        lcd.write_string('\x07')
        lcd.cursor_pos = (3, 17)
        lcd.write_string('2/4')
        return costoH,costoM
    
    def showDisponible():
        lcd.create_char(4, placaTres)
        i=0
        while(i<=19): 
            lcd.cursor_pos = (0, i)
            lcd.write_string('\x04')
            if(i<=14 and i>=5):
                pass
            else:
                lcd.cursor_pos = (3, i)
                lcd.write_string('\x04')
            i+=1
        i=0
        while(i<=3):
            lcd.cursor_pos = (i, 0)
            lcd.write_string('\x04')
            lcd.cursor_pos = (i, 19)
            lcd.write_string('\x04')
            i+=1
        lcd.cursor_pos = (1, 7)
        lcd.write_string('ESPACIO')
        lcd.cursor_pos = (2, 5)
        lcd.write_string('DISPONIBLE')
        lcd.cursor_pos = (3, 6)
        initH=time.strftime("%H")
        initM=time.strftime("%M")
        initS=time.strftime("%S")
        lcd.write_string(f'{initH}:{initM}:{initS}')

    def showPago(usd):
        lcd.create_char(4, placaTres)
        i=0
        while(i<=19): 
            lcd.cursor_pos = (0, i)
            lcd.write_string('\x04')
            lcd.cursor_pos = (3, i)
            lcd.write_string('\x04')
            i+=1
        lcd.cursor_pos = (1, 0)
        lcd.write_string('  Pago Registrado   ')
        lcd.cursor_pos = (2, 0)
        p=usd['pago']
        lcd.write_string(f'     $: {p} Usd    ')
    
    def clean():
        lcd.home()
        lcd.clear()

    def showDetectando():
        lcd.create_char(4, placaTres)
        i=0
        while(i<=19): 
            lcd.cursor_pos = (0, i)
            lcd.write_string('\x04')
            lcd.cursor_pos = (3, i)
            lcd.write_string('\x04')
            i+=1
        lcd.cursor_pos = (1, 3)
        lcd.write_string('Auto Detectado')
        lcd.cursor_pos = (2, 1)
        lcd.write_string('Reconociendo Placa')
        
    def getHoraEnd(initH,initM,costoH,costoM):
        endH=0;endM=0
        endM=int(initM)+int(costoM)
        if( endM>60):
            endM=int(endM)-60
            endH+=1
        endH=int(endH)+int(initH)+int(costoH)
        return endH,endM

    def showContTiempo(endH,endM,nowH,nowM,nowS,initH,initM):
        contNow=int(nowH*3600+nowM*60+nowS)
        contEnd=int(endH*3600+endM*60)
        cont=int(contEnd-contNow)
        contH=int(cont/3600)
        contM=int((cont-3600*contH)/60)
        contS=int(cont)-int(contH*3600)-int(contM*60)
        lcd.cursor_pos = (0, 1)
        lcd.write_string('TIEMPO DISPONIBLE')
        lcd.cursor_pos = (1, 3)
        lcd.write_string(f'Entrada : {initH}:{initM}')
        lcd.cursor_pos = (2, 4)
        lcd.write_string(f'Salida : {endH}:{endM}')
        lcd.cursor_pos = (3, 2)
        lcd.create_char(5, horaInitUno)
        lcd.write_string('\x05')
        lcd.create_char(6, horaInitMitad)
        lcd.write_string('\x06')
        lcd.create_char(7, horaInitDos)
        lcd.write_string('\x07')
        lcd.write_string(f' Time:{contH}:{contM}:{contS}')
        return cont
    
    def showAutor():
        i=0
        while(i<=19):
            if(i>=5 and i<=14):
                pass
            else:
                lcd.cursor_pos = (0, i)
                lcd.write_string('\x04')
            lcd.cursor_pos = (2, i)
            lcd.write_string('-')
            i+=1
        lcd.cursor_pos = (3, 3)
        lcd.write_string('HUMBERTO BAQUE')
        lcd.cursor_pos = (1, 0)
        texto='PROTOTIPO DE UN SISTEMA INTELIGENTE BASADO EN TECNOLOGIA IOT, PARA LA GESTION DE PARQUEADEROS VEHICULAR PUBLICOS DE LA CIUDAD DE GUAYAQUIL – ECUADOR.'
        LCD.long_text(texto)
        
        
        

def main():
    #La placa debe mostrarse del algoritmo de reconocimiento
    
    #LCD.showContTiempo(20,15,19,49,10)
    #sleep(15)
    #LCD.clean()
    #-------------------------------------------
    #num=549
    #abe='PRG'
    #LCD.showDataUser(123,abe,num)
    #-------------------------------------------
    #costo tarifa hora hora
    #sleep(5)
    #LCD.clean()
    #LCD.showDataTarifa(1.05)
    #sleep(5)
    #LCD.clean()
    #-------------------------------------------
    #LCD.showDisponible()
    #sleep(5)
    #LCD.clean()
    #LCD.showContTiempo(20,15,19,49,10)
    #sleep(5)
    #LCD.clean()
    LCD.showAutor()
    
    
if __name__ == "__main__":
    while(True):
        main()