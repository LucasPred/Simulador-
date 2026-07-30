import os
from flask import Flask, render_template, request, redirect, url_for
from google import genai

app = Flask(__name__)

# Configuración y validación robusta de la clave de API
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No se encontró la clave de API de Gemini en las variables de entorno de Render.")

# Inicializar el cliente oficial de Gemini
client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    # Renderiza la interfaz principal (asegúrate de tener tu archivo index.html en la carpeta templates)
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    # Lógica de recepción de datos o imágenes para procesar con Gemini
    if 'imagen' not in request.files:
        return redirect(url_for('index'))
    
    archivo = request.files['imagen']
    if archivo.filename == '':
        return redirect(url_for('index'))

    # Aquí puedes integrar la llamada al modelo de Gemini usando 'client'
    # Ejemplo: response = client.models.generate_content(...)
    
    return "Análisis en proceso..."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
