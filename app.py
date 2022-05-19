import os
from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
from removebackground import quitar_fondo
from upload import download_file

app = Flask(__name__)
app.secret_key = "removebackground"

app.config['IMAGE_FOLDER'] = "/static/"
os.chdir(os.path.dirname(__file__) + app.config['IMAGE_FOLDER'])

print(os.getcwd())

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        imagenOriginal = request.files['imagenOriginal']
        imagenFondo = request.files['imagenFondo']


        imagenOriginalFilename = secure_filename(imagenOriginal.filename)
        imagenFondoFilename = secure_filename(imagenFondo.filename)
        imagenOriginal.save(imagenOriginalFilename)
        imagenFondo.save(imagenFondoFilename)
        nombreNuevaImagen = quitar_fondo(imagenOriginalFilename, imagenFondoFilename, app.config['IMAGE_FOLDER'])
        session["rutaNuevaImagen"] = nombreNuevaImagen;
        return redirect(url_for("resultado"))
    else:
        return render_template("main.html")

@app.route("/resultado")
def resultado():
    if "rutaNuevaImagen" in session:
        return render_template("resultado.html", rutaImagen=session["rutaNuevaImagen"])
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()