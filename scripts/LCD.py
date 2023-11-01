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
            lcd.write_string(row.ljust(num_cols)[:num_cols])
            lcd.write_string('\r\n')
    def long_text(text):
        if len(text)<20:
            lcd.write_string(text)      
        for i in range(len(text) - 20 + 1):
            framebuffer[1] = text[i:i+20]
            write_to_lcd(lcd, framebuffer, 20)
            sleep(0.8)
    def showPlaca(abc,num):
        lcd.cursor_pos = (0, 0)
        lcd.create_char(1, placaUno)
        lcd.write_string('\x01')
        lcd.create_char(2, placaMitad)
        lcd.write_string('\x02')
        lcd.create_char(3, placaDos)
        lcd.write_string('\x03')
        lcd.create_char(4, placaTres)
        lcd.write_string('\x04')
        lcd.write_string(f' Placa: {abc}-{num}')
        
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
    def contTiempo(cont):
        contH=int(cont/3600)
        contM=int((cont-3600*contH)/60)
        contS=int(cont)-int(contH*3600)-int(contM*60)
        lcd.cursor_pos = (3, 0)
        lcd.write_string(f'contador: {contH}:{contM}:{contS}')
        return contH,contM,contS
        
    def sumarHoraFin(h1,m1,h2,m2):
        
        finH=0
        finM=0
        finM=int(m1)+int(m2)
        if( finM>60):
            finM=int(finM)-60
            finH+=1
        finH=int(finH)+int(h1)+int(h2)
        return finH,finM
    def showHora(initH,initM):
        lcd.cursor_pos = (1, 0)
        lcd.create_char(5, horaInitUno)
        lcd.write_string('\x05')
        lcd.create_char(6, horaInitMitad)
        lcd.write_string('\x06')
        lcd.create_char(7, horaInitDos)
        lcd.write_string('\x07')
        lcd.write_string(f' Inicio: {initH}H{initM}')
    
    def getHora():
        initH=time.strftime("%H")
        initM=time.strftime("%M")
        return initH,initM

    def showTarifa(usd):
        lcd.cursor_pos = (2, 0)
        costoH=int(usd)
        #print(f'costoH={costoH}')
        costoM=int((usd-costoH)*100*30/50)
        #print(f'costoM={costoM}')
        lcd.write_string(f'$:{usd} USD -> t:{costoH}H{costoM}')
        return costoH,costoM
    
    def showDisponible():
        lcd.create_char(4, placaTres)
        i=0
        while(i<=19): 
            lcd.cursor_pos = (0, i)
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
        lcd.cursor_pos = (3, 3)
        initH=time.strftime("%H")
        initM=time.strftime("%M")
        initS=time.strftime("%S")
        lcd.create_char(5, horaInitUno)
        lcd.write_string('\x05')
        lcd.create_char(6, horaInitMitad)
        lcd.write_string('\x06')
        lcd.create_char(7, horaInitDos)
        lcd.write_string('\x07')
        lcd.write_string(f'   {initH}:{initM}:{initS}')

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
        
        

def main(cont):
    #La placa debe mostrarse del algoritmo de reconocimiento
    #num=549
    #abe='PRG'
    #LCD.showPlaca(abe,num)
    #hora de reconocimiento
    #initH,initM=LCD.showHora()
    #costo tarifa hora hora
    #LCD.showTarifa(1.00)
    
    LCD.showDisponible()
    
    
    
    
    
    
    
    
    
    
    
    #tiempo de salida y contador
    """    
        cont=costoH*3600+costoM*60#costo en segundos
        while(cont>=0):
            contH,contM,contS=contTiempo(cont)
            finH,finM=sumarHoraFin(initH,initM,costoH,costoM)
            if(contS%10==0):
                lcd.cursor_pos = (3, 0)
                lcd.write_string(f'Hora Salida: {finH}H{finM}')
            else:
                lcd.cursor_pos = (3, 0)
                lcd.write_string(f'Cont: {contH}:{contM}:{contS}')
            cont-=1
            sleep(1)
            lcd.cursor_pos = (3, 0)
            lcd.write_string('                   ')
        
        #lcd.cursor_pos = (0, 3)
        #long_text('Sistema de gestios de parqueaderos, ciudad de Santa Elena')
    """
    
    
if __name__ == "__main__":
    main(cont)