from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)