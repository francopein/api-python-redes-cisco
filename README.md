# API Python - Redes Cisco

Proyecto desarrollado para el **Trabajo Práctico N.º 4 Integrador de Redes de Computadoras (3643) - UNLaM, 2026**.

El objetivo es utilizar Python para realizar consultas sobre la API REST del Cisco Network Controller, obtener información de los dispositivos de red y hosts registrados, y generar un inventario de red en formato CSV.

## 1. Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.
- Cisco Packet Tracer con el Network Controller en ejecución.
- Librería `requests`.
- Librería `tabulate`.

## 2. Clonación del proyecto

Para descargar el repositorio mediante Git, ejecutar:

```bash
git clone https://github.com/francopein/api-python-redes-cisco.git
```

Ingresar a la carpeta del proyecto:

```bash
cd api-python-redes-cisco
```

## 3. Creación del entorno virtual

Un entorno virtual permite instalar las librerías necesarias para el proyecto sin modificar la instalación general de Python.

### Windows (PowerShell)

Crear el entorno virtual:

```powershell
py -m venv cisco
```

Activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\cisco\Scripts\Activate.ps1
```

### Linux

Crear el entorno virtual:

```bash
python3 -m venv cisco
```

Activarlo:

```bash
source cisco/bin/activate
```

Cuando el entorno está activado, su nombre aparece entre paréntesis en la terminal.

## 4. Instalación de dependencias

Con el entorno virtual activado y ubicados en la carpeta raíz del proyecto, ejecutar:

```bash
python -m pip install -r requirements.txt
```

Este comando instala las dependencias necesarias para ejecutar los programas.

## 5. Estructura del proyecto

Los scripts se encuentran dentro de la carpeta `src`.

```text
api-python-redes-cisco/
│
├── src/
│   ├── 01_get-ticket.py
│   ├── 02_get-network-device.py
│   ├── 03_get-host.py
│   ├── 04_tabulate.py
│   └── 05_inventario_red.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 6. Descripción de los scripts

### 01_get-ticket.py

Realiza una solicitud POST al endpoint `/ticket` del Cisco Network Controller para obtener un ticket de autenticación.

El ticket permite realizar consultas posteriores a la API.

### 02_get-network-device.py

Realiza una solicitud GET al endpoint `/network-device` para consultar los dispositivos de red registrados en el controlador.

Muestra información como:

- Hostname.
- Plataforma.
- Dirección IP de administración.

Utiliza valores alternativos cuando algunos campos no están disponibles en la respuesta.

### 03_get-host.py

Realiza una solicitud GET al endpoint `/host` para consultar los hosts registrados en la red.

Muestra información como:

- Nombre del host.
- Dirección IP.
- Dirección MAC.
- Interfaz de conexión.

### 04_tabulate.py

Realiza consultas a la API para obtener información de los dispositivos de red y los hosts.

Utiliza la librería `tabulate` para organizar y mostrar los resultados en tablas en la terminal.

### 05_inventario_red.py

Es un script desarrollado para este trabajo práctico.

Solicita las credenciales del usuario del Network Controller y obtiene un ticket de autenticación.

Luego realiza consultas a los endpoints:

- `/network-device`
- `/host`

Con la información obtenida genera un archivo llamado `inventario_red.csv`.

El archivo contiene las siguientes columnas:

- Categoría.
- Nombre.
- Tipo.
- Dirección IP.
- Plataforma.
- Número de serie.
- Dirección MAC.

Los datos que no están disponibles en la respuesta de la API se representan mediante valores alternativos, por ejemplo, `Sin hostname`.

## 7. Ejecución de los programas

Desde la carpeta raíz del proyecto, con el entorno virtual activado, ejecutar los siguientes comandos en PowerShell:

```powershell
python .\src\01_get-ticket.py
```

```powershell
python .\src\02_get-network-device.py
```

```powershell
python .\src\03_get-host.py
```

```powershell
python .\src\04_tabulate.py
```

```powershell
python .\src\05_inventario_red.py
```

Para el último programa se solicitará:

- Usuario del controlador.
- Contraseña del controlador.

La contraseña se introduce de forma oculta durante la ejecución.

## 8. Autenticación y tickets

La API del Cisco Network Controller utiliza un mecanismo de autenticación mediante tickets.

Para obtener un ticket se realiza una solicitud POST al endpoint:

```text
http://localhost:58000/api/v1/ticket
```

El ticket obtenido se utiliza posteriormente en el encabezado HTTP:

```text
X-Auth-Token
```

Los tickets tienen una duración limitada y pueden vencer. En ese caso, es necesario solicitar uno nuevo.

**Importante:** las credenciales deben corresponder a un usuario creado en el Cisco Network Controller. No se deben publicar contraseñas ni tickets de autenticación en el repositorio público.

## 9. Resultado de la ejecución

Durante las pruebas realizadas con el Cisco Network Controller se obtuvieron los siguientes resultados para el script `05_inventario_red.py`:

- Autenticación exitosa: HTTP 201.
- Dispositivos de red registrados: 12.
- Hosts registrados: 11.
- Archivo CSV generado correctamente: `inventario_red.csv`.

El archivo permite consultar la información obtenida y utilizarla como inventario de los elementos registrados en la red.

## 10. Desactivación del entorno virtual

Para desactivar el entorno virtual, ejecutar:

```powershell
deactivate
```

El mismo comando se utiliza en Linux.

## 11. Consideraciones de seguridad

- No publicar contraseñas del Network Controller.
- No publicar tickets de autenticación.
- No subir carpetas de entornos virtuales.
- Mantener las dependencias declaradas en `requirements.txt`.
- Utilizar el archivo `.gitignore` para excluir archivos locales y datos sensibles.

## 12. Conclusión

El proyecto permite interactuar con la API REST del Cisco Network Controller mediante Python.

A través de los distintos scripts se obtiene información de autenticación, dispositivos de red y hosts. Además, se incorpora una funcionalidad propia que permite exportar los datos consultados a un archivo CSV para generar un inventario de red.