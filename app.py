from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

#Importar parquetes necesarios
import os
import cv2 
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys
from PIL import Image
#import mediapipe as mp
import shutil

@app.route("/")
def hello():
    return "Hello, World!"

def eliminarFondo1():
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
    result[:, :, 3] = mask

    cv2.imshow('imagen',mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows


def prueba2():
    img = cv.imread('OIP.jpg', cv.IMREAD_UNCHANGED)
    original = img.copy()

    l = int(max(5, 6))
    u = int(min(6, 6))

    ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.GaussianBlur(img, (21, 51), 3)
    edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(edges, l, u)

    _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

    data = mask.tolist()
    sys.setrecursionlimit(10**8)
    for i in  range(len(data)):
        for j in  range(len(data[i])):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
        for j in  range(len(data[i])-1, -1, -1):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
    image = np.array(data)
    image[image !=  -1] =  255
    image[image ==  -1] =  0

    mask = np.array(image, np.uint8)

    result = cv.bitwise_and(original, original, mask=mask)
    result[mask ==  0] =  255
    cv.imwrite('bg.png', result)

    img = Image.open('bg.png')
    img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("img.png", "PNG")


def prueba3():
    pass


#prueba2()
#eliminarFondo1()

prueba3()
