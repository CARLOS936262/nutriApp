from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secreto_123"


@app.route('/')
def index():
    return render_template('index.html')


# -----------------------------
# PERFIL
# -----------------------------
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if request.method == "POST":
        session["usuario"] = {
            "nombre": request.form["nombre"],
            "peso": request.form["peso"],
            "altura": request.form["altura"],
            "edad": request.form["edad"],
            "sexo": request.form.get("sexo"),
            "nivel": request.form.get("nivel"),
            "email": request.form["email"]
        }
        return redirect(url_for("perfil"))

    return render_template("perfil.html", usuario=session.get("usuario"))


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("perfil"))


# -----------------------------
# PÁGINAS GENERALES
# -----------------------------
@app.route('/educacion')
def educacion():
    return render_template('educacion.html')


@app.route('/planificacion')
def planificacion():
    return render_template('planificacion.html')


# ⭐ NUEVA RUTA: BANCO DE RECETAS
@app.route('/banco_recetas')
def banco_recetas():
    return render_template('banco_recetas.html')


# ⭐ NUEVA RUTA: HERRAMIENTAS (con tarjetas)
@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')


# -----------------------------
# CALCULADORAS
# -----------------------------
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


# -----------------------------
# ANALIZADOR DE RECETAS
# -----------------------------
NUTRI_DB = {
    "pollo": {"carbs": 0.0, "proteina": 31.0, "grasas": 3.6, "kcal": 165},
    "arroz": {"carbs": 28.0, "proteina": 2.7, "grasas": 0.3, "kcal": 130},
    "huevo": {"carbs": 1.1, "proteina": 13.0, "grasas": 11.0, "kcal": 155},
    "tortilla": {"carbs": 21.0, "proteina": 2.5, "grasas": 1.2, "kcal": 104},
    "manzana": {"carbs": 14.0, "proteina": 0.3, "grasas": 0.2, "kcal": 52},
    "aguacate": {"carbs": 9.0, "proteina": 2.0, "grasas": 15.0, "kcal": 160},
    "platano": {"carbs": 23.0, "proteina": 1.1, "grasas": 0.3, "kcal": 96},
    "pechuga": {"carbs": 0.0, "proteina": 31.0, "grasas": 3.6, "kcal": 165},
    "pan": {"carbs": 49.0, "proteina": 9.0, "grasas": 3.2, "kcal": 265},
    "leche": {"carbs": 5.0, "proteina": 3.4, "grasas": 3.6, "kcal": 60},
    "jamon": {"carbs": 1.6, "proteina": 19.0, "grasas": 3.9, "kcal": 195},
    "salchichon": {"carbs": 2.0, "proteina": 25.48, "grasas": 34.7, "kcal": 160},
    "frijoles": {"carbs": 23.5, "proteina": 8.5, "grasas": 7.5, "kcal": 192},
    "tomate": {"carbs": 3.5, "proteina": 0.9, "grasas": 0.1, "kcal": 19},
    "cebolla": {"carbs": 8.5, "proteina": 0.86, "grasas": 0.08, "kcal": 25},
    "carne de res": {"carbs": 0.1, "proteina": 37.0, "grasas": 63.0, "kcal": 288},
}


@app.route('/analizador', methods=['GET', 'POST'])
def analizador():
    resultado = None
    unknowns = []
    detalles = []
    totals = {"carbs": 0.0, "proteina": 0.0, "grasas": 0.0, "kcal": 0.0}

    if request.method == 'POST':
        ingredientes = request.form.getlist('ingrediente')
        cantidades = request.form.getlist('cantidad')

        for i in range(len(ingredientes)):
            name_raw = ingredientes[i].strip()
            if name_raw == "":
                continue

            q_str = cantidades[i].strip() if i < len(cantidades) else "0"
            try:
                cantidad = float(q_str)
            except:
                cantidad = 0.0

            key = name_raw.lower().replace(" ", "_")

            if key in NUTRI_DB:
                info = NUTRI_DB[key]

                carbs_g = (info["carbs"] * cantidad) / 100.0
                prot_g  = (info["proteina"] * cantidad) / 100.0
                gras_g  = (info["grasas"] * cantidad) / 100.0
                kcal    = (info["kcal"] * cantidad) / 100.0

                detalles.append({
                    "nombre": name_raw,
                    "cantidad": cantidad,
                    "carbs_g": round(carbs_g, 2),
                    "prot_g": round(prot_g, 2),
                    "gras_g": round(gras_g, 2),
                    "kcal": round(kcal, 2)
                })

                totals["carbs"] += carbs_g
                totals["proteina"] += prot_g
                totals["grasas"] += gras_g
                totals["kcal"] += kcal

            else:
                unknowns.append(name_raw)

        totals = {k: round(v, 2) for k, v in totals.items()}

        resultado = {
            "detalles": detalles,
            "totales": totals,
            "unknowns": unknowns
        }

    return render_template('analizador.html', resultado=resultado, db_keys=sorted(NUTRI_DB.keys()))



if __name__ == '__main__':
    app.run(debug=True)