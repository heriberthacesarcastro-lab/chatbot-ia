from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/pregunta", methods=["POST"])
def pregunta():
    datos = request.get_json()
    texto = datos.get("pregunta", "").strip()

    if not texto:
        return jsonify({"respuesta": "No recibí ninguna pregunta."})

    try:
        respuesta = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=texto
        )

        return jsonify({
            "respuesta": respuesta.text
        })

    except Exception as error:
        print("ERROR DE GEMINI:", error)

        return jsonify({
            "respuesta": "Gemini está temporalmente ocupado. Intenta de nuevo."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )