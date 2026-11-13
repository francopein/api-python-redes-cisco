
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

    # Consultar hosts
    api_url = baseUri + "/host"

    headers = {
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers)

    print("Request status:", resp.status_code)

    if resp.status_code == 200:

        response_json = resp.json()
        hosts = response_json["response"]

        print()
        print("Hosts de la red:")
        print()

        for host in hosts:

            nombre = host.get("hostName", "Sin nombre")
            ip = host.get("hostIp", "Sin IP")
            mac = host.get("hostMac", "Sin MAC")
            interfaz = host.get("connectedInterfaceName", "Sin interfaz")

            print(nombre, "\t", ip, "\t", mac, "\t", interfaz)

    else:
        print("Error al consultar los hosts:")
        print(resp.text)

else:
    print("No se pudo obtener el ticket de autenticacion.")
    print(resp.text)
