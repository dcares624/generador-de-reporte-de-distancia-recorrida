import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import requests
import json
from fpdf import FPDF

# Configuración de la API REST de GPS
api_url = "https://api.gps.com/locations"
api_key = "TU_API_KEY"

# Configuración del script
script_timezone = pytz.timezone("America/Mexico_City")
script_schedule = datetime.now(script_timezone).replace(hour=8, minute=0, second=0)

# Input de fecha y hora
st.title("Generador de Reporte de Distancia Recorrida")
st.write("Ingrese la fecha y hora en la que se quiere ejecutar el script:")
fecha_hora = st.text_input("Fecha y hora", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Botón de ejecución
if st.button("Ejecutar"):
    # Consumir la API REST de GPS
    response = requests.get(api_url, headers={"Authorization": f"Bearer {api_key}"})
    data = json.loads(response.text)
    
    # Calcular la distancia recorrida
    distancia_recorrida = []
    for location in data:
        distancia_recorrida.append(location["distance"])
    
    # Generar el reporte PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Reporte de Distancia Recorrida", ln=True, align='C')
    pdf.ln(10)
    for i, location in enumerate(data):
        pdf.cell(200, 10, txt=f"Fecha: {location['date']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Distancia recorrida: {location['distance']} km", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Ubicación inicial: {location['initial_location']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Ubicación final: {location['final_location']}", ln=True, align='L')
        pdf.ln(10)
    
    # Almacenar el reporte PDF en un directorio específico
    pdf.output("reporte.pdf", "F")

    # Mostrar el gráfico de distancia recorrida
    plt.plot(distancia_recorrida)
    plt.xlabel("Fecha")
    plt.ylabel("Distancia recorrida (km)")
    plt.title("Gráfico de distancia recorrida")
    st.pyplot(plt.gcf())

    # Mostrar la tabla de reporte
    tabla_reporte = pd.DataFrame(data)
    st.write(tabla_reporte)
Nota: Es importante reemplazar la URL de la API REST de GPS y la API key con los valores reales. Además, es importante configurar el script para que se ejecute automáticamente cada día a la misma hora.