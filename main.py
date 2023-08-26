from iqoptionapi.stable_api import IQ_Option
from dotenv import load_dotenv
import os
import time

# Configura las credenciales de inicio de sesión
username = os.getenv("CORREO")
password = os.getenv("CONTRASEHA")

# Crea una instancia de la API de IQ Option
iq_api = IQ_Option(username, password)

# Inicia sesión en la cuenta
check,error=iq_api.connect()
if check==True:print("Logeado correctamente", check)
else:print(error, check)

def cuenta(tipo:int=0):
    if tipo == 0:
        iq_api.change_balance('PRACTICE')
        print("cuenta de practica")      
    else:
        iq_api.change_balance('REAL')
        print("cuenta real")
        
        
def compra_venta(activo, valor, direccion, tiempo_expiracion, tipo):
    check, id_orden = False, {}
    if tipo == 'digital':
        check, id_orden = iq_api.buy_digital_spot_v2(activo, valor, direccion, tiempo_expiracion)
    elif tipo == 'binaria':
        check, id_orden = iq_api.buy(valor, activo, direccion, tiempo_expiracion)
                      
    if check:
        print("orden abierta",id_orden)
        while True:
            time.sleep((tiempo_expiracion*60)/3)
            estado, resultado = iq_api.check_win_digital_v2(id_orden) if tipo == 'digital' else iq_api.check_win_v4(id_orden) # type: ignore
            if estado and isinstance(resultado, float):
                if resultado>0:print("se gano", round(resultado,2))
                elif resultado==0:print("se empaoe", round(resultado,2))
                elif resultado<0:print("se perdio", round(resultado,2))
                break
    else: print("error en la orden", id_orden)  
    
    
if __name__ == '__main__':
    cuenta()
    c=0
    while c<10:
        compra_venta('EURGBP',1,'call',1,'digital')
        time.sleep(15)
        c+=1