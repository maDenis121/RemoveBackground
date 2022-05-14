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

@app.route("/")
def hello():
    return "Hello, World!"

def eliminarFondo():
    #cargar imagen
    img = cv2.imread('OIP.jpg', cv2.IMREAD_COLOR)
    
    #convertir a gris
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #límite de la imagen de input como máscara
    mask = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY)[1]
    
    #negamos la máscara
    mask = 255 - mask

    #aplicamos la morfología para quitar ruído momentáneo 
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    #Hacemos anti-aliasing de la másrcara
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX = 2, sigmaY = 2, borderType= cv2.BORDER_DEFAULT)

    #Limitar los valores a blanco o negro
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    #ponemos la máscara en el canal aplha
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:,:,3] = mask

    cv2.imshow('imagen',result)
    cv2.waitKey(0)
    cv2.destroyAllWindows

eliminarFondo()
