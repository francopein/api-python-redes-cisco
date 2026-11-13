
import requests
import csv
from getpass import getpass

# Direccion del Cisco Network Controller
baseUri = "http://localhost:58000/api/v1"

# Solicitar credenciales
usuario = input("Usuario del controlador: ")
contrasena = getpass("Contrasena del controlador: ")

# Solicitar ticket de autenticacion
data = {
    "username": usuario,
    "password": contrasena
}

headers = {
    "Content-Type": "application/json"
}

resp = requests.post(
    baseUri + "/ticket",
    json=data,
    headers=headers
)

print("Estado de autenticacion:", resp.status_code)

if resp.status_code == 201:

    # Obtener ticket de autenticacion
    ticket = resp.json()["response"]["serviceTicket"]

    # Header para las consultas
    headers = {
        "X-Auth-Token": ticket
    }

    # Consultar dispositivos de red
    respDispositivos = requests.get(
        baseUri + "/network-device",
        headers=headers
    )

    # Consultar hosts
    respHosts = requests.get(
        baseUri + "/host",
        headers=headers
    )

    if respDispositivos.status_code == 200 and respHosts.status_code == 200:

        dispositivos = respDispositivos.json()["response"]
        hosts = respHosts.json()["response"]

        # Crear archivo CSV
        with open("inventario_red.csv", "w", newline="", encoding="utf-8-sig") as archivo:

            escritor = csv.writer(archivo, delimiter=";")

            escritor.writerow([
                "Categoria",
                "Nombre",
                "Tipo",
                "Direccion IP",
                "Plataforma",
                "Numero de serie",
                "Direccion MAC"
            ])

            # Guardar dispositivos
            for dispositivo in dispositivos:

                escritor.writerow([
                    "Dispositivo",
                    dispositivo.get("hostname", "Sin hostname"),
                    dispositivo.get("type", "Sin tipo"),
                    dispositivo.get("managementIpAddress", "Sin IP"),
                    dispositivo.get("platformId", "Sin plataforma"),
                    dispositivo.get("serialNumber", "Sin serial"),
                    dispositivo.get("macAddress", "Sin MAC")
                ])

            # Guardar hosts
            for host in hosts:

                escritor.writerow([
                    "Host",
                    host.get("hostName", "Sin nombre"),
                    host.get("hostType", "Sin tipo"),
                    host.get("hostIp", "Sin IP"),
                    "",
                    "",
                    host.get("hostMac", "Sin MAC")
                ])

        print("Inventario exportado correctamente.")
        print("Dispositivos registrados:", len(dispositivos))
        print("Hosts registrados:", len(hosts))
        print("Archivo generado: inventario_red.csv")

    else:
        print("Error al consultar dispositivos u hosts.")
        print("Estado dispositivos:", respDispositivos.status_code)
        print("Estado hosts:", respHosts.status_code)

else:
    print("No se pudo obtener el ticket de autenticacion.")
    print(resp.text)
