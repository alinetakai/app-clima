import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Pega a chave da variável de ambiente
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None

    if request.method == "POST":
        cidade = request.form.get("cidade")

        if not API_KEY:
            erro = "Chave da API não encontrada. Verifique a variável de ambiente."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": cidade,
                "appid": API_KEY,
                "units": "metric",
                "lang": "pt_br"
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                dados = response.json()

                icone = f"http://openweathermap.org/img/wn/{dados['weather'][0]['icon']}@2x.png"

                clima = {
                    "cidade": cidade.title(),
                    "temp": dados["main"]["temp"],
                    "sensacao": dados["main"]["feels_like"],
                    "descricao": dados["weather"][0]["description"].capitalize(),
                    "icone": icone
                }
            elif response.status_code == 404:
                erro = "Cidade não encontrada 😢"
            else:
                erro = "Erro ao buscar dados da API."

    return render_template("index.html", clima=clima, erro=erro)

# Versão sem deploy
# if __name__ == "__main__":
#    app.run(debug=True)

# 🔥 IMPORTANTE PARA DEPLOY
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)