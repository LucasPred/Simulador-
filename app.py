import os
from flask import Flask, render_template, request, redirect, url_for
from google import genai

app = Flask(__name__)

# Inicializar el cliente forzando la lectura de la variable de entorno de Render
import os
from google import genai

# Inicializar el cliente asegurando que lea la variable de Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))



app = Flask(__name__)

# Inicializar el cliente de la API de Gemini (toma automáticamente la variable de entorno GEMINI_API_KEY)
client = genai.Client()

# Interfaz HTML integrada en el mismo archivo para hacerlo 100% autosuficiente
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Analizador Granulométrico IA - Áridos</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { color: #0f172a; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 8px; }
        input[type="file"] { display: block; width: 100%; padding: 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; }
        button { background: #2563eb; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; width: 100%; }
        button:hover { background: #1d4ed8; }
        #loading { display: none; text-align: center; font-style: italic; color: #64748b; margin-top: 15px; }
        .result-box { margin-top: 30px; background: #f8fafc; border-left: 5px solid #2563eb; padding: 20px; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Análisis Granulométrico por IA</h1>
        <p style="text-align: center; color: #64748b;">Sube una fotografía clara de la muestra de arena o grava para estimación técnica.</p>
        
        <div class="form-group">
            <label for="imageFile">Seleccionar Imagen de la Muestra:</label>
            <input type="type" id="imageFile" type="file" accept="image/*">
        </div>
        
        <button onclick="analizarMuestra()">Ejecutar Análisis Granulométrico</button>
        
        <div id="loading">Procesando imagen con motores multimodales de Gemini...</div>
        
        <div id="resultado" class="result-box" style="display:none;"></div>
    </div>

    <script>
        async function analizarMuestra() {
            const fileInput = document.getElementById('imageFile');
            const resultDiv = document.getElementById('resultado');
            const loadingDiv = document.getElementById('loading');

            if (fileInput.files.length === 0) {
                alert('Por favor, selecciona una imagen primero.');
                return;
            }

            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = async function(e) {
                const base64Data = e.target.result.split(',')[1];
                
                loadingDiv.style.display = 'block';
                resultDiv.style.display = 'none';

                try {
                    const response = await fetch('/analizar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ image: base64Data, mime_type: file.type })
                    });

                    const data = await response.json();
                    loadingDiv.style.display = 'none';
                    resultDiv.style.display = 'block';

                    if (data.success) {
                        resultDiv.textContent = JSON.stringify(data.analisis, null, 2);
                    } else {
                        resultDiv.textContent = "Error: " + data.error;
                    }
                } catch (err) {
                    loadingDiv.style.display = 'none';
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = "Error de conexión: " + err.message;
                }
            };
            reader.readAsDataURL(file);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        data = request.json
        image_bytes = base64.b64decode(data['image'])
        mime_type = data.get('mime_type', 'image/jpeg')

        # Prompt experto estructurado para control granulométrico
        prompt_experto = (
            "Actúa como un ingeniero experto en procesamiento de áridos, extracción y mecánica de tamizado. "
            "Analiza detalladamente esta fotografía de la muestra de material granular. "
            "Estima y devuelve estrictamente un reporte técnico que incluya: "
            "1. Granulometría estimada predominante (ej. evaluación orientativa respecto a parámetro objetivo de 0.9). "
            "2. Coeficiente de uniformidad estimado (Cu) y curvatura. "
            "3. Morfología de las partículas (angulosidad, redondez, presencia de finos o arcillas superficiales). "
            "4. Observaciones de calidad y control de buenas prácticas para la línea de producción."
        )

        # Invocación oficial del modelo multimodal de Gemini 
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt_experto,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ],
        )

        return jsonify({'success': True, 'analisis': response.text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

