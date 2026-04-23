# Generador de Reporte de Distancia Recorrida
==========================

Este proyecto es un script que consume la API REST de GPS para obtener la ubicación diaria de los vehículos y calcular la distancia recorrida diaria entre las ubicaciones de los vehículos. El script genera un reporte PDF diario con la distancia recorrida de cada vehículo y lo envía a los responsables a través de correo electrónico.

## Características

* Consumo de API REST de GPS para obtener la ubicación diaria de los vehículos
* Cálculo de la distancia recorrida diaria entre las ubicaciones de los vehículos
* Generación de reporte PDF diario con la distancia recorrida de cada vehículo
* Envío del reporte PDF diario a los responsables a través de correo electrónico
* Manejo de múltiples vehículos y ubicaciones
* Generación de reportes diarios en un rango de fechas específico

## Requisitos

* Python 3.x
* Biblioteca `requests` para consumo de API REST
* Biblioteca `matplotlib` para generación de reporte PDF
* Biblioteca `smtplib` para envío de correo electrónico
* Conexión a la API de GPS

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias con `pip install -r requirements.txt`
3. Configurar la conexión a la API de GPS en el archivo `config.py`

## Uso

1. Ejecutar el script con `python main.py`
2. Seleccionar la fecha de inicio y fin del rango de fechas para generar el reporte
3. Seleccionar los vehículos para incluir en el reporte
4. El script generará un reporte PDF diario con la distancia recorrida de cada vehículo y lo enviará a los responsables a través de correo electrónico