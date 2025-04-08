# Control de LEDs para REAPER

Este programa permite visualizar y controlar LEDs virtuales en función de las pistas de audio de REAPER, con opciones para personalización de umbrales y respuesta de los LEDs.


## 🔧 Instalación
1. Clona este repositorio:
   ```bash
https://github.com/Esteban-MV/MusicTouch-TresCabezas.git
cd MusicTouch-TresCabezas

Instala las dependencias:   pip install -r requirements.txt

Ejecuta la aplicación: python main.py

# LedVisualizer

## Descripción
LedVisualizer es una aplicación en Python con PyQt6 que permite visualizar y controlar LEDs virtuales en tiempo real, asignados a las pistas de audio de REAPER a través de OSC.

## Características
- Visualización en tiempo real de LEDs que muestran su intensidad mediante opacidad.
- Configuración individual de cada LED (threshold, intensidad, método de respuesta).
- Gestión de múltiples pistas y LEDs.
- Recepción de datos OSC desde REAPER.
- Posibilidad de expandir con guardado/carga de perfiles y salida a hardware real.

## Estructura del Proyecto
