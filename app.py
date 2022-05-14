from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

#Importar parquetes necesarios
#import os
import cv2
import numpy as np
#import mediapipe as mp


from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def eliminarFondo():
    #cargar imagen
    img = cv2.imread('OIP.jpg')
    
    #convertir a gris
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #límite de la imagen de input como máscara
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    #negamos la máscara
    mask = 255 - mask

    cv2.imshow('imagen',mask)


eliminarFondo()
