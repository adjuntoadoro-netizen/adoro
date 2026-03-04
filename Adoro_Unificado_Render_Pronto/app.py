from flask import Flask, render_template
import datetime
import calendar
import ephem
import os

app = Flask(__name__)

def calcular_regencia():
    hoje = datetime.date.today()
    agora = ephem.Date(datetime.datetime.now())

    ultima = ephem.previous_full_moon(agora).datetime().date()
    proxima = ephem.next_full_moon(agora).datetime().date()

    lua_cheia = ultima if abs((hoje-ultima).days) <= abs((proxima-hoje).days) else proxima

    inicio = lua_cheia - datetime.timedelta(days=3)
    fim = lua_cheia + datetime.timedelta(days=3)

    dias = []
    d = inicio
    while d <= fim:
        dias.append(d.day)
        d += datetime.timedelta(days=1)

    return dias

@app.route("/")
def home():
    hoje = datetime.date.today()
    dias_regencia = calcular_regencia()
    dias_no_mes = calendar.monthrange(hoje.year, hoje.month)[1]

    return render_template(
        "home.html",
        hoje=hoje,
        dias_regencia=dias_regencia,
        dias_no_mes=dias_no_mes
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
