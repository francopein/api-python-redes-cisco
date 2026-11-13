
import json
import requests
from getpass import getpass

# Direccion de la API del Cisco Network Controller
baseUri = "http://localhost:58000/api/v1"

# Solicitar credenciales
usuario = input("Usuario del controlador: ")
contrasena = getpass("Contrasena del controlador: ")

# Obtener ticket de autenticacion
headers = {
    "Content-Type": "application/json"
}

data = {
    "username": usuario,
    "password": contrasena
}

resp = requests.post(
    baseUri + "/ticket",
    json=data,
    headers=headers
)

print("Estado de autenticacion:", resp.status_code)

if resp.status_code == 201:

    # Obtener ticket
    response_json = resp.json()
    ticket = response_json["response"]["serviceTicket"]

    # Consultar dispositivos de red
    api_url = baseUri + "/network-device"

    headers = {
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers)

    print("Request status:", resp.status_code)

    if resp.status_code == 200:

        response_json = resp.json()
        networkDevices = response_json["response"]

        print()
        print("Dispositivos de red:")
        print()

        for networkDevice in networkDevices:

            hostname = networkDevice.get("hostname", "Sin hostname")
            plataforma = networkDevice.get("platformId", "Sin plataforma")
            ip = networkDevice.get("managementIpAddress", "Sin IP")

            print(hostname, "\t", plataforma, "\t", ip)

    else:
        print("Error al consultar los dispositivos:")
        print(resp.text)

else:
    print("No se pudo obtener el ticket de autenticacion.")
    print(resp.text)
