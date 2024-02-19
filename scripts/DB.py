import firebase_admin
import time
from firebase_admin import db
from firebase_admin import credentials
cred = credentials.Certificate('/home/parking/Desktop/raspberry_IoT_parking/scripts/credIoT.json')
nombreBase= 'rasp_IoT_fireBase'
auth=firebase_admin.initialize_app(cred,{
    'databaseURL':'https://rasp-iot-parquimetro-default-rtdb.firebaseio.com/'
}) 
 
dataB={'idAgent':345,'idSudo':'343fskdf','idUser':159,'llegadaHora':21048,'pagoUsd':1050,'placaAuto':'ASR-123','distAuto':40}

class fireBase(object):
    def __init__(self):
        self.dataB={}
        pass
    def crearData(self):
        """Esta función crea una una variable en la base de  
           datos. 
        """ 
        ref = db.reference() 
        ref.push({'clave':'987'}) 
        print(ref.get()) 
    def addData(self): 
        """Esta función aniade datos a la base creada 
        """ 
        ref = db.reference(nombreBase) 
        producto= {'clave':'123','modelo':'raspberry pi'} 
        producto_ref=ref.push(producto) 
    def ActualizarData(self): 
        ref = db.reference(nombreBase) 
        ref_producto = ref.child(nombreBase) 
        ref_producto.update({'clave':'11111'}) 
    def upIdUser(id): 
        """ 
        Actualiza el Id del usuario 
        """ 
        ref = db.reference(nombreBase) 
        ref.update({ 
            'idUser' : id 
            }) 
        print('Id User update') 
         
    def upIdAgent(id): 
        """ 
        Actualiza el Id del agente de transito 
        """ 
        ref = db.reference(nombreBase) 
        ref.update({ 
            'idAgent' : id 
            }) 
        print('Id Agent update') 
 
    def upIdSudo(id): 
        """ 
        Actualiza el Id del super usuario 
        """ 
        ref = db.reference(nombreBase) 
        ref.update({ 
            'idSudo' : id 
            }) 
        print('Id Sudo update')
    def upHoraIn(): 
        """ 
        Actualiza la actual de llegada  
        al estacionamiento 
        """ 
        initH=time.strftime("%H") 
        initM=time.strftime("%M") 
        initLlegada=int(initH)*1000+int(initM) 
        ref = db.reference(nombreBase)
        ref.update({
            'llegadaHora' : initLlegada
            })
        print('Hora actual update')
    def upPago(tarifa):
        """
        Actualiza la costo tarifa 
        al estacionamiento
        """ 
        dolar = int(tarifa)
        moneda=tarifa-dolar
        pagoUsd=dolar*1000+moneda*100
        ref = db.reference(nombreBase)
        ref.update({
            'pagoUsd' : pagoUsd
            })
        print('Costo Hora update')
        
    def upPlacaAuto(placa):
        """
        Actualiza la placa del auto
        """
        ref = db.reference(nombreBase)
        ref.update({
            'placaAuto' : placa
            })
        print('placa Auto update')
        
    def manejoData():
        """Comandos para manejar el diccionario 
           con la base de datos
        """
        print(dataB)
        #actualizar datos
        dataB['idUser']=5000
        dato=dataB['idAgent']
        print(f'Dato del agente es: {dato}')
        
    def getDistAuto(): 
        """ 
        Obtiene la distancia de reconocimiento de los autos 
        """ 
        ref = db.reference('/rasp_IoT_fireBase/distAuto')#db.reference(nombreBase) 
        dist=ref.get()
        #print(f'Distancia configurada es: {dist} cm')
        return dist
        
        
def main():
    pass
    # Inicialización de datos
    #fireBase.upIdUser(159)
    #fireBase.upIdAgent(345)
    #fireBase.upIdSudo('343fskdf')
    #fireBase.upHoraIn()
    #fireBase.upPago(1.25)
    #fireBase.upPlacaAuto('ASR-123')
    fireBase.getDistAuto()
    
        
if __name__ == '__main__':
    main()