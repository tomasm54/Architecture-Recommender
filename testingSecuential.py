import requests
import json
"""
    Este es un ejemplo de como debe ser el input y cual será el output
"""
URL = "http://localhost:5005/webhooks/rest_custom/webhook"
        

def send_msg(msg, name, personality):
    data = {"sender": name, "message": msg, "metadata": { "personality": personality} }
    x = requests.post(URL, json = data)
    rta = x.json()[-1] 
    text = rta["text"]
    
    if x.status_code == 200:
        return text
    else:
        print(x.raw)
        return None

personality = "Sequential" #estas prob hacen que los mensajes pasen a ser de formato informal
input()
rta = send_msg("Los datos del cerebro son procesados por la unidad de procesamiento de senales", "Matias", personality) #Input
print(rta) #print del Output
input()
rta = send_msg("La informacion es convertida a senales electricas y enviadas al cerebro","Matias",personality)
print(rta)

