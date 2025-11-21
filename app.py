from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/educacion')
def educacion():
    return render_template('educacion.html')

@app.route('/planificacion')
def planificacion():
    return render_template('planificacion.html')

@app.route("/imc", methods=["GET", "POST"])
def imc():
    resultado = None
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"]) / 100
        imc_calc = peso / (altura ** 2)
        resultado = round(imc_calc, 2)
    return render_template("imc.html", resultado=resultado)

@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    resultado = None
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = int(request.form["edad"])
        sexo = request.form["sexo"]

        if sexo == "hombre":
            tmb_calc = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb_calc = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = round(tmb_calc, 2)

    return render_template("tmb.html", resultado=resultado)

@app.route("/gct", methods=["GET", "POST"])
def gct():
    resultado = None
    if request.method == "POST":
        tmb = float(request.form["tmb"])
        actividad = float(request.form["actividad"])
        resultado = round(tmb * actividad, 2)
    return render_template("gct.html", resultado=resultado)

@app.route("/ideal", methods=["GET", "POST"])
def ideal():
    resultado = None
    if request.method == "POST":
        altura = float(request.form["altura"])
        sexo = request.form["sexo"]

        if sexo == "hombre":
            ideal = 50 + 0.9 * (altura - 152)
        else:
            ideal = 45.5 + 0.9 * (altura - 152)

        resultado = round(ideal, 2)

    return render_template("ideal.html", resultado=resultado)

@app.route("/macros", methods=["GET", "POST"])
def macros():
    resultado = None
    if request.method == "POST":
        calorias = float(request.form["calorias"])
        prote = round((0.30 * calorias) / 4, 2)
        carbs = round((0.40 * calorias) / 4, 2)
        grasas = round((0.30 * calorias) / 9, 2)
        resultado = {"prote": prote, "carbs": carbs, "grasas": grasas}
    return render_template("macros.html", resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)