import os
import base64
import requests
import math
from datetime import datetime, timedelta
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import concurrent.futures

# Configuración de la API REST de GPS
gps_api_url = "https://api.gps.com/v1/locations"
gps_api_key = os.environ.get("GPS_API_KEY")  # Cifre la clave de API de GPS
gps_api_key_cifrado = base64.b64encode(gps_api_key.encode()).decode()  # Cifre la clave de API de GPS

# Configuración de la cuenta de correo electrónico
correo_remitente = "tu_correo_remitente@gmail.com"
correo_asunto = "Reporte de Distancia Recorrida"
correo_password = os.environ.get("CORREO_PASSWORD")  # Cifre la contraseña de correo electrónico
correo_password_cifrado = base64.b64encode(correo_password.encode()).decode()  # Cifre la contraseña de correo electrónico

# Función para calcular la distancia entre dos puntos
def calcular_distancia(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine para calcular la distancia entre dos puntos en la superficie de la Tierra
    R = 6371  # Radio de la Tierra en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

# Función para generar el reporte PDF
def generar_reporte_pdf(vehiculos, fecha):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt="Reporte de Distancia Recorrida", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for vehiculo in vehiculos:
            pdf.cell(200, 10, txt=f"Vehículo: {vehiculo['nombre']}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Distancia recorrida: {vehiculo['distancia']} km", ln=True, align='L')
            pdf.ln(10)
        pdf.output("reporte_" + fecha + ".pdf")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

# Función para enviar el correo electrónico con el reporte PDF
def enviar_correo(remitente, asunto, password, destinatario, archivo):
    try:
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = asunto
        body = "Reporte de Distancia Recorrida"
        msg.attach(MIMEText(body))
        attachment = open(archivo, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % archivo)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        text = msg.as_string()
        server.sendmail(remitente, destinatario, text)
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")

# Función para obtener los datos de la API REST de GPS para una fecha
def obtener_datos_fecha(fecha):
    params = {
        "api_key": gps_api_key_cifrado,
        "fecha": fecha
    }
    response = requests.get(gps_api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos para la fecha {fecha}: {response.status_code}")
        return None

# Función para obtener los datos de la API REST de GPS para un rango de fechas
def obtener_datos_fecha_rango(fecha_inicio, fecha_fin):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for fecha in [fecha_inicio + timedelta(days=i) for i in range(int((fecha_fin - fecha_inicio).days) + 1)]:
            fecha_str = fecha.strftime("%Y-%m-%d")
            futures.append(executor.submit(obtener_datos_fecha, fecha_str))
        resultados = [f.result() for f in futures]
        return resultados

# Función principal para generar el reporte de distancia recorrida
def generar_reporte():
    fecha_inicio = datetime.now() - timedelta(days=1)
    fecha_fin = datetime.now()
    vehiculos = []
    resultados = obtener_datos_fecha_rango(fecha_inicio, fecha_fin)
    for resultado in resultados:
        if resultado is not None:
            for vehiculo in resultado['vehiculos']:
                ubicacion_anterior = vehiculo['ubicacion_anterior']
                ubicacion_actual = vehiculo['ubicacion_actual']
                distancia = calcular_distancia(ubicacion_anterior['lat'], ubicacion_anterior['lon'], ubicacion_actual['lat'], ubicacion_actual['lon'])
                vehiculos.append({
                    'nombre': vehiculo['nombre'],
                    'distancia': distancia
                })
    generar_reporte_pdf(vehiculos, fecha_fin.strftime("%Y-%m-%d"))
    enviar_correo(correo_remitente, correo_asunto, correo_password_cifrado, "destinatario@example.com", "reporte_" + fecha_fin.strftime("%Y-%m-%d") + ".pdf")

# Ejecutar la función principal
generar_reporte()
Nota: En este código, se utiliza la biblioteca `os` para obtener las credenciales de API de GPS y la contraseña de correo electrónico desde variables de entorno. Se cifran las credenciales utilizando la biblioteca `base64`. Se utiliza la función `obtener_datos_fecha` para obtener los datos de la API de GPS para una fecha, y se utiliza la función `obtener_datos_fecha_rango` para obtener los datos de la API de GPS para un rango de fechas. Se utiliza la función `generar_reporte_pdf` para generar el reporte PDF, y se utiliza la función `enviar_correo` para enviar el correo electrónico con el reporte PDF.