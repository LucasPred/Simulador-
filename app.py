from flask import Flask, request, render_template_string
import os
from google import genai
from google.genai import types

app = Flask(__name__)

# Configuración del cliente de Gemini utilizando la variable de entorno
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Analizador Granulométrico - GRAVAFILT S.A.</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        form { margin-top: 20px; display: flex; flex-direction: column; gap: 15px; }
        input[type="file"] { border: 1px solid #ccc; padding: 10px; border-radius: 4px; background: #fafafa; }
        button { background-color: #3498db; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #2980b9; }
        .result { margin-top: 30px; background: #ecf0f1; padding: 20px; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>GRAVAFILT S.A.</h1>
        <h3>Control de Calidad - Análisis Granulométrico 0.9</h3>
        <form method="POST" enctype="multipart/form-data">
            <label for="image">Sube la fotografía de la muestra de áridos:</label>
            <input type="file" name="image" id="image" accept="image/*" required>
            <button type="submit">Ejecutar Análisis Técnico</button>
        </form>
        {% if result %}
            <div class="result"><strong>Resultado del Análisis:</strong><br>{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = None
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_bytes = file.read()
                mime_type = file.mimetype or 'image/jpeg'
                
                try:
                    prompt_text = (
                        "Actúa como un ingeniero experto en programación con conocimientos técnicos profesionales "
                        "idóneos en materia de extracción, secado y tamizado de arenas y gravas. Analiza esta imagen "
                        "de la muestra de áridos y proporciona un informe detallado bajo los parámetros de buenas prácticas "
                        "para la obtención de una granulometría 0.9 con un coeficiente de uniformidad de 1.1."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=image_bytes,
                                mime_type=mime_type,
                            ),
                            prompt_text
                        ]
                    )
                    analysis_result = response.text
                except Exception as e:
                    analysis_result = f"Error al procesar la imagen con Gemini: {str(e)}"
                    
    return render_template_string(HTML_TEMPLATE, result=analysis_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
