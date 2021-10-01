import requests
import json
"""
    Este es un ejemplo de como debe ser el input y cual será el output
"""
URL = "http://localhost:5005/webhooks/rest_custom/webhook"
        

def send_msg(msg, name, personality):
    data = {"sender": name, "message": msg, "metadata": { "personality": personality} }
    x = requests.post(URL, json = data)
    print(x)
    rta = x.json()[-1] 
    text = rta["text"]
    
    if x.status_code == 200:
        return text
    else:
        print(x.raw)
        return None

personality = "global" #estas prob hacen que los mensajes pasen a ser de formato informal
input()
rta = send_msg("Los datos procesados se envian a action management para determinar que accion ejecutar en el habitante","Emiliano",personality)
print(rta)
input()
rta = send_msg("repetime que es scrum","Emiliano",personality)
print(rta)
