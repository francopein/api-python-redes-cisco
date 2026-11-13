
import requests
from getpass import getpass

# URL del Cisco Network Controller
baseUri = "http://localhost:58000/api/v1"

# Solicitar credenciales
usuario = input("Usuario del controlador: ")
contrasena = getpass("Contrasena del controlador: ")

# Preparar los datos de autenticacion
headers = {
    "Content-Type": "application/json"
}

data = {
    "username": usuario,
    "password": contrasena
}

# Solicitar ticket al controlador
resp = requests.post(
    baseUri + "/ticket",
    json=data,
    headers=headers
)

print("Ticket request status:", resp.status_code)

if resp.status_code == 201:

    result = resp.json()
    ticket = result["response"]["serviceTicket"]

    print("Autenticacion exitosa.")
    print("El ticket se obtuvo correctamente.")

else:
    print("Error al obtener el ticket.")
    print(resp.text)
