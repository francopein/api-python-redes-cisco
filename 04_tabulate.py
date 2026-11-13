
# Modulos que se utilizaran
import requests
from getpass import getpass
from tabulate import tabulate

# URL del Cisco Network Controller
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

print("Status de Solicitud:")
print(resp.status_code)

if resp.status_code == 201:

    # Obtener ticket
    result = resp.json()
    ticket = result["response"]["serviceTicket"]

    # Encabezado para las consultas
    headers = {
        "X-Auth-Token": ticket
    }

    # Consultar dispositivos de red
    resp = requests.get(
        baseUri + "/network-device",
        headers=headers
    )

    if resp.status_code == 200:

        result = resp.json()

        print("\nDispositivos de Red:")

        host_list = []
        i = 0

        for item in result["response"]:
            i += 1

            host_list.append([
                i,
                item.get("hostname", "Sin hostname"),
                item.get("serialNumber", "Sin serial"),
                item.get("softwareVersion", "Sin version")
            ])

        print(tabulate(
            host_list,
            headers=["Nro", "Hostname", "Serial Number", "Software Version"],
            tablefmt="rst"
        ))

    else:
        print("Error al consultar los dispositivos:")
        print(resp.text)

    # Consultar hosts de la red
    resp = requests.get(
        baseUri + "/host",
        headers=headers
    )

    if resp.status_code == 200:

        result = resp.json()

        print("\nHosts de la Red:")

        host_list = []
        i = 0

        for item in result["response"]:
            i += 1

            host_list.append([
                i,
                item.get("hostName", "Sin nombre"),
                item.get("hostType", "Sin tipo"),
                item.get("hostIp", "Sin IP")
            ])

        print(tabulate(
            host_list,
            headers=["Nro", "Hostname", "Tipo", "IP"],
            tablefmt="rst"
        ))

    else:
        print("Error al consultar los hosts:")
        print(resp.text)

else:
    print("No se pudo obtener el ticket de autenticacion.")
    print(resp.text)
